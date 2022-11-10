import unittest
from unittest import mock

from behave_django_autodoc.html_builder import HtmlBuilder


class TestHtmlBuilder(unittest.TestCase):

    @mock.patch('behave_django_autodoc.html_builder.resource_string')
    def test_init_with_initial_string(self, resource_string):
        resource_string.return_value.decode.return_value = "test html"
        html_builder = HtmlBuilder()
        self.assertEqual(html_builder.string, "test html")

    def test_add_feature(self):
        html_builder = HtmlBuilder()
        html_builder.add_feature(mock.Mock(to_html=mock.Mock(return_value="feature string")))
        self.assertIn("feature string", html_builder.string)

    def test_add_scenario(self):
        html_builder = HtmlBuilder()
        html_builder.add_scenario(mock.Mock(to_html=mock.Mock(return_value="scenario string")))
        self.assertIn("scenario string", html_builder.string)

    def test_add_step(self):
        html_builder = HtmlBuilder()
        html_builder.add_step(mock.Mock(to_html=mock.Mock(return_value="step string")))
        self.assertIn("step string", html_builder.string)
