"""Abstraction of the elements from the behave, like feature, scenario and step."""
from jinja2 import Template as JinjaTemplate
from pkg_resources import resource_string


class ScreenShotError(Exception):
    pass


class Feature(object):
    """
    Feature object representation
    fields:
        title: feature title
        description: feature description(optional)
    """

    def __init__(self, feature_dict) -> None:
        self.title = feature_dict["title"]
        self.description = feature_dict.get("description", None)

    def to_html(self):
        """Generate the feature html"""

        feature_string = resource_string(
            "behave_django_autodoc", "assets/feature.html").decode('utf-8')
        feature_template = JinjaTemplate(feature_string)
        return feature_template.render(feature=self)


class Scenario(object):
    """
    Scenario object representation
    fields:
        title: scenario title
        description: scenario description(optional)
    """

    def __init__(self, scenario_dict) -> None:
        self.title = scenario_dict["title"]
        self.description = scenario_dict.get("description", None)

    def to_html(self):
        """Generate the scenario html"""

        scenario_string = resource_string(
            "behave_django_autodoc", "assets/scenario.html").decode('utf-8')
        scenario_template = JinjaTemplate(scenario_string)
        return scenario_template.render(scenario=self)


class Step(object):
    """
    Step object representation
    fields:
        title: step title
        description: step description(optional)
        layout: step layout, vertical or horizontal(optional, default vertical)
        screenshot: configure if the step should have a screenshot(optional, default True)
        screenshot_time: when to take the screenshot, before or after the step(optional, default after)
    """

    def __init__(self, step_dict) -> None:
        self.title = step_dict["title"]
        self.description = step_dict.get("description", None)
        self.layout = step_dict.get("layout", "vertical")
        self.screenshot = step_dict.get("screenshot", True)
        self.screenshot_time = step_dict.get("screenshot_time", "after")
        if self.layout not in ["vertical", "horizontal"]:
            raise ValueError(f"Invalid layout: {self.layout}")
        if self.screenshot_time not in ["before", "after"]:
            raise ValueError(f"Invalid screenshot_time: {self.screenshot_time}")

    def to_html(self, step_screenshot_base64=None):
        """Generate the step html"""
        if self.screenshot and not step_screenshot_base64:
            raise ScreenShotError("Screenshot base64 not found")
        step_string = resource_string(
            "behave_django_autodoc", f"assets/step_{self.layout}.html").decode('utf-8')
        step_template = JinjaTemplate(step_string)
        return step_template.render(step=self, step_screenshot_base64=step_screenshot_base64)
