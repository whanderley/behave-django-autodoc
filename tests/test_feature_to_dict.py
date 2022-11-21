"""Test class to transform behave features to dict"""
import unittest
from collections import OrderedDict
from unittest.mock import Mock

from behave_django_autodoc.feature_transformer import FeatureTransformer


class FeatureParserTest(unittest.TestCase):
    """Test class to transform behave features to dict"""

    def test_steps_to_dict(self):
        """Test to transform a behave step to dict"""
        feature = Mock()
        step = Mock()
        step.name = 'I have a step'
        step.text = 'And some text'
        feature_parser = FeatureTransformer(feature)
        steps_dict = feature_parser.steps_to_dict([step])
        self.assertEqual(steps_dict[0]['title'], 'I have a step')
        self.assertEqual(steps_dict[0]['description'], 'And some text')

    def test_scenarios_to_dict(self):
        """Test to transform a behave scenarios list to dict"""
        feature = Mock()
        scenario = Mock()
        scenario.name = 'I have a scenario'
        scenario.description = ['And some description']
        step = Mock()
        step.name = 'I have a step'
        step.text = 'And some text'
        scenario.steps = [step]
        feature_parser = FeatureTransformer(feature)
        scenarios_dict = feature_parser.scenarios_to_dict([scenario])
        self.assertEqual(scenarios_dict[0]['title'], 'I have a scenario')
        self.assertEqual(scenarios_dict[0]['description'], 'And some description')
        self.assertEqual(scenarios_dict[0]['steps'], [{'title': 'I have a step', 'description': 'And some text'}])

    def test_feature_to_dict(self):
        """Test to transform a behave feature to dict"""
        feature = Mock()
        feature.name = 'I have a feature'
        feature.description = 'And some description'
        scenario = Mock()
        scenario.name = 'I have a scenario'
        scenario.description = 'And some description'
        step = Mock()
        step.name = 'I have a step'
        step.text = 'And some text'
        scenario.steps = [step]
        feature.scenarios = [scenario]
        feature_parser = FeatureTransformer(feature)
        expected_dict = OrderedDict({
            'title': 'I have a feature',
            'description': 'And some description',
            'scenarios': [
                {
                    'title': 'I have a scenario',
                    'description': 'And some description',
                    'steps': [
                        {
                            'title': 'I have a step',
                            'description': 'And some text'
                        }
                    ]
                }
            ]
        })
        self.assertEqual(feature_parser.feature_to_dict(), expected_dict)
