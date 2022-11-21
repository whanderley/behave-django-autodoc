import unittest
from unittest import mock
from unittest.mock import Mock

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

    @mock.patch('behave_django_autodoc.html_builder.os.path.join')
    @mock.patch('behave_django_autodoc.html_builder.BrowserDriver')
    def test_add_step_with_screenshot(self, mock_browser_driver, mock_join):
        html_builder = HtmlBuilder()
        mock_browser_driver.return_value.take_screenshot.return_value = "Image string base64"
        step_config = {"steps": [{"title": "title1", "description": "description1",
                                  "screenshot-time": "after", "screenshot": False},
                                 {"title": "title2", "description": "description2"}]}
        context = Mock(step_config=step_config)
        context.browser = Mock(__module__="splinter.driver.webdriver.firefox")
        step = mock.Mock(to_html=mock.Mock(return_value="step string"), screenshot=True, title="title2")
        html_builder.add_step(step, 'images_dir', context)
        step.to_html.assert_called_with('Image string base64')
        mock_join.assert_called_with('images_dir', 'title2.png')
        self.assertIn("step string", html_builder.string)

    @mock.patch('behave_django_autodoc.html_builder.os.path.join')
    @mock.patch('behave_django_autodoc.html_builder.BrowserDriver')
    def test_add_step_without_screenshot(self, mock_browser_driver, mock_join):
        html_builder = HtmlBuilder()
        step_config = {"steps": [{"title": "title1", "description": "description1",
                                  "screenshot-time": "after", "screenshot": False},
                                 {"title": "title2", "description": "description2"}]}
        context = Mock(step_config=step_config)
        context.browser = Mock(__module__="splinter.driver.webdriver.firefox")
        step = mock.Mock(to_html=mock.Mock(return_value="step string"), screenshot=False, title="title2")
        html_builder.add_step(step, 'images_dir', context)
        step.to_html.assert_called_with()
        self.assertIn("step string", html_builder.string)

    @mock.patch('behave_django_autodoc.html_builder.resource_string')
    @mock.patch('behave_django_autodoc.html_builder.OutputFormat', autospec=True)
    def test_save(self, mock_output_format, mock_resource_string):
        mock_resource_string.return_value.decode.return_value = "final html"
        html_builder = HtmlBuilder()
        html_builder.save('auto_docs')
        self.assertIn("final html", html_builder.string)
        mock_output_format(html_builder.string, 'auto_docs', ['html']).save.assert_called_with()
