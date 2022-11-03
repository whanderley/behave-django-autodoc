class UnkownBrowserDriverException(Exception):
    pass


class BrowserDriver(object):
    
    def __new__(cls, browser):
        if browser.__module__.startswith('selenium'):
            return BrowserDriverSelenium(browser)
        elif browser.__module__.startswith('splinter'):
            return BrowserDriverSplinter(browser)
        raise UnkownBrowserDriverException('Unknown browser driver from module: %s' % browser.__module__)
    

class BrowserDriverSelenium():
    
    def __init__(self, browser) -> None:
        self.browser = browser
        
    def get_screenshot(self, filename):
        self.browser.get_screenshot(filename)
        
    def execute_script(self, script):
        self.browser.execute_script(script)
        
    def scroll_to_by_css(self, css_selector):
        self.browser.execute_script('document.querySelector("%s").scrollIntoView()' % css_selector)

class BrowserDriverSplinter():
    
    def __init__(self, browser) -> None:
        self.browser = browser
        
    def get_screenshot(self, filename):
        self.browser.screenshot(filename)
        
    def execute_script(self, script):
        self.browser.execute_script(script)
        
    def scroll_to_by_css(self, css_selector):
        self.browser.execute_script('document.querySelector("%s").scrollIntoView()' % css_selector)