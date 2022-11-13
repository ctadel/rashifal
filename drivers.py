from selenium import webdriver

from conf import settings

class WebDriver:
    def __init__(self):
        self.browser = WebDriver.get_driver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.quit()

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        if settings.PRODUCTION:
            options.add_argument('headless')
        driver = webdriver.Chrome(executable_path = settings.CHROME_BINARY, options = options)
        return driver

