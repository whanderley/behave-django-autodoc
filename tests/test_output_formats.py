import unittest

from behave_django_autodoc.output_formats import OutputFormat


class TestOutputFormat(unittest.TestCase):

    def test_init(self):
        output_format = OutputFormat(html_string="test html", docs_dir="dir/docs")
        self.assertEqual(output_format.html_string, "test html")
        self.assertEqual(output_format.docs_dir, "dir/docs")
