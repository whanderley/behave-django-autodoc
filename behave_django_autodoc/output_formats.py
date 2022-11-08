"""
Module to save the documentation in different formats(html, pdf).
"""


class OutputFormat(object):
    """Class to save the documentation in formats like html, pdf"""
    def __init__(self, html_string, docs_dir):
        self.html_string = html_string
        self.docs_dir = docs_dir
