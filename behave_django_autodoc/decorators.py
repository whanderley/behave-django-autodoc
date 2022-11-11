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

    def docs_dir(self):
        return os.path.join(os.path.dirname(self.function.__globals__["__file__"]), 'docs')


class BeforeAllDecorator(BaseDecorator):
    """
    Decorator to be used in before_all function.
    """

    def get_features_configs_dir(self):
        return os.path.join(self.docs_dir(), 'features_configs')
