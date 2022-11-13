# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock

from behave_django_autodoc.browser_driver_adapter import BrowserDriver
from behave_django_autodoc.browser_driver_adapter import UnkownBrowserDriverException


class TestBrowserDriverAdapter(unittest.TestCase):

    def test_selenium_browser_driver_adapter(self):
        browser = Mock(__module__="selenium.webdriver.firefox.webdriver")
        browser_driver = BrowserDriver(browser)
        self.assertEqual(browser_driver.__class__.__name__, "BrowserDriverSelenium")

    def test_splinter_browser_driver_adapter(self):
        browser = Mock(__module__="splinter.driver.webdriver.firefox")
        browser_driver = BrowserDriver(browser)
        self.assertEqual(browser_driver.__class__.__name__, "BrowserDriverSplinter")

    def test_unknown_browser_driver_adapter(self):
        browser = Mock(__module__="unknown")
        with self.assertRaises(UnkownBrowserDriverException):
            BrowserDriver(browser)


class TestBrowserDriverSelenium(unittest.TestCase):

    def test_init(self):
        browser = Mock(__module__="selenium.webdriver.firefox.webdriver")
        browser_driver = BrowserDriver(browser)
        self.assertEqual(browser_driver.browser, browser)

    @unittest.mock.patch("behave_django_autodoc.browser_driver_adapter.base64")
    @unittest.mock.patch("behave_django_autodoc.browser_driver_adapter.open")
    def test_take_screenshot(self, mock_open, mock_base64):
        browser = Mock(__module__="selenium.webdriver.firefox.webdriver")
        browser.get_screenshot = MagicMock(return_value=True)
        browser_driver = BrowserDriver(browser)
        mock_open.return_value.read.return_value = b"test"
        mock_base64.b64encode.return_value.decode.return_value = "test"
        self.assertEqual('data:image/jpeg;base64,test', browser_driver.take_screenshot("test.jpg"))
        browser.get_screenshot.assert_called_once_with("test.jpg")

    def test_execute_script(self):
        browser = Mock(__module__="selenium.webdriver.firefox.webdriver")
        browser.execute_script = MagicMock(return_value=True)
        browser_driver = BrowserDriver(browser)
        browser_driver.execute_script('alert("test")')
        browser.execute_script.assert_called_once_with('alert("test")')

    def test_scroll_to_by_css(self):
        browser = Mock(__module__="selenium.webdriver.firefox.webdriver")
        browser.execute_script = MagicMock(return_value=True)
        browser_driver = BrowserDriver(browser)
        browser_driver.scroll_to_by_css("#id")
        browser.execute_script.assert_called_once_with(
            'document.querySelector("#id").scrollIntoView()'
        )


class TestBrowserDriverSplinter(unittest.TestCase):

    def test_init(self):
        browser = Mock(__module__="splinter.driver.webdriver.firefox")
        browser_driver = BrowserDriver(browser)
        self.assertEqual(browser_driver.browser, browser)

    @unittest.mock.patch("behave_django_autodoc.browser_driver_adapter.base64")
    @unittest.mock.patch("behave_django_autodoc.browser_driver_adapter.open")
    def test_take_screenshot(self, mock_open, mock_base64):
        browser = Mock(__module__="splinter.driver.webdriver.firefox")
        browser.screenshot = MagicMock(return_value=True)
        browser_driver = BrowserDriver(browser)
        mock_open.return_value.read.return_value = b"test"
        mock_base64.b64encode.return_value.decode.return_value = "test"
        self.assertEqual('data:image/jpeg;base64,test', browser_driver.take_screenshot("test.jpg"))
        browser.screenshot.assert_called_once_with("test.jpg")

    def test_execute_script(self):
        browser = Mock(__module__="splinter.driver.webdriver.firefox")
        browser.execute_script = MagicMock(return_value=True)
        browser_driver = BrowserDriver(browser)
        browser_driver.execute_script('alert("test")')
        browser.execute_script.assert_called_once_with('alert("test")')

    def test_scroll_to_by_css(self):
        browser = Mock(__module__="splinter.driver.webdriver.firefox")
        browser.execute_script = MagicMock(return_value=True)
        browser_driver = BrowserDriver(browser)
        browser_driver.scroll_to_by_css("#id")
        browser.execute_script.assert_called_once_with(
            'document.querySelector("#id").scrollIntoView()'
        )
