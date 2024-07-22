from selenium import webdriver
'''
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
'''
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


#https://sdb.dtu.dk/2023
class WebScrapingTool:
    """ Get page source from target url via Selenium Webdriver.
        This class is meant to be instantiated by the html-scraper
        class, which will carry out the scraping operation """

    def __init__(self: 'WebScrapingTool'):
        """ temp """
        self._driver: type[WebDriver] = None
        self._is_running: bool = False
        self._cache: dict[str, str] = {} #Cache is disabled due to not being used

    def _launch_webdriver(self) -> type[WebDriver]:
        """ Initialize selenium webdriver and return driver """
        service: type[Service] = Service(ChromeDriverManager().install())
        options: type[Options] = Options()
        options.add_argument("--log-level=3")
        options.add_argument('--disable-logging')
        driver: type[WebDriver] = webdriver.Chrome(service=service, options=options)
        return driver

    def _ensure_webdriver_is_running(self) -> None:
        """ Launch webdriver if it is not already running """
        if not self._is_running:
            self._driver = self._launch_webdriver()
            self._is_running = True

    def get_page_source(self: 'WebScrapingTool', url: str) -> str:
        """ Return the page source of the specified url """
        self._ensure_webdriver_is_running()
        if len(url) == 0:
            page_source: str = ""
        elif url in self._cache: # Check if page_source is cached locally from previous scrapes
            page_source: str = self._cache[url]
        else:
            page_source = self._scrape_page_source(url)
        return page_source

    def search_for_evaluation_hrefs(self: 'WebScrapingTool', course_id: str) -> str:
        """ Unique pagination required to obtain urls for Evaluation data """
        self._ensure_webdriver_is_running()
        driver: type[WebDriver] = self._driver
        URL = 'https://evaluering.dtu.dk/CourseSearch'
        SEARCH_INPUT_BOX = '//*[@id="CourseCodeTextbox"]'
        SEARCH_SUBMIT_BUTTON = '//*[@id="SearchButton"]'
        driver.get(URL)
        driver.find_element(By.XPATH, SEARCH_INPUT_BOX).send_keys(course_id)
        driver.find_element(By.XPATH, SEARCH_SUBMIT_BUTTON).click()
        page_source: str =  driver.page_source
        return page_source

    def _scrape_page_source(self: 'WebScrapingTool', url: str) -> str:
        """ Scrape and return the page source of the specified url """
        driver: type[WebDriver] = self._driver
        driver.get(url)
        page_source: str = driver.page_source
        self._cache_scraped_page_source(url, page_source)
        return page_source

    def _cache_scraped_page_source(self: 'WebScrapingTool', url: str, page_source: str) -> None:
        """ Cache the URL's page source for later use
            NOTE: Due to performance concerns, cache writes are disabled """
        #self._cache[url] = page_source

    def _terminate_webdriver(self: 'WebScrapingTool') -> None:
        """ Terminate an existing selenium webdriver """
        self._driver.quit()
        self._is_running = False


#%%

if __name__ == "__main__":
    # Test code, remove later
    my_scraping_tool = WebScrapingTool()
    source_a = my_scraping_tool.get_page_source("https://kurser.dtu.dk/archive/2019-2020/letter/A")
    source_b = my_scraping_tool.search_for_evaluation_hrefs('01005')
    my_scraping_tool.terminate_webdriver()
    print(len(source_a))
    print(len(source_b))