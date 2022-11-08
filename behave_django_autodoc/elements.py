"""Abstraction of the elements from the behave, like feature, scenario and step."""


class Feature(object):
    """
    Feature object representation
    fields:
        tittle: feature tittle
        description: feature description(optional)
    """

    def __init__(self, feature_dict) -> None:
        self.tittle = feature_dict["tittle"]
        self.description = feature_dict.get("description", None)


class Scenario(object):
    """
    Scenario object representation
    fields:
        tittle: scenario tittle
        description: scenario description(optional)
        layout: scenario layout, vertical or horizontal(optional)
    """

    def __init__(self, scenario_dict) -> None:
        self.tittle = scenario_dict["tittle"]
        self.description = scenario_dict.get("description", None)
        self.layout = scenario_dict.get("layout", "vertical")
        if self.layout not in ["vertical", "horizontal"]:
            raise ValueError(f"Invalid layout: {self.layout}")


class Step(object):
    """
    Step object representation
    fields:
        tittle: step tittle
        description: step description(optional)
        layout: step layout, vertical or horizontal(optional)
        screenshot_time: when to take the screenshot, before or after the step(optional)
    """

    def __init__(self, step_dict) -> None:
        self.tittle = step_dict["tittle"]
        self.description = step_dict.get("description", None)
        self.layout = step_dict.get("layout", "vertical")
        self.screenshot = step_dict.get("screenshot", True)
        self.screenshot_time = step_dict.get("screenshot_time", "after")
        if self.layout not in ["vertical", "horizontal"]:
            raise ValueError(f"Invalid layout: {self.layout}")
        if self.screenshot_time not in ["before", "after"]:
            raise ValueError(f"Invalid screenshot_time: {self.screenshot_time}")
