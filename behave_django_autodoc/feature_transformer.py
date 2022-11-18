class FeatureTransformer:
    """Class to transform behave features to dict"""

    def __init__(self, feature):
        self.feature = feature

    def steps_to_dict(self, steps):
        """Transform a behave step to dict"""
        steps_dict = []
        for _step in steps:
            steps_dict.append({
                'title': _step.name,
                'description': _step.text and _step.text.replace('\n', '')
            })
        return steps_dict

    def scenarios_to_dict(self, scenarios):
        """Transform a behave scenarios list to dict"""
        scenarios_dict = []
        for scenario in scenarios:
            scenarios_dict.append({
                'title': scenario.name,
                'description': ''.join(scenario.description),
                'steps': self.steps_to_dict(scenario.steps)
            })
        return scenarios_dict

    def feature_to_dict(self):
        """Transform a behave feature to dict"""
        return {
            'title': self.feature.name,
            'description': self.feature.description,
            'scenarios': self.scenarios_to_dict(self.feature.scenarios)
        }
