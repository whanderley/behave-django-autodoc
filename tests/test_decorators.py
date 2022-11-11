import unittest
from unittest import mock
from unittest.mock import Mock

from behave_django_autodoc.decorators import BaseDecorator
from behave_django_autodoc.decorators import BeforeAllDecorator
from behave_django_autodoc.html_builder import HtmlBuilder


class TestBaseDecorator(unittest.TestCase):

    def test_initialising(self):
        function = Mock()
        base_decorator = BaseDecorator(function)
        self.assertEqual(base_decorator.function, function)

    @mock.patch('behave_django_autodoc.decorators.os.path')
    def test_get_behave_django_autodoc_dir(self, mock_path):
        function = Mock(__globals__={"__file__": "enviroment_dir/enviroment.py"})
        mock_path.dirname.return_value = "enviroment_dir"
        mock_path.join.return_value = "enviroment_dir/behave_django_autodoc"
        base_decorator = BaseDecorator(function)
        self.assertEqual(base_decorator.behave_django_autodoc_dir, "enviroment_dir/behave_django_autodoc")

    @mock.patch('behave_django_autodoc.decorators.os.path.join')
    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.behave_django_autodoc_dir',
                new_callable=mock.PropertyMock)
    def test_get_docs_dir(self, mock_behave_django_autodoc_dir, mock_path_join):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        mock_behave_django_autodoc_dir.return_value = "enviroment_dir/behave_django_autodoc"
        base_decorator = BaseDecorator(function)
        base_decorator.docs_dir
        mock_path_join.assert_called_once_with("enviroment_dir/behave_django_autodoc", 'docs')

    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.behave_django_autodoc_dir',
                new_callable=mock.PropertyMock)
    def test_get_features_configs_dir(self, mock_behave_django_autodoc_dir):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        mock_behave_django_autodoc_dir.return_value = "enviroment_dir/behave_django_autodoc"
        base_decorator = BaseDecorator(function)
        self.assertEqual(base_decorator.features_configs_dir, "enviroment_dir/behave_django_autodoc/features_configs")

    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.docs_dir', new_callable=mock.PropertyMock)
    def test_get_images_dir(self, mock_docs_dir):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        mock_docs_dir.return_value = "enviroment_dir/behave_django_autodoc/docs"
        base_decorator = BaseDecorator(function)
        self.assertEqual(base_decorator.images_dir, "enviroment_dir/behave_django_autodoc/docs/images")


class TestBeforeAllDecorator(unittest.TestCase):

    @mock.patch('behave_django_autodoc.decorators.os.makedirs')
    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.docs_dir',
                new_callable=mock.PropertyMock)
    def create_docs_dir(self, mock_docs_dir, mock_makedirs):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        mock_docs_dir.return_value = "enviroment_dir/behave_django_autodoc/docs"
        before_all_decorator = BeforeAllDecorator(function)
        before_all_decorator.create_docs_dir()
        mock_makedirs.assert_called_once_with("enviroment_dir/behave_django_autodoc/docs", exist_ok=True)

    def test_initializate_html_documentation(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_all_decorator = BeforeAllDecorator(function)
        before_all_decorator.initialize_html_documentation()
        self.assertEqual(before_all_decorator.html_documentation.__class__, HtmlBuilder)
