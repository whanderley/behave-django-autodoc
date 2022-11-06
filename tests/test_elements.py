# -*- coding: utf-8 -*-
import unittest

from behave_django_autodoc.elements import Feature
from behave_django_autodoc.elements import Scenario
from behave_django_autodoc.elements import Step


class TestFeature(unittest.TestCase):
    def test_init(self):
        feature = Feature({"tittle": "test tittle", "description": "test description"})
        self.assertEqual(feature.tittle, "test tittle")
        self.assertEqual(feature.description, "test description")

    def test_init_with_empty_description(self):
        feature = Feature({"tittle": "test tittle"})
        self.assertEqual(feature.tittle, "test tittle")
        self.assertEqual(feature.description, None)


class TestScenario(unittest.TestCase):
    def test_init(self):
        scenario = Scenario(
            {
                "tittle": "test tittle",
                "description": "test description",
                "layout": "vertical",
            }
        )
        self.assertEqual(scenario.tittle, "test tittle")
        self.assertEqual(scenario.description, "test description")
        self.assertEqual(scenario.layout, "vertical")

    def test_init_with_empty_description(self):
        scenario = Scenario({"tittle": "test tittle", "layout": "vertical"})
        self.assertEqual(scenario.tittle, "test tittle")
        self.assertEqual(scenario.description, None)
        self.assertEqual(scenario.layout, "vertical")

    def test_by_default_vertical_layout(self):
        scenario = Scenario({"tittle": "test tittle"})
        self.assertEqual(scenario.layout, "vertical")

    def test_not_accept_invalid_layout(self):
        with self.assertRaises(ValueError):
            Scenario({"tittle": "test tittle", "layout": "invalid"})


class TestStep(unittest.TestCase):
    def test_init(self):
        step = Step(
            {
                "tittle": "test tittle",
                "description": "test description",
                "layout": "vertical",
            }
        )
        self.assertEqual(step.tittle, "test tittle")
        self.assertEqual(step.description, "test description")
        self.assertEqual(step.layout, "vertical")

    def test_init_with_empty_description(self):
        step = Step({"tittle": "test tittle"})
        self.assertEqual(step.tittle, "test tittle")
        self.assertEqual(step.description, None)

    def test_by_default_vertical_layout(self):
        step = Step({"tittle": "test tittle"})
        self.assertEqual(step.layout, "vertical")

    def test_not_accept_invalid_layout(self):
        with self.assertRaises(ValueError):
            Step({"tittle": "test tittle", "layout": "invalid"})

    def test_screenshot_time(self):
        step = Step({"tittle": "test tittle", "screenshot_time": "after"})
        self.assertEqual(step.screenshot_time, "after")

    def test_by_default_screenshot_time_after(self):
        step = Step({"tittle": "test tittle"})
        self.assertEqual(step.screenshot_time, "after")

    def test_not_accept_invalid_screenshot_time(self):
        with self.assertRaises(ValueError):
            Step({"tittle": "test tittle", "screenshot_time": "invalid"})
