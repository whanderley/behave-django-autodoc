# -*- coding: utf-8 -*-
# flake8: noqa
from behave_django_autodoc.decorators import *


__version__ = "0.1.0"


def auto_doc(dict_functions):
    to_decorate_functions = ["before_all", "after_all", "before_feature",
                             "after_feature", "before_scenario", "after_scenario",
                             "before_step", "after_step"]
    for func in to_decorate_functions:
        decorator = eval(decorator_for_function(func))
        if func in dict_functions:
            dict_functions[func] = decorator(dict_functions[func])
        else:
            dict_functions[func] = decorator(lambda *args: None)


def decorator_for_function(function_name):
    words = function_name.split('_')
    return "".join([w.capitalize() for w in words]) + 'Decorator'
