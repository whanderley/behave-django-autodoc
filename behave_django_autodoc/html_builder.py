"""
Module to build the html string containing the documentation.
"""
import os
import re

from pkg_resources import resource_string

from behave_django_autodoc.browser_driver_adapter import BrowserDriver
from behave_django_autodoc.output_formats import OutputFormat


class HtmlBuilder(object):
    """
    class to build the html string containing the documentation, based on elements from features files.
    """

    def __init__(self):
        self.string = resource_string(
            __name__, "assets/initial_html.html").decode('utf-8')

    def add_feature(self, feature):
        """
        Add a feature to the html string.
        :param feature: feature object
        """
        self.string += feature.to_html()

    def add_scenario(self, scenario):
        """
        Add a scenario to the html string.
        :param scenario: scenario object
        """
        self.string += scenario.to_html()

    def add_step(self, step, images_dir, context):
        """
        Add a step to the html string.
        :params
            step: step object
            images_dir: directory where the screenshots will be saved
            context: behave context
        """
        if step.screenshot:
            screenshot_path = os.path.join(images_dir, re.sub(r"\W|^(?=\d)", '_', step.title) + ".png")
            image64 = BrowserDriver(context.browser).take_screenshot(screenshot_path)
            self.string += step.to_html(image64)
        else:
            self.string += step.to_html()

    def save(self, docs_dir):
        """
        Save the html string in the chosen formats(for now only html is available).
        :param docs_dir: directory where the documentation will be saved
        """
        self.string += resource_string(
           __name__, "assets/final_html.html").decode('utf-8')
        self.string += resource_string(
            __name__, "assets/doc.css").decode('utf-8') + "</style></html>"
        OutputFormat(self.string, docs_dir, ['html']).save()
