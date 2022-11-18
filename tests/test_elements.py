# -*- coding: utf-8 -*-
import unittest

from behave_django_autodoc.elements import Feature
from behave_django_autodoc.elements import Scenario
from behave_django_autodoc.elements import ScreenShotError
from behave_django_autodoc.elements import Step


def _strip_whitespace(string):
    return string.replace(" ", "").replace("\t", "").replace("\n", "")


class TestFeature(unittest.TestCase):

    def test_init(self):
        feature = Feature({"title": "test title", "description": "test description"})
        self.assertEqual(feature.title, "test title")
        self.assertEqual(feature.description, "test description")

    def test_init_with_empty_description(self):
        feature = Feature({"title": "test title"})
        self.assertEqual(feature.title, "test title")
        self.assertEqual(feature.description, None)

    def test_to_html(self):
        expected_html = """
        <h2 class="feature-title"> test title </h2>
        <div class="row">
            <div class="col-8">
                <p class="feature-description">test description</p>
            </div>
        </div>
        """
        feature = Feature({"title": "test title", "description": "test description"})
        html = feature.to_html()
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))


class TestScenario(unittest.TestCase):
    def test_init(self):
        scenario = Scenario(
            {
                "title": "test title",
                "description": "test description",
            }
        )
        self.assertEqual(scenario.title, "test title")
        self.assertEqual(scenario.description, "test description")

    def test_init_with_empty_description(self):
        scenario = Scenario({"title": "test title", "layout": "vertical"})
        self.assertEqual(scenario.title, "test title")
        self.assertEqual(scenario.description, None)

    def test_join_description(self):
        scenario = Scenario(
            {
                "title": "test title",
                "description": ["test", "description"],
            }
        )
        self.assertEqual(scenario.description, "test description")

    def test_to_html(self):
        expected_html = """
        <h3 class="scenario-title"> test title </h3>
        <div class="row">
            <div class="col-8">
                <p class="scenario-description">test description</p>
            </div>
        </div>
        """
        scenario = Scenario(
            {
                "title": "test title",
                "description": "test description",
            }
        )
        html = scenario.to_html()
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))

    def test_equal(self):
        scenario1 = Scenario({"title": "test title", "description": "test description"})
        scenario2 = Scenario({"title": "test title", "description": "test description"})
        self.assertEqual(scenario1, scenario2)


class TestStep(unittest.TestCase):
    def test_init(self):
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "vertical",
            }
        )
        self.assertEqual(step.title, "test title")
        self.assertEqual(step.description, "test description")
        self.assertEqual(step.layout, "vertical")

    def test_init_with_empty_description(self):
        step = Step({"title": "test title"})
        self.assertEqual(step.title, "test title")
        self.assertEqual(step.description, None)

    def test_by_default_vertical_layout(self):
        step = Step({"title": "test title"})
        self.assertEqual(step.layout, "vertical")

    def test_not_accept_invalid_layout(self):
        with self.assertRaises(ValueError):
            Step({"title": "test title", "layout": "invalid"})

    def test_screenshot_time(self):
        step = Step({"title": "test title", "screenshot_time": "after"})
        self.assertEqual(step.screenshot_time, "after")

    def test_by_default_screenshot_time_after(self):
        step = Step({"title": "test title"})
        self.assertEqual(step.screenshot_time, "after")

    def test_not_accept_invalid_screenshot_time(self):
        with self.assertRaises(ValueError):
            Step({"title": "test title", "screenshot_time": "invalid"})

    def test_no_title_by_default_is_false(self):
        step = Step({"title": "test title"})
        self.assertFalse(step.no_title)

    def test_without_screen_shot(self):
        step = Step({"title": "test title", "screenshot": False})
        self.assertFalse(step.screenshot)

    def test_by_default_has_screen_shot(self):
        step = Step({"title": "test title"})
        self.assertTrue(step.screenshot)

    def test_to_html_vertical_step(self):
        expected_html = """
        <div class="row step">
            <div class="col-12">
                <span class="align-middle">
                    <p class=step-title>test title</p>
                    <p class="step-description">test description</p>
                </span>
            </div>
        </div>
        """
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "vertical",
                "screenshot": False,
            }
        )
        html = step.to_html()
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))

    def test_to_html_horizontal_step(self):
        expected_html = """
        <div class="row step">
            <div class="col-6">
                <span class="align-middle">
                    <p class=step-title>test title</p>
                    <p class="step-description">test description</p>
                </span>
            </div>
        </div>
        """
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "horizontal",
                "screenshot": False,
            }
        )
        html = step.to_html()
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))

    def test_to_horizontal_html_with_screenshot(self):
        expected_html = """
        <div class="row step">
            <div class="col-6"><img src='screenshot_base64' class="img-fluid rounded" /></div>
            <div class="col-6">
                <span class="align-middle">
                    <p class=step-title>test title</p>
                    <p class="step-description">test description</p>
                </span>
            </div>
        </div>
        """
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "horizontal",
                "screenshot": True,
            }
        )
        html = step.to_html(step_screenshot_base64='screenshot_base64')
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))

    def test_to_vertical_html_with_screenshot(self):
        expected_html = """
        <div class="row step">
            <div class="col-12"><img src='screenshot_base64' class="img-fluid rounded" /></div>
            <div class="col-12">
                <span class="align-middle">
                    <p class=step-title>test title</p>
                    <p class="step-description">test description</p>
                </span>
            </div>
        </div>
        """
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "vertical",
                "screenshot": True,
            }
        )
        html = step.to_html(step_screenshot_base64='screenshot_base64')
        self.assertEqual(_strip_whitespace(html), _strip_whitespace(expected_html))

    def test_to_html_with_no_title_vertical_layout(self):
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "vertical",
                "screenshot": True,
                "no-title": True,
            }
        )
        html = step.to_html(step_screenshot_base64='screenshot_base64')
        self.assertNotIn('step-title', html)

    def test_to_html_with_no_title_horizontal_layout(self):
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "horizontal",
                "screenshot": True,
                "no-title": True,
            }
        )
        html = step.to_html(step_screenshot_base64='screenshot_base64')
        self.assertNotIn('step-title', html)

    def test_to_html_with_no_doc_return_empty_string(self):
        step = Step(
            {
                "title": "test title",
                "description": "test description",
                "layout": "horizontal",
                "screenshot": True,
                "no_title": True,
                "no-doc": True,
            }
        )
        html = step.to_html(step_screenshot_base64='screenshot_base64')
        self.assertEqual(html, '')

    def test_step_screenshot_base64_is_mandatory_when_screenshot_is_true(self):
        with self.assertRaises(ScreenShotError):
            step = Step({"title": "test title", "screenshot": True})
            step.to_html()

    def test_equal(self):
        step1 = Step({"title": "test title", "description": "test description"})
        step2 = Step({"title": "test title", "description": "test description"})
        self.assertEqual(step1, step2)

    def test_not_equal(self):
        step1 = Step({"title": "test title", "description": "test description"})
        step2 = Step({"title": "test title", "description": "test description 2"})
        self.assertNotEqual(step1, step2)
