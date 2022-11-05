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
