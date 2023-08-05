import os
import string
import random
import shutil
from PIL import Image, ImageDraw, ImageFont
from robot.libraries.BuiltIn import _Variables as Variables
from .config import *


class Artifacts:
    def _create_temp_dir(self):
        temp_dir_path = os.path.join(
            Variables().get_variable_value("${OUTPUT DIR}"),
            f'temp-{"".join(random.choices(string.ascii_lowercase + string.digits, k=10))}')
        if not os.path.exists(temp_dir_path):
            os.makedirs(temp_dir_path)
            return temp_dir_path

    def _delete_temp_dir(self, temp_dir_path):
        if os.path.exists(temp_dir_path):
            shutil.rmtree(temp_dir_path)

    def _add_diff_file_to_report(self, source):
        source_file_name = os.path.split(source)[1]
        destination = os.path.join(
            Variables().get_variable_value("${OUTPUT DIR}"),
            DIR_FOR_SCREENSHOTS_IN_REPORT)
        if not os.path.exists(destination):
            os.makedirs(destination)

        destination_file = f'{"".join(random.choices(string.ascii_lowercase + string.digits, k=10))}-{source_file_name}'
        destination_file_path = os.path.join(destination, destination_file)
        shutil.copy(source, destination_file_path)
        return destination_file_path

    def _join_screenshots(self, image_actual, image_expected, image_diff):
        images = [
            Image.open(x) for x in [
                image_actual,
                image_expected,
                image_diff]]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths) + 20
        max_height = max(heights) + 30

        report_im = Image.new(
            'RGB', (total_width, max_height), color="dimgrey")
        report_im.paste(images[0], (5, 25))
        report_im.paste(images[1], (images[0].size[0] + 10, 25))
        report_im.paste(
            images[2],
            (images[0].size[0] +
             images[1].size[0] +
                15,
                25))
        title_font = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
        if os.path.exists(title_font):
            titles = ImageDraw.Draw(report_im)
            titles.text((5, 5), "ACTUAL", fill="yellow",
                        font=ImageFont.truetype(title_font, 16))
            titles.text(
                (images[0].size[0] + 10,
                 5),
                "EXPECTED",
                fill="lawngreen",
                font=ImageFont.truetype(
                    title_font,
                    16))
            titles.text(
                (images[0].size[0] +
                 images[1].size[0] +
                    15,
                    5),
                "DIFF",
                fill="red",
                font=ImageFont.truetype(
                    title_font,
                    16))
        else:
            titles = ImageDraw.Draw(report_im)
            titles.text((5, 5), "ACTUAL", fill="yellow")
            titles.text((images[0].size[0] + 10, 5),
                        "EXPECTED", fill="lawngreen")
            titles.text(
                (images[0].size[0] +
                 images[1].size[0] +
                    15,
                    5),
                "DIFF",
                fill="red")

        report_im.save(image_diff)
        return image_diff
