# -*- coding: utf-8 -*-
import unittest

from behave_django_autodoc.elements import Feature
from behave_django_autodoc.elements import Scenario
from behave_django_autodoc.elements import Step


def _strip_whitespace(string):
    return string.replace(" ", "").replace("\t", "").replace("\n", "")


class TestFeature(unittest.TestCase):

    def _strip_whitespace(self, string):
        return string.replace(" ", "").replace("\t", "").replace("\n", "")

    def test_init(self):
        feature = Feature({"tittle": "test tittle", "description": "test description"})
        self.assertEqual(feature.tittle, "test tittle")
        self.assertEqual(feature.description, "test description")

    def test_init_with_empty_description(self):
        feature = Feature({"tittle": "test tittle"})
        self.assertEqual(feature.tittle, "test tittle")
        self.assertEqual(feature.description, None)

    def test_to_html(self):
        expected_html = """
        <h2 class="feature-tittle"> test tittle </h2>
        <div class="row">
            <div class="col-8">
                <p class="feature-description">test description</p>
            </div>
        </div>
        """
        feature = Feature({"tittle": "test tittle", "description": "test description"})
        html = feature.to_html()
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))


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

    def test_to_html(self):
        expected_html = """
        <h3 class="scenario-tittle"> test tittle </h3>
        <div class="row">
            <div class="col-8">
                <p class="scenario-description">test description</p>
            </div>
        </div>
        """
        scenario = Scenario(
            {
                "tittle": "test tittle",
                "description": "test description",
                "layout": "vertical",
            }
        )
        html = scenario.to_html()
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))


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

    def test_without_screen_shot(self):
        step = Step({"tittle": "test tittle", "screenshot": False})
        self.assertFalse(step.screenshot)

    def test_by_default_has_screen_shot(self):
        step = Step({"tittle": "test tittle"})
        self.assertTrue(step.screenshot)
