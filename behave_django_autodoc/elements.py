'''Abstraction of the elements from the behave, like feature, scenario and step.'''


class Feature(object):
    '''
    Feature object representation
    fields:
        tittle: feature tittle
        description: feature description(optional)
    '''
    def __init__(self, feature_dict) -> None:
        self.tittle = feature_dict['tittle']
        self.description = feature_dict.get('description', None)


class Scenario(object):
    '''
    Scenario object representation
    fields:
        tittle: scenario tittle
        description: scenario description(optional)
        layout: scenario layout, vertical or horizontal(optional)
    '''
    def __init__(self, scenario_dict) -> None:
        self.tittle = scenario_dict['tittle']
        self.description = scenario_dict.get('description', None)
        self.layout = scenario_dict.get('layout', 'vertical')
        if self.layout not in ['vertical', 'horizontal']:
            raise ValueError(f'Invalid layout: {self.layout}')
