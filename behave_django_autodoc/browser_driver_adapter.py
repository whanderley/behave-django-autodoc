# -*- coding: utf-8 -*-
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


class BrowserDriverSelenium:
    """Browser driver for Selenium"""

    def __init__(self, browser) -> None:
        self.browser = browser

    def get_screenshot(self, filename):
        self.browser.get_screenshot(filename)

    def execute_script(self, script):
        self.browser.execute_script(script)

    def scroll_to_by_css(self, css_selector):
        self.browser.execute_script(
            f'document.querySelector("{css_selector}").scrollIntoView()'
        )


class BrowserDriverSplinter:
    """Browser driver for Splinter"""

    def __init__(self, browser) -> None:
        self.browser = browser

    def get_screenshot(self, filename):
        self.browser.screenshot(filename)

    def execute_script(self, script):
        self.browser.execute_script(script)

    def scroll_to_by_css(self, css_selector):
        self.browser.execute_script(
            f'document.querySelector("{css_selector}").scrollIntoView()'
        )
