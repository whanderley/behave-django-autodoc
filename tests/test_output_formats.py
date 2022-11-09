import unittest
from unittest import mock

from behave_django_autodoc.output_formats import HtmlFormat
from behave_django_autodoc.output_formats import OutputFormat


class TestOutputFormat(unittest.TestCase):

    def test_init(self):
        output_format = OutputFormat(html_string="test html", docs_dir="dir/docs", formats=["html"])
        self.assertEqual(output_format.html_string, "test html")
        self.assertEqual(output_format.docs_dir, "dir/docs")
        self.assertEqual(output_format.formats, ["html"])

    @mock.patch('behave_django_autodoc.output_formats.HtmlFormat', autospec=True)
    def test_save(self, mock_html_format):
        output_format = OutputFormat(html_string="test html", docs_dir="dir/docs", formats=["html"])
        output_format.save()
        mock_html_format.assert_called_once_with("test html", "dir/docs")


class TestHtmlFormat(unittest.TestCase):

    @mock.patch('behave_django_autodoc.output_formats.os.path.join')
    @mock.patch('behave_django_autodoc.output_formats.os.path')
    @mock.patch('behave_django_autodoc.output_formats.open')
    def test_save(self, mock_open, mock_path, mock_join):
        mock_join.return_value = "dir/docs/doc.html"
        output_format = HtmlFormat(html_string="test html", docs_dir="dir/docs")
        output_format.save()
        mock_path.join.assert_called_with("dir/docs", "doc.html")
        mock_open.assert_called_with("dir/docs/doc.html", "w+")
        mock_open().writelines.assert_called_with("test html")
        mock_open().close.assert_called_with()
