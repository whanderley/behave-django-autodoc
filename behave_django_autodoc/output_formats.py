"""
Module to save the documentation in different formats(html, pdf).
"""
import os.path


class OutputFormat(object):
    """Class to save the documentation in formats like html, pdf"""

    def __init__(self, html_string, docs_dir):
        self.html_string = html_string
        self.docs_dir = docs_dir


class HtmlFormat(OutputFormat):
    """Class to save the documentation in html format"""

    def save(self):
        html_path = os.path.join(self.docs_dir, "doc.html")
        html_doc = open(html_path, "w+")
        html_doc.writelines(self.html_string)
        html_doc.close()
