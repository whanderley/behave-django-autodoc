"""
Module to build the html string containing the documentation.
"""
from pkg_resources import resource_string


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
