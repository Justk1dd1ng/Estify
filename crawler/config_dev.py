from platform import platform

from selenium.webdriver.chrome.options import Options


class Config:
    def __init__(self):
        self.platform = platform()
        self.crome_driver_options = Options()
        self.configure_chrome_options()

    def configure_chrome_options(self):
        self.crome_driver_options.headless = True
        if 'linux' in self.platform.lower():
            self.crome_driver_options.add_argument('--no-sandbox')
            self.crome_driver_options.add_argument('--disable-dev-shm-usage')


