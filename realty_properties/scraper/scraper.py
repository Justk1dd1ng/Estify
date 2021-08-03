from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class Driver:
    def __init__(self):
        self.options = Options()
        self.chrome = webdriver.Chrome(ChromeDriverManager().install())