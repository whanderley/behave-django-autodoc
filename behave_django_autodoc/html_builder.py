"""
Module to build the html string containing the documentation.
"""
from pkg_resources import resource_string

from behave_django_autodoc.output_formats import OutputFormat


class HtmlBuilder(object):
    """
    class to build the html string containing the documentation, based on elements from features files.
    """

    def __init__(self):
        self.string = resource_string(
            "behave_django_autodoc", "assets/initial_html.html").decode('utf-8')

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

    def add_step(self, step):
        """
        Add a step to the html string.
        :param step: step object
        """
        self.string += step.to_html()

    def save(self, docs_dir):
        """
        Save the html string in the chosen formats(for now only html is available).
        :param docs_dir: directory where the documentation will be saved
        """
        self.string += resource_string(
           "behave_django_autodoc", "assets/final_html.html").decode('utf-8')
        self.string += resource_string(
            "docme", "assets/doc.css").decode('utf-8') + "</style></html>"
        OutputFormat(self.string, ['html'], docs_dir).save()
