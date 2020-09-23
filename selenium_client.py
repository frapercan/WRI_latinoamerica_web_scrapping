from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumClient:
    def __init(self, driver_path):
        self.driver_path = driver_path
        self.browser = None

    def start(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

    def stop(self):
        self.browser = self.browser.quit()
