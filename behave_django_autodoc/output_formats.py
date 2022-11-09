"""
Module to save the documentation in different formats(html, pdf).
"""
import os.path


class OutputFormat(object):
    """Class to save the documentation in formats like html, pdf"""

    def __init__(self, html_string: str, docs_dir: str, formats: list = None) -> None:
        self.html_string = html_string
        self.docs_dir = docs_dir
        self.formats = formats

    def save(self) -> None:
        class_formats = {
            'html': HtmlFormat
        }
        for output_format in self.formats:
            output_format in class_formats and\
                class_formats[output_format](self.html_string, self.docs_dir).save()


class HtmlFormat(OutputFormat):
    """Class to save the documentation in html format"""

    def save(self) -> None:
        html_path = os.path.join(self.docs_dir, "doc.html")
        html_doc = open(html_path, "w+")
        html_doc.writelines(self.html_string)
        html_doc.close()
