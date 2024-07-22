from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class LoadWebpage:

    def launch_selenium_webdriver():
        """Initialize selenium webdriver and return driver"""
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument('--disable-logging')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        #driver = webdriver.Chrome(PATH, options=options)
        return driver

    def access_url_via_selenium(url, driver):
        """Return page source from url. Return an empty string if 10-second timeout"""
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "viewport")))
            page_source = driver.page_source
            return page_source
        except TimeoutException:
            message = f"{''}, Timeout exception at url: {url}"
            LoadWebpage.log(message, 'Error', '')
            empty_string = ''
            return None

    def access_url_with_selenium_webdriver():
        pass

    def return_page_source_as_string():
        pass

    def log(a, b, c):
        pass

