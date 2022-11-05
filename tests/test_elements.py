# -*- coding: utf-8 -*-
import unittest
from behave_django_autodoc.elements import Feature, Scenario


class TestFeature(unittest.TestCase):

    def test_init(self):
        feature = Feature({'tittle': 'test tittle', 'description': 'test description'})
        self.assertEqual(feature.tittle, 'test tittle')
        self.assertEqual(feature.description, 'test description')

    def test_init_with_empty_description(self):
        feature = Feature({'tittle': 'test tittle'})
        self.assertEqual(feature.tittle, 'test tittle')
        self.assertEqual(feature.description, None)


class TestScenario(unittest.TestCase):

    def test_init(self):
        scenario = Scenario({'tittle': 'test tittle', 'description': 'test description', 'layout': 'vertical'})
        self.assertEqual(scenario.tittle, 'test tittle')
        self.assertEqual(scenario.description, 'test description')
        self.assertEqual(scenario.layout, 'vertical')

    def test_init_with_empty_description(self):
        scenario = Scenario({'tittle': 'test tittle', 'layout': 'vertical'})
        self.assertEqual(scenario.tittle, 'test tittle')
        self.assertEqual(scenario.description, None)
        self.assertEqual(scenario.layout, 'vertical')

    def test_by_default_vertical_layout(self):
        scenario = Scenario({'tittle': 'test tittle'})
        self.assertEqual(scenario.layout, 'vertical')

    def test_not_accept_invalid_layout(self):
        with self.assertRaises(ValueError):
            Scenario({'tittle': 'test tittle', 'layout': 'invalid'})
