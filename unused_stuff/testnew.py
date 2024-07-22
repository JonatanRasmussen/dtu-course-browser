
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# This import will fix ssl.SSLCertVerificationError
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# IF CHROMEDRIVER COMPLAINS ABOUT INCORRECT INSTALL VERSION,
# GO TO https://chromedriver.chromium.org/downloads
# AND PLACE NEW VERSION IN C:\Program Files (x86)\ChromeDriver

def launch_selenium():
    """Initialize selenium webdriver and return driver"""
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument('--disable-logging')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Launch selenium-driver and access url.
driver = launch_selenium()
url = 'https://evaluering.dtu.dk/CourseSearch'
driver.get(url)

# (OPTIONAL) Wait up to 10 seconds for page to load, otherwise return a timeout error
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "viewport")))
except:
    html_page_source = 'Error: Webpage failed to load and timed out after 10 seconds'

# Locate search box on the webpage of the url and input the search term
course_input = '//*[@id="CourseCodeTextbox"]'
my_searchbox_input = "01005"
driver.find_element(By.XPATH, course_input).send_keys(my_searchbox_input)

# Click the search button and return the html_page_source
search_submit = '//*[@id="SearchButton"]'
driver.find_element(By.XPATH, search_submit).click()
html_page_source = driver.page_source

# On the html_page_source, locate all href links starting with "https://evaluering.dtu.dk/kursus/"
elems = driver.find_elements(By.PARTIAL_LINK_TEXT, '')
evaluation_urls = []
for elem in elems:
    href = elem.get_attribute("href")
    if len(href) >= 33 and href[0:33] == 'https://evaluering.dtu.dk/kursus/':
        evaluation_urls.append(href)
        print(href)