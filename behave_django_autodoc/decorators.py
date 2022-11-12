"""
Module containing decorators to environmental controls from behave.
"""
import os

from behave_django_autodoc.html_builder import HtmlBuilder


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
        """Return behave_django_autodoc directory path."""
        return os.path.join(os.path.dirname(self.function.__globals__["__file__"]), 'behave_django_autodoc')

    @property
    def docs_dir(self):
        """Return docs directory path."""
        return os.path.join(self.behave_django_autodoc_dir, 'docs')

    @property
    def features_configs_dir(self):
        """Return features_configs directory path."""
        return os.path.join(self.behave_django_autodoc_dir, 'features_configs')

    @property
    def images_dir(self):
        """Return images directory path."""
        return os.path.join(self.docs_dir, 'images')


class BeforeAllDecorator(BaseDecorator):
    """
    Decorator to be used in before_all function.
    """

    def __call__(self, context):
        """
        Call before_all function.
        create docs directory and initialize html documentation.
        fields:
            context: behave context
        """
        self.create_docs_dir()
        context.html_doc_builder = self.initialize_html_documentation()
        self.function(context)

    def create_docs_dir(self):
        """Create or replace docs directory."""
        os.makedirs(self.docs_dir, exist_ok=True)

    def initialize_html_documentation(self):
        """Initialize html documentation."""
        return HtmlBuilder()


class AfterAllDecorator(BaseDecorator):
    """
    Decorator to be used in after_all function.
    """

    def __call__(self, context):
        """
        Call after_all function.
        Save html documentation.
        fields:
            context: behave context
        """
        context.html_doc_builder.save(self.docs_dir)
        self.function(context)


class BeforeFeatureDecorator(BaseDecorator):
    """
    Decorator to be used in before_feature function.
    """

    def __call__(self, context, feature):
        """
        Call before_feature function.
        Add feature to html documentation.
        fields:
            context: behave context
            feature: behave feature
        """
        context.html_doc_builder.add_feature(feature)
        self.function(context, feature)

    def get_feature_config_path(self, feature):
        """Return feature config path."""
        feature_config_file = os.path.join(self.features_configs_dir, feature.filename.split('.')[0] + '.yaml')
        if not os.path.exists(feature_config_file):
            raise FileNotFoundError(f'Feature config file not found: {feature_config_file}')
        return feature_config_file
