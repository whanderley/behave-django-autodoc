from collections import OrderedDict


class FeatureTransformer:
    """Class to transform behave features to dict"""

    def __init__(self, feature):
        self.feature = feature

    def steps_to_dict(self, steps):
        """Transform a behave step to dict"""
        steps_dict = []
        for _step in steps:
            step_dict = OrderedDict()
            step_dict['title'] = _step.name
            step_dict['description'] = _step.text and str(_step.text)
            steps_dict.append(step_dict)

        return steps_dict

    def scenarios_to_dict(self, scenarios):
        """Transform a behave scenarios list to dict"""
        scenarios_dict = []
        for scenario in scenarios:
            scenario_dict = OrderedDict()
            scenario_dict['title'] = scenario.name
            scenario_dict['description'] = ''.join(scenario.description)
            scenario_dict['steps'] = self.steps_to_dict(scenario.steps)
            scenarios_dict.append(scenario_dict)
        return scenarios_dict

    def feature_to_dict(self):
        """Transform a behave feature to dict"""
        feature_dict = OrderedDict()
        feature_dict['title'] = self.feature.name
        feature_dict['description'] = ''.join(self.feature.description)
        feature_dict['scenarios'] = self.scenarios_to_dict(self.feature.scenarios)
        return feature_dict
