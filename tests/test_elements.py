# -*- coding: utf-8 -*-
import unittest
from behave_django_autodoc.elements import Feature


class TestFeature(unittest.TestCase):

    def test_init(self):
        feature = Feature({'tittle': 'test tittle', 'description': 'test description'})
        self.assertEqual(feature.tittle, 'test tittle')
        self.assertEqual(feature.description, 'test description')

    def test_init_with_empty_description(self):
        feature = Feature({'tittle': 'test tittle'})
        self.assertEqual(feature.tittle, 'test tittle')
        self.assertEqual(feature.description, None)
