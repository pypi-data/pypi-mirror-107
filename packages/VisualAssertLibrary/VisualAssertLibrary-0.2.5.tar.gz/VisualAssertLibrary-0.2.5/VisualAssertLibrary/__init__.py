import os
from robot.libraries.BuiltIn import _Variables as Variables
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword, library
from .baseline import MegaBaseLine, LocalBaseline, FtpServerBaseline
from .comparator import Comparator
from .browser import Browser
from .artifacts import Artifacts
from .config import *


@library(scope='GLOBAL', auto_keywords=False)
class VisualAssertLibrary:

    @keyword
    def assert_screenshot(self, message, element_locator, image_expected,
                          exclude=None, cols=20, rows=20, factor=1000, trim=None):
        """
        Keyword to assert web element screenshot.
        :param message: Text to be displayed in report if test failed.
        :param element_locator: xpath to find the element that under test
        :param image_expected: path to the base line screenshot with expected result
        :param exclude: xpath to element to be excluded from comparing, xpath string or list of strings
        :param cols: number of columns to split images for comparison
        :param rows: number of rows to split images for comparison
        :param factor: accuracy of comparing screenshots
        :param trim: trim passed number of pixels from top/bottom/left/right
        :return: absolute path to joined diff image (actual result / expected result / diff) if test failed (screenshots
                 differ) or None if test passed (screenshots are identical)
        """
        if ".png" not in image_expected:
            image_expected = image_expected + ".png"

        # Use baseline if exist or save new baseline otherwise:
        if Variables().get_variable_value("${MEGA_BASELINE_DIR_NAME}"):
            temp_dir = Artifacts()._create_temp_dir()
            BuiltIn().log_to_console(f"\n1. Create temp dir {temp_dir}")

            BuiltIn().log_to_console("2. Search baseline with expected result")
            remote_mega_dir_name = Variables().get_variable_value(
                "${MEGA_BASELINE_DIR_NAME}")

            screenshot_actual = Browser()._save_screenshot(
                temp_dir, element_locator, image_expected, exclude, trim)

            screenshot_expected = MegaBaseLine().get(
                temp_dir, remote_mega_dir_name, image_expected)
            if screenshot_expected:
                diff_screenshot = Comparator()._analyze(
                    screenshot_actual, screenshot_expected, cols, rows, factor)
                if diff_screenshot:
                    BuiltIn().log_to_console(
                        "3. Test failed. Add diff screenshot to report")
                    report_diff_screenshot = Artifacts()._add_diff_file_to_report(diff_screenshot)
                    BuiltIn().log_to_console(f"4. Delete temp dir {temp_dir}")
                    Artifacts()._delete_temp_dir(temp_dir)
                    self._fail_visual_test(
                        message, image_expected, report_diff_screenshot)
                else:
                    BuiltIn().log_to_console("3. Test Pass")
                    BuiltIn().log_to_console(f"4. Delete temp dir {temp_dir}")
                    Artifacts()._delete_temp_dir(temp_dir)

            else:
                BuiltIn().log_to_console(
                    "3. Not found screenshot of expected result in baseline. Save new baseline with expected results")
                MegaBaseLine().save(screenshot_actual, remote_mega_dir_name)
                Artifacts()._delete_temp_dir(temp_dir)
        else:
            raise Exception(
                "Baseline with expected results is not set in visual tests. Please check configuration.")

    def _fail_visual_test(self, message,
                          baseline_screenshot_name,
                          path_to_joined_actual_expected_diff_image):
        """
        Fails visual test with message and joined screenshot (actual result / expected result / diff) in report.
        :param message: Text to be placed under the screenshot in report
        :param baseline_screenshot_name:
        :param path_to_joined_actual_expected_diff_image:
        """
        current_baseline_dir = Variables().get_variable_value(
            "${MEGA_BASELINE_DIR_NAME}")
        diff_image_file_name = os.path.split(
            path_to_joined_actual_expected_diff_image)[1]
        raise Exception(f'*HTML*Verification: <b>{message}</b>'
                        f'<br>Base line:'
                        f'<br> - directory: <i>"{current_baseline_dir}"</i>'
                        f'<br> - file: "<i>{baseline_screenshot_name}"</i>'
                        f'<br>ACTUAL / EXPECTED / DIFF:<br>'
                        f'<a href="{DIR_FOR_SCREENSHOTS_IN_REPORT}/{diff_image_file_name}">'
                        f'<img src="{DIR_FOR_SCREENSHOTS_IN_REPORT}/{diff_image_file_name}"'
                        f' width="98%" border="0" alt=""></a>')
