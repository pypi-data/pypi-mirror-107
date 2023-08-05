import os
from PIL import Image, ImageDraw
from robot.libraries.BuiltIn import BuiltIn
from .config import *


class Browser:
    def _get_current_browser(self):
        if hasattr(BuiltIn().get_library_instance(
                'SeleniumLibrary'), 'driver'):
            return BuiltIn().get_library_instance('SeleniumLibrary').driver
        else:
            return BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()

    def _get_element_coordinates(self, element_locator):
        browser = self._get_current_browser()
        element = browser.find_element_by_xpath(element_locator)
        location = element.location
        size = element.size
        return location, size

    def _exclude_elements(self, locator, screenshot, excluded_locators):
        if isinstance(excluded_locators, str):
            excluded_locators = [excluded_locators, ]

        with Image.open(screenshot) as image:
            element_location, element_size = self._get_element_coordinates(
                locator)
            for item in excluded_locators:
                excluded_element_location, excluded_element_size = self._get_element_coordinates(
                    item)
                x1 = excluded_element_location['x'] - element_location['x']
                y1 = excluded_element_location['y'] - element_location['y']
                x2 = x1 + excluded_element_size['width']
                y2 = y1 + excluded_element_size['height']
                draw = ImageDraw.Draw(image)
                draw.rectangle([(x1, y1), (x2, y2)], fill="lightgrey")
            image.save(screenshot)

    def _save_screenshot(self, temp_dir, locator, name,
                         excluded_locators, trim):
        browser = self._get_current_browser()
        element = browser.find_element_by_xpath(locator)

        screenshot_path = os.path.join(temp_dir, name)
        saved_screenshot = element.screenshot(screenshot_path)
        if not saved_screenshot:
            raise Exception('Failed to save screenshot')

        if excluded_locators:
            self._exclude_elements(locator, screenshot_path, excluded_locators)

        if trim:
            im = Image.open(screenshot_path)
            width, height = im.size
            cropped_image = im.crop(
                (0 + int(trim),
                 0 + int(trim),
                    width - int(trim),
                    height - int(trim)))
            cropped_image.save(screenshot_path)

        return screenshot_path
