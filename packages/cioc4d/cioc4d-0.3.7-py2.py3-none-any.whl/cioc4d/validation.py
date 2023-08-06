import os
import c4d
import sys
from ciopath.gpath import Path
from ciopath.gpath_list import GLOBBABLE_REGEX, PathList
from ciocore.validator import ValidationError, Validator
from cioc4d import const as k
from ciocore import data as coredata


class ValidateUploadDaemon(Validator):
    def run(self, _):
        dialog = self._submitter
        use_daemon = dialog.section("UploadOptionsSection").use_daemon_widget.get_value()
        if not use_daemon:
            return

        msg = "This submission expects an uploader daemon to be running.\n After you press submit you can open a shell and type: 'conductor uploader'"

        location = (dialog.section("LocationSection").widget.get_value() or "").strip()
        if location:
            msg = "This submission expects an uploader daemon to be running and set to a specific location tag.\nAfter you press OK you can open a shell and type: 'conductor uploader --location {}'".format(
                location
            )

        self.add_notice(msg)
        # By also writing the message to the console, the user can copy paste
        # `conductor uploader --location blah`.
        c4d.WriteConsole(msg)


class ValidateTaskCount(Validator):
    def run(self, _):
        dialog = self._submitter
        count = dialog.section("InfoSection").frame_count
        if count > 1000:
            self.add_notice(
                "This submission contains over 1000 tasks ({}). Are you sure this is correct?".format(
                    count
                )
            )

class ValidateRedshiftGPU(Validator):
    def run(self, _):
        dialog = self._submitter

        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()
        renderer = render_data[c4d.RDATA_RENDERENGINE]
        if renderer != k.RENDERERS["redshift"]:
            return
        
        description = dialog.section("GeneralSection").instance_types_widget.get_selected_value()

        instance_type = next(
            (it for it in coredata.data()["instance_types"] if it["description"] == description), None
        )

        if not (instance_type and instance_type["gpu"]):
            msg = "The Redshift renderer is not compatible with the instance type: '{}' as it has no graphics card.\n".format(
                description
            )
            msg += "Please select a machine with a graphics card in the General section of the submitter. The submission is blocked as it would incur unexpected costs."
            self.add_error(msg)
            return



class ValidateDestinationDirectoryClash(Validator):
    def run(self, _):
        dialog = self._submitter
        bad_dest_msg = "There was an error while trying to resolve the destination directory."

        tasks_section = dialog.section("TaskSection")
        is_override = tasks_section.widget.get_visible()

        if is_override:
            dest = tasks_section.get_custom_destination()
            bad_dest_msg += "Please check the value for the destination folder in the submitter."
        else:
            dest = tasks_section.get_common_destination()
            bad_dest_msg += "Please check your image paths all save to the same filesystem."

        dest_path = ""
        try:
            dest_path = Path(dest).fslash(with_drive=False)
        except BaseException:
            self.add_error(bad_dest_msg)

        path_list = dialog.section("AssetsSection").get_assets_path_list()

        for gpath in path_list:
            asset_path = gpath.fslash(with_drive=False)
            if asset_path.startswith(dest_path):
                c4d.WriteConsole(
                    "Some of your upload assets exist in the specified output destination directory\n. {} contains {}.".format(
                        dest_path, asset_path
                    )
                )
                self.add_error(
                    "The destination directory for rendered output ({}) contains assets that are in the upload list. This can cause your render to fail. See the script editor for details.".format(
                        dest_path
                    )
                )
                break
            if dest_path.startswith(asset_path):
                c4d.WriteConsole(
                    "You are trying to upload a directory that contains your destination directory.\n. {} contains {}".format(
                        asset_path, dest_path
                    )
                )
                self.add_error(
                    "One of your assets is a directory that contains the specified output destination directory. This will cause your render to fail. See the script editor for details."
                )
                break


class ValidateCustomTaskTemplate(Validator):
    def run(self, _):
        dialog = self._submitter
        tasks_section = dialog.section("TaskSection")
        if not tasks_section.widget.get_visible():
            return

        self.add_notice(
            """You are using a custom task template. 
We strongly recommend you use the -oimage and/or -omultipass flags to specify your image output.
Please ensure these paths are below the Destination directory, as it's the only writable location. 
Check the Preview panel."""
        )
        return


class ValidateMissingExtraAssets(Validator):
    def run(self, _):

        missing = []
        for gpath in self._submitter.section("AssetsSection").pathlist:
            pp = gpath.fslash()
            if not os.path.exists(pp):
                missing.append(pp)

        if missing:
            self.add_warning(
                "Some of the assets specified in the Extra Assets section do not exist on disk. See the console for details. You can continue if you don't need them."
            )

            c4d.WriteConsole("----- Conductor Asset Validation -------\n")
            for asset in missing:
                c4d.WriteConsole("Missing: {}\n".format(asset))


