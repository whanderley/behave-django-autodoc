# -*- coding: utf-8 -*-
import unittest

from behave_django_autodoc import __version__
from behave_django_autodoc import auto_doc
from behave_django_autodoc import decorator_for_function


def test_version():
    assert __version__ == "0.1.0"


class TestAutoDoc(unittest.TestCase):

    def test_decorator_for_function(self):
        function_name = "before_all"
        self.assertEqual(decorator_for_function(function_name), "BeforeAllDecorator")
        function_name = "after_all"
        self.assertEqual(decorator_for_function(function_name), "AfterAllDecorator")
        function_name = "before_feature"
        self.assertEqual(decorator_for_function(function_name), "BeforeFeatureDecorator")

    def test_auto_doc(self):
        dict_functions = {'before_all': lambda *args: None, '__file__': "dir/enviroment.py"}
        auto_doc(dict_functions)
        self.assertEqual(dict_functions['before_all'].__class__.__name__, "BeforeAllDecorator")
        self.assertEqual(dict_functions['after_all'].__class__.__name__, "AfterAllDecorator")
        self.assertEqual(dict_functions['before_feature'].__class__.__name__, "BeforeFeatureDecorator")
        self.assertEqual(dict_functions['after_feature'].__class__.__name__, "AfterFeatureDecorator")
        self.assertEqual(dict_functions['before_scenario'].__class__.__name__, "BeforeScenarioDecorator")
        self.assertEqual(dict_functions['after_scenario'].__class__.__name__, "AfterScenarioDecorator")
