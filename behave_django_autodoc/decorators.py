"""
Module containing decorators to environmental controls from behave.
"""
import os


class BaseDecorator(object):
    """
    Base decorator class to be inherited by all decorators.

    fields:
        function: function to be decorated
    """

    def __init__(self, function):
        self.function = function

    @property
    def behave_django_autodoc_dir(self):
        return os.path.join(os.path.dirname(self.function.__globals__["__file__"]), 'behave_django_autodoc')

    @property
    def docs_dir(self):
        return os.path.join(self.behave_django_autodoc_dir, 'docs')

    @property
    def features_configs_dir(self):
        return os.path.join(self.behave_django_autodoc_dir, 'features_configs')

    @property
    def images_dir(self):
        return os.path.join(self.docs_dir, 'images')
