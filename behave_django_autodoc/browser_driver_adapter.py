# -*- coding: utf-8 -*-
import base64
from abc import ABC
from abc import abstractmethod


class UnkownBrowserDriverException(Exception):
    """Exception raised when the browser driver is not supported"""


class BrowserDriver(object):
    """
    Factory class for browser drivers. It returns the correct driver for the browser,
    based on the browser module name
    """

    def __new__(cls, browser):
        if browser.__module__.startswith("selenium"):
            return BrowserDriverSelenium(browser)
        elif browser.__module__.startswith("splinter"):
            return BrowserDriverSplinter(browser)
        raise UnkownBrowserDriverException(
            f"Unknown browser driver from module: {browser.__module__}"
        )


class BrowserDriverBase(ABC):
    """
    Abstract class for browser drivers. It defines the methods that must be implemented
    """

    def __init__(self, browser) -> None:
        self.browser = browser

    @abstractmethod
    def take_screenshot(self, filename):
        pass

    @abstractmethod
    def execute_script(self, script):
        pass

    @abstractmethod
    def scroll_to_by_css(self, css_selector):
        pass


class BrowserDriverSelenium(BrowserDriverBase):
    """Browser driver for Selenium"""

    def take_screenshot(self, filename):
        self.browser.get_screenshot(filename)
        return 'data:image/jpeg;base64,' + base64.b64encode(open(filename, 'rb').read()).decode()

    def execute_script(self, script):
        self.browser.execute_script(script)

    def scroll_to_by_css(self, css_selector):
        self.browser.execute_script(
            f'document.querySelector("{css_selector}").scrollIntoView()'
        )


class BrowserDriverSplinter(BrowserDriverBase):
    """Browser driver for Splinter"""

    def take_screenshot(self, filename):
        filename = self.browser.screenshot(filename)
        return 'data:image/jpeg;base64,' + base64.b64encode(open(filename, 'rb').read()).decode()

    def execute_script(self, script):
        self.browser.execute_script(script)

    def scroll_to_by_css(self, css_selector):
        self.browser.execute_script(
            f'document.querySelector("{css_selector}").scrollIntoView()'
        )
