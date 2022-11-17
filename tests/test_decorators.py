import unittest
from unittest import mock
from unittest.mock import Mock

import yaml

from behave_django_autodoc.decorators import AfterAllDecorator
from behave_django_autodoc.decorators import AfterFeatureDecorator
from behave_django_autodoc.decorators import AfterScenarioDecorator
from behave_django_autodoc.decorators import AfterStepDecorator
from behave_django_autodoc.decorators import BaseDecorator
from behave_django_autodoc.decorators import BeforeAllDecorator
from behave_django_autodoc.decorators import BeforeFeatureDecorator
from behave_django_autodoc.decorators import BeforeScenarioDecorator
from behave_django_autodoc.decorators import BeforeStepDecorator
from behave_django_autodoc.elements import Scenario
from behave_django_autodoc.elements import Step
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
    def test_create_docs_dir(self, mock_docs_dir, mock_makedirs):
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

    @mock.patch('behave_django_autodoc.decorators.FeatureTransformer.feature_to_dict')
    @mock.patch('behave_django_autodoc.decorators.open')
    @mock.patch('behave_django_autodoc.decorators.yaml.load')
    @mock.patch('behave_django_autodoc.decorators.BeforeFeatureDecorator.get_feature_config_path')
    def test_load_feature_config(self, mock_get_feature_config_path, mock_yaml_load,
                                 mock_open, mock_feature_to_dict):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        feature = Mock(filename="filename.feature")
        mock_get_feature_config_path.return_value = "config_path"
        before_feature_decorator = BeforeFeatureDecorator(function)
        mock_feature_to_dict.return_value = {}
        before_feature_decorator.load_feature_config(feature)
        file_handle = mock_open.return_value.__enter__.return_value
        mock_yaml_load.assert_called_once_with(file_handle, Loader=yaml.FullLoader)

    @mock.patch('behave_django_autodoc.decorators.yaml.dump')
    @mock.patch('behave_django_autodoc.decorators.FeatureTransformer.feature_to_dict')
    @mock.patch('behave_django_autodoc.decorators.open')
    @mock.patch('behave_django_autodoc.decorators.yaml.load')
    @mock.patch('behave_django_autodoc.decorators.BeforeFeatureDecorator.get_feature_config_path')
    def test_load_feature_config_when_file_not_exist(self, mock_get_feature_config_path, mock_yaml_load,
                                                     mock_open, mock_feature_to_dict, mock_yaml_dump):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        feature = Mock(filename="filename.feature")
        mock_get_feature_config_path.return_value = "config_path"
        before_feature_decorator = BeforeFeatureDecorator(function)
        mock_feature_to_dict.return_value = {}
        before_feature_decorator.load_feature_config(feature)
        file_handle = mock_open.return_value.__enter__.return_value
        mock_yaml_dump.assert_called_once_with({}, file_handle, default_flow_style=False)
        mock_yaml_load.assert_called_once_with(file_handle, Loader=yaml.FullLoader)

    def test_extract_feature_config(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_feature_decorator = BeforeFeatureDecorator(function)
        feature_dict = {"title": "feature", "description": "description", "scenarios": [{"scenario": "scenario"}]}
        self.assertEqual(before_feature_decorator.extract_feature_config(feature_dict),
                         {"title": "feature", "description": "description"})

    @mock.patch('behave_django_autodoc.html_builder.HtmlBuilder.add_feature')
    @mock.patch('behave_django_autodoc.decorators.BeforeFeatureDecorator.extract_feature_config')
    @mock.patch('behave_django_autodoc.decorators.BeforeFeatureDecorator.load_feature_config')
    def test_call(self, mock_load_feature_config, mock_extract_feature_config, mock_add_feature):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_feature_decorator = BeforeFeatureDecorator(function)
        feature = Mock(filename="filename.feature")
        context = Mock()
        mock_load_feature_config.return_value = {"title": "feature", "description": "description",
                                                 "scenarios": [{"scenario": "scenario"}]},
        mock_extract_feature_config.return_value = {"title": "feature", "description": "description"}
        before_feature_decorator(context, feature)
        before_feature_decorator.load_feature_config.assert_called_once_with(feature)
        before_feature_decorator.extract_feature_config.assert_called_once_with(
            before_feature_decorator.load_feature_config.return_value)
        function.assert_called_once_with(context, feature)
        context.html_doc_builder.add_feature.assert_called()
        self.assertEqual(context.feature_doc_config, before_feature_decorator.load_feature_config.return_value)


class TestAfterFeatureDecorator(unittest.TestCase):

    def test_call(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        after_feature_decorator = AfterFeatureDecorator(function)
        feature = Mock(filename="filename.feature")
        context = Mock()
        after_feature_decorator(context, feature)
        function.assert_called_once_with(context, feature)


class TestBeforeScenarioDecorator(unittest.TestCase):

    def test_load_scenario_config_element(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_scenario_decorator = BeforeScenarioDecorator(function)
        scenario = Mock()
        scenario.name = "title1"
        feature_config = {"scenarios": [{"title": "title1", "description": "description1"},
                                        {"title": "title2", "description": "description2"}]}
        context = Mock(feature_config=feature_config)
        self.assertEqual(before_scenario_decorator.load_scenario_config_doc(context, scenario),
                         Scenario({"title": "title1", "description": "description1"}))

    @mock.patch('behave_django_autodoc.decorators.HtmlBuilder.add_scenario')
    @mock.patch('behave_django_autodoc.decorators.BeforeScenarioDecorator.load_scenario_config_doc')
    def test_call(self, mock_load_scenario_config_doc, mock_add_scenario):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_scenario_decorator = BeforeScenarioDecorator(function)
        scenario = Mock()
        scenario.name = "title1"
        feature_config = {"scenarios": [{"title": "title1", "description": "description1"},
                                        {"title": "title2", "description": "description2"}]}
        context = Mock(feature_config=feature_config)
        before_scenario_decorator(context, scenario)
        function.assert_called_once_with(context, scenario)
        before_scenario_decorator.load_scenario_config_doc.assert_called_once_with(context, scenario)
        context.html_doc_builder.add_scenario.assert_called_once_with(
            before_scenario_decorator.load_scenario_config_doc.return_value)
        self.assertEqual(context.scenario_doc_config, before_scenario_decorator.load_scenario_config_doc.return_value)


class TestAfterScenarioDecorator(unittest.TestCase):

    def test_call(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        after_scenario_decorator = AfterScenarioDecorator(function)
        scenario = Mock()
        context = Mock()
        after_scenario_decorator(context, scenario)
        function.assert_called_once_with(context, scenario)


class TestBeforeStepDecorator(unittest.TestCase):

    def test_load_step_config_element(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_step_decorator = BeforeStepDecorator(function)
        step = Mock()
        step.name = "title1"
        scenario_config = {"steps": [{"title": "title1", "description": "description1"},
                                     {"title": "title2", "description": "description2"}]}
        context = Mock(scenario_config=scenario_config)
        self.assertEqual(before_step_decorator.load_step_config_doc(context, step),
                         Step({"title": "title1", "description": "description1"}))

    @mock.patch('behave_django_autodoc.decorators.os.path.join')
    @mock.patch('behave_django_autodoc.decorators.HtmlBuilder.add_step')
    def test_call_when_step_screenshot_time_is_after(self, mock_add_step, mock_os_path_join):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_step_decorator = BeforeStepDecorator(function)
        step = Mock()
        step.name = "title1"
        scenario_config = {"steps": [{"title": "title1", "description": "description1", "screenshot_time": "after"},
                                     {"title": "title2", "description": "description2"}]}
        context = Mock(scenario_config=scenario_config)
        before_step_decorator(context, step)
        mock_add_step.assert_not_called()
        mock_os_path_join.assert_not_called()
        function.assert_called_once_with(context, step)

    @mock.patch('behave_django_autodoc.decorators.os.path.join')
    @mock.patch('behave_django_autodoc.decorators.HtmlBuilder.add_step')
    def test_call_when_step_screenshot_time_is_before(self, mock_add_step, mock_os_path_join):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        before_step_decorator = BeforeStepDecorator(function)
        step = Mock()
        step.name = "title1"
        scenario_config = {"steps": [{"title": "title1", "description": "description1",
                                      "screenshot_time": "before", "screenshot": False},
                                     {"title": "title2", "description": "description2"}]}
        context = Mock(scenario_config=scenario_config)
        before_step_decorator(context, step)
        step_config_doc = Step({"title": "title1", "description": "description1",
                               "screenshot_time": "before", "screenshot": False})
        context.html_doc_builder.add_step.assert_called_once_with(
            step_config_doc, before_step_decorator.images_dir, context)
        function.assert_called_once_with(context, step)


class TestAfterStepDecorator(unittest.TestCase):

    def test_load_step_config_element(self):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        after_step_decorator = AfterStepDecorator(function)
        step = Mock()
        step.name = "title1"
        scenario_config = {"steps": [{"title": "title1", "description": "description1"},
                                     {"title": "title2", "description": "description2"}]}
        context = Mock(scenario_config=scenario_config)
        self.assertEqual(after_step_decorator.load_step_config_doc(context, step),
                         Step({"title": "title1", "description": "description1"}))

    @mock.patch('behave_django_autodoc.decorators.os.path.join')
    @mock.patch('behave_django_autodoc.decorators.HtmlBuilder.add_step')
    def test_call_when_step_screenshot_time_is_before(self, mock_add_step, mock_os_path_join):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        after_step_decorator = AfterStepDecorator(function)
        step = Mock()
        step.name = "title1"
        scenario_config = {"steps": [{"title": "title1", "description": "description1", "screenshot_time": "before"},
                                     {"title": "title2", "description": "description2"}]}
        context = Mock(scenario_config=scenario_config)
        after_step_decorator(context, step)
        mock_add_step.assert_not_called()
        mock_os_path_join.assert_not_called()
        function.assert_called_once_with(context, step)

    @mock.patch('behave_django_autodoc.decorators.os.path.join')
    @mock.patch('behave_django_autodoc.decorators.HtmlBuilder.add_step')
    def test_call_when_step_screenshot_time_is_after(self, mock_add_step, mock_os_path_join):
        function = Mock(__globals__={"__file__": "dir/enviroment.py"})
        after_step_decorator = AfterStepDecorator(function)
        step = Mock()
        step.name = "title1"
        scenario_config = {"steps": [{"title": "title1", "description": "description1",
                                      "screenshot_time": "after", "screenshot": False},
                                     {"title": "title2", "description": "description2"}]}
        context = Mock(scenario_config=scenario_config)
        after_step_decorator(context, step)
        step_config_doc = Step({"title": "title1", "description": "description1",
                               "screenshot_time": "after", "screenshot": False})
        context.html_doc_builder.add_step.assert_called_once_with(step_config_doc,
                                                                  after_step_decorator.images_dir, context)
        function.assert_called_once_with(context, step)
