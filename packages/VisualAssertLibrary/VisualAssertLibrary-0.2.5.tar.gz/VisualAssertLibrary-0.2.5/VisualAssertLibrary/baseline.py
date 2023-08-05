import os
from mega import Mega
from robot.libraries.BuiltIn import _Variables as Variables
from .config import *


class MegaBaseLine:
    """
    Works with baseline placed on mega.nz
    """

    def __init__(self):
        mega_account_email = Variables().get_variable_value("${MEGA_EMAIL}")
        mega_account_passw = Variables().get_variable_value("${MEGA_PASSW}")

        self.mega = Mega()
        self.m = self.mega.login(mega_account_email, mega_account_passw)

    def get(self, temp_local_baseline_path, remote_mega_dir, image_expected):
        """
        Gets previously saved screenshot from Mega
        :param temp_local_baseline_path: Absolute path to local temp directory to download file to.
        :param remote_mega_dir: Name of the directory with a baseline on Mega
        :param image_expected: Name of the screenshot file with expected result.
        :return: Absolute path to downloaded baseline file
        """
        mega_dir = self.m.find(remote_mega_dir, exclude_deleted=True)
        files_in_target_folder = self.m.get_files_in_node(mega_dir[0])
        found_baseline_screenshot = False

        for file_id in files_in_target_folder.keys():
            if files_in_target_folder[file_id]['a']['n'] == image_expected:
                found_baseline_screenshot = True
                file_obj = (file_id, files_in_target_folder[file_id])
                self.m.download(
                    file_obj,
                    dest_path=temp_local_baseline_path,
                    dest_filename=f"expected-{image_expected}")
                break
        if found_baseline_screenshot:
            return os.path.join(temp_local_baseline_path,
                                f"expected-{image_expected}")
        else:
            print(
                f"Not found baseline screenshot '{image_expected}' in the dir '{remote_mega_dir}'")
            return None

    def save(self, temp_local_baseline_screenshot_path, remote_mega_dir):
        """
        Save new baseline to Mega
        :param temp_local_baseline_screenshot_path: Absolute path to local file to be saved in Mega.
        :param remote_mega_dir: Name of the directory with a baseline on Mega
        """
        mega_dir = self.m.find(remote_mega_dir, exclude_deleted=True)
        if mega_dir:
            files_in_target_folder = self.m.get_files_in_node(mega_dir[0])
            if len(files_in_target_folder) == 0:
                self.m.upload(
                    temp_local_baseline_screenshot_path,
                    dest=mega_dir[0])
            else:
                existing_file_nodes = files_in_target_folder.keys()
                for file_uuid in existing_file_nodes:
                    if files_in_target_folder[file_uuid]['a']['n'] == os.path.split(
                            temp_local_baseline_screenshot_path)[1]:
                        self.m.delete(file_uuid)
                        break
                self.m.upload(
                    temp_local_baseline_screenshot_path,
                    dest=mega_dir[0])
        else:
            raise Exception(f"Not found '{remote_mega_dir}' in MEGA")


class LocalBaseline:
    """
    Works with baseline placed on local machine
    """
    pass


class FtpServerBaseline:
    """
    Works with baseline placed on a remote server via FTP
    """
    pass