class ValidateAbsoluteWindowsPaths(Validator):
    def run(self, _):
        if not sys.platform == "win32":
            return
        document = c4d.documents.GetActiveDocument()
        if k.C4D_VERSION < 22:
            assets = c4d.documents.GetAllAssets(document, False, "")
        else:
            assets = []
            success = c4d.documents.GetAllAssetsNew(document, False, "", flags=c4d.ASSETDATA_FLAG_WITHCACHES, assetList=assets)

        bad_assets = []

        for asset in assets:
            assetname = asset["assetname"]
            if assetname:
                pth = Path(assetname)
                if pth.absolute and not pth.is_unc:
                    bad_assets.append(asset)

        if bad_assets:
            msg = "Some assets have absolute paths containing Windows drive letters. These files won't be found correctly on Conductor's render nodes."
            msg += "Please use relative texture paths. The easiest way to do this is to run File->Save Project with Assets"
            msg += "Alternatively. Move all assets to your tex folder and enter their filenames in your materials."
            msg += "See the console for a list of files that need to be addressed."
            self.add_warning(msg)
            c4d.WriteConsole("-" * 30)
            c4d.WriteConsole("The following asset paths should be made relative.")
            for asset in bad_assets:
                ob = asset["owner"]
                c4d.WriteConsole("{} -->> {}".format(ob.GetName(), asset["assetname"]))

        # Now check the output paths
        render_data = document.GetActiveRenderData()
        doc_path = document.GetDocumentPath()

        for output_type_enum, output_path_enum in [
            (c4d.RDATA_SAVEIMAGE, c4d.RDATA_PATH),
            (c4d.RDATA_MULTIPASS_SAVEIMAGE, c4d.RDATA_MULTIPASS_FILENAME),
        ]:
            self._check_image_path(doc_path, render_data, output_type_enum, output_path_enum)

    def _check_image_path(self, doc_path, render_data, output_type_enum, output_path_enum):
        """Return the output image if it is active."""
        save_enabled = render_data[c4d.RDATA_GLOBALSAVE]
        do_image_save = render_data[output_type_enum]
        if save_enabled and do_image_save:
            image_path = render_data[output_path_enum]
            if image_path:
                pth = Path(image_path)
                if pth.absolute and not pth.is_unc:
                    msg = "Some image outputs contain Windows drive letters. '"
                    msg += image_path
                    msg += "' As Conductor render nodes are Linux based, you'll need to "
                    msg += "specify only relative or UNC image paths in Render Settings."
                    self.add_warning(msg)


class ValidateDontSaveVideoPosts(Validator):

    GI_AUTOSAVE_ID = 3804
    AO_AUTOSAVE_ID = 2204
    AO_USE_CACHE_ID = 2000

    def run(self, _):
        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()
        vp = render_data.GetFirstVideoPost()
        while vp:
            if vp.CheckType(c4d.VPglobalillumination):
                self._validate_video_post(vp, "Global Illumination", self.GI_AUTOSAVE_ID)
            elif vp.CheckType(c4d.VPambientocclusion):
                self._validate_video_post(
                    vp, "Ambient occlusion", self.AO_AUTOSAVE_ID, self.AO_USE_CACHE_ID
                )
            vp = vp.GetNext()

    def _validate_video_post(self, vp, label, *ids):
        if vp.GetBit(c4d.BIT_VPDISABLED):
            return
        container = vp.GetDataInstance()
        for element_id in ids:
            if not container[element_id]:
                return

        self.add_warning(
            "{} Auto Save is set to ON. You should turn it off for the render, otherwise it may try to write files in a read-only directory and cause the render to fail".format(
                label
            )
        )


# Implement more validators here
####################################
####################################


def run(dialog, submitting=True):

    errors, warnings, notices = _run_validators(dialog)

    if errors:
        msg = ""
        msg += "Some errors would cause the submission to fail:\n\n" + "\n".join(errors) + "\n"
        c4d.gui.MessageDialog(msg, type=c4d.GEMB_OK)
        raise ValidationError(msg)
    if notices or warnings:
        if submitting:
            msg = "Would you like to continue this submission?\n\n"
            dialog_type = c4d.GEMB_OKCANCEL
        else:
            msg = "Validate only.\n\n"
            dialog_type = c4d.GEMB_OK

        if warnings:
            msg += (
                "Please check the warnings below:\n\n"
                + "\n\n".join(["[WARN]:{}".format(w) for w in warnings])
                + "\n\n"
            )
        if notices:
            msg += (
                "Please check the notices below:\n\n"
                + "\n\n".join(["[INFO]:{}".format(n) for n in notices])
                + "\n\n"
            )

        result = c4d.gui.MessageDialog(msg, type=dialog_type)
        if result != c4d.GEMB_R_OK:
            c4d.WriteConsole("Submission cancelled by user.\n")
            raise ValidationError(msg)
    else:
        if not submitting:
            msg = "No issues found!"
            result = c4d.gui.MessageDialog(msg, type=c4d.GEMB_OK)


def _run_validators(dialog):

    takename = "Main"
    validators = [plugin(dialog) for plugin in Validator.plugins()]
    for validator in validators:
        validator.run(takename)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices
