import unittest
from unittest import mock
from unittest.mock import Mock

import yaml

from behave_django_autodoc.decorators import AfterAllDecorator
from behave_django_autodoc.decorators import BaseDecorator
from behave_django_autodoc.decorators import BeforeAllDecorator
from behave_django_autodoc.decorators import BeforeFeatureDecorator
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
        before_all_decorator
        self.assertEqual(before_all_decorator.initialize_html_documentation().__class__, HtmlBuilder)

    def test_call(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_all_decorator = BeforeAllDecorator(function)
        context = Mock()
        before_all_decorator.create_docs_dir = Mock()
        before_all_decorator(context)
        before_all_decorator.create_docs_dir.assert_called_once_with()
        function.assert_called_once_with(context)
        self.assertEqual(context.html_doc_builder.__class__, HtmlBuilder)


class TestAfterAllDecorator(unittest.TestCase):

    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.docs_dir',  new_callable=mock.PropertyMock)
    def test_call(self, mock_docs_dir):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        after_all_decorator = AfterAllDecorator(function)
        context = Mock()
        mock_docs_dir.return_value = "enviroment_dir/behave_django_autodoc/docs"
        after_all_decorator(context)
        function.assert_called_once_with(context)
        context.html_doc_builder.save.assert_called_once_with("enviroment_dir/behave_django_autodoc/docs")


class TestBeforeFeatureDecorator(unittest.TestCase):

    @mock.patch('behave_django_autodoc.decorators.os.path.exists')
    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.features_configs_dir', new_callable=mock.PropertyMock)
    def test_get_feature_config_path(self, mock_features_configs_dir, mock_path_exists):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        feature = Mock(filename="filename.feature")
        mock_path_exists.return_value = True
        before_feature_decorator = BeforeFeatureDecorator(function)
        mock_features_configs_dir.return_value = "enviroment_dir/behave_django_autodoc/features_configs"
        before_feature_decorator.features_configs_dir = "features_configs_dir"
        self.assertEqual(before_feature_decorator.get_feature_config_path(feature),
                         "enviroment_dir/behave_django_autodoc/features_configs/filename.yaml")

    @mock.patch('behave_django_autodoc.decorators.os.path.exists')
    @mock.patch('behave_django_autodoc.decorators.BaseDecorator.features_configs_dir', new_callable=mock.PropertyMock)
    def test_raise_error_when_config_not_exist(self, mock_features_configs_dir, mock_file_exists):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        feature = Mock(filename="filename.feature")
        mock_file_exists.return_value = False
        before_feature_decorator = BeforeFeatureDecorator(function)
        mock_features_configs_dir.return_value = "enviroment_dir/behave_django_autodoc/features_configs"
        before_feature_decorator.features_configs_dir = "features_configs_dir"
        with self.assertRaises(FileNotFoundError):
            before_feature_decorator.get_feature_config_path(feature)

    @mock.patch('behave_django_autodoc.decorators.open')
    @mock.patch('behave_django_autodoc.decorators.yaml.load')
    @mock.patch('behave_django_autodoc.decorators.BeforeFeatureDecorator.get_feature_config_path')
    def test_load_feature_config(self, mock_get_feature_config_path, mock_yaml_load, mock_open):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        feature = Mock(filename="filename.feature")
        mock_get_feature_config_path.return_value = "config_path"
        before_feature_decorator = BeforeFeatureDecorator(function)
        before_feature_decorator.load_feature_config(feature)
        file_handle = mock_open.return_value.__enter__.return_value
        mock_open.assert_called_once_with("config_path", "r")
        mock_yaml_load.assert_called_once_with(file_handle, Loader=yaml.FullLoader)

    def test_extract_feature_config(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_feature_decorator = BeforeFeatureDecorator(function)
        feature_dict = {"title": "feature", "description": "description", "scenarios": [{"scenario": "scenario"}]}
        self.assertEqual(before_feature_decorator.extract_feature_config(feature_dict),
                         {"title": "feature", "description": "description"})
