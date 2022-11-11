import unittest
from unittest import mock
from unittest.mock import Mock

from behave_django_autodoc.decorators import BaseDecorator
from behave_django_autodoc.decorators import BeforeAllDecorator


class TestBaseDecorator(unittest.TestCase):

    def test_initialising(self):
        function = Mock()
        base_decorator = BaseDecorator(function)
        self.assertEqual(base_decorator.function, function)

    @mock.patch('behave_django_autodoc.decorators.os.path')
    def test_docs_dir(self, mock_path):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        mock_path.dirname.return_value = "enviroment_dir"
        mock_path.join.return_value = "enviroment_dir/docs"
        base_decorator = BaseDecorator(function)
        self.assertEqual(base_decorator.docs_dir(), "enviroment_dir/docs")


class TestBeforeAllDecorator(unittest.TestCase):

    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.docs_dir')
    @mock.patch('behave_django_autodoc.decorators.os.path')
    def test_get_configs_dir(self, mock_path, mock_docs_dir):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        base_decorator = BeforeAllDecorator(function)
        mock_path.dirname.return_value = "enviroment_dir"
        mock_docs_dir.return_value = "enviroment_dir/docs"
        base_decorator.get_features_configs_dir()
        mock_path.join.assert_called_with("enviroment_dir/docs", "features_configs")
