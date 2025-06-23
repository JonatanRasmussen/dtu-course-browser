#%%

# These two imports will fix ssl.SSLCertVerificationError
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Imports
import time
import bs4 as bs
import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
# Helper functions and global constants
from utils import Utils
from website.global_constants.eval_consts import EvalConsts
from website.global_constants.file_name_consts import FileNameConsts
import json

def scrape_evaluations(course_numbers, file_name):
    """Scrape grades for a given set of courses and href digits"""

    def scrape_url(url):
        """ Get page source from url, split it at /n and return it as list.
            Note that this is some old and ugly code that I have not bothered to clean up"""
        # Load page source from url
        source = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(source,'lxml')
        scraped_html = ''
        # A string containing the 'Results' section of the web page is created
        for paragraph in soup.find_all(id='Results'):
            scraped_html = str(paragraph.text)
        # Stuff such as HTML was auto-removed, but further clean-up is needed
        scraped_html = scraped_html.replace("\r","")
        scraped_html = scraped_html.replace("            ","")
        # Converting the string to a list (split at every 'new line')
        scraped_html = scraped_html.split('\n')
        # Empty indexes in the list are removed
        scraped_html = list(filter(lambda a: a != '', scraped_html))
        return scraped_html

    def get_course_number_and_period(scraped_html):
        """ The scraped_html contains evaluations for an unknown season/period.
            The season/period can be Summer, Winter, F20, E20, Jan, Jun, Jul or Aug.
            Summer, Jun, Jul and Aug is converted to F20. Winter and Jan is converted to E20.
            Note that this is some old and ugly code that I have not bothered to clean up"""
        # First, we extract the course number and semester (evaluation period)
        course_number = scraped_html[0][13:18]
        if scraped_html[0][-4] == ' ': # Period format is F19 or E19
            course_period = scraped_html[0][-3:]
        elif (scraped_html[0][-6:-3]).upper() == 'JAN': # Period format is Jan 19
            # This evaluation belongs to the previous year:
            course_period = 'E'+str(int(scraped_html[0][-2:])-1)
        elif (scraped_html[0][-6:-4]).upper() == 'JU' or (scraped_html[0][-6:-4]).upper() == 'AU': # Period format is Jun 19 or Jul 19 or Aug 19
            course_period = 'F'+scraped_html[0][-2:]
        elif scraped_html[0][-8:-3] == 'inter': # Period format is Winter 19
            course_period = 'E'+scraped_html[0][-2:]
        elif scraped_html[0][-7:-3] == 'mmer': # Period format is Summer 19
            course_period = 'F'+scraped_html[0][-2:]
        else: # Period format is invalid
            message = f"{file_name}, {course_number}: Semester format unknown"
            Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
        return [course_number, course_period]

    def extract_evaluation_data(scraped_data, course_period):
        """ Extract evaluations from scrapedData and return them as dict
            Note that this is some old and ugly code that I have not bothered to clean up"""
        # In Sep-2019, the old evaluation questions were replaced by new ones
        # Data generated after Sep-2019 starts with 'Jeg synes, at…'
        if scraped_data[1] == 'Jeg synes, at…':
            age_of_evaluation_data = 'after Sep-2019'
        else:
            age_of_evaluation_data = 'before Sep-2019'

        # List of the phrases (questions) we'll search for in scrapedData
        lst_questions = []
        if age_of_evaluation_data == 'after Sep-2019':
            lst_questions.append('jeg har lært meget i dette kursus.')
            lst_questions.append('undervisningsaktiviteterne motiverer mig til at arbejde med stoffet.')
            lst_questions.append('jeg i løbet af kurset har haft mulighed for at få feedback på, hvordan jeg fagligt klarer mig på kurset.')
            lst_questions.append('Jeg mener, at den tid jeg har brugt på kurset er')
            answers_to_first_questions = 'Helt uenig'
            answers_to_last_questions = 'Meget mindre'

        else: # evaluationDate == 'before Sep-2019':
            lst_questions.append('Jeg synes, at jeg lærer meget i dette kursus')
            lst_questions.append('Jeg synes, at undervisningsmaterialet er godt')
            lst_questions.append('Jeg synes, at underviseren/underviserne i løbet af kurset har gjort det klart for mig, hvor jeg står fagligt set')
            lst_questions.append('5 point er normeret til 9t./uge (45 t./uge i treugers-perioden). Jeg mener, at min arbejdsindsats i kurset er')
            answers_to_first_questions = 'Helt enig'
            answers_to_last_questions = 'Meget mindre'

        # I have rephrased the questions as a single word (for the dict)
        lst_rephrased_questions = []
        lst_rephrased_questions.append(str(course_period)+'_'+EvalConsts.learning)
        lst_rephrased_questions.append(str(course_period)+'_'+EvalConsts.motivation)
        lst_rephrased_questions.append(str(course_period)+'_'+EvalConsts.feedback)
        lst_rephrased_questions.append(str(course_period)+'_'+EvalConsts.workload)

        eval_dict = {}
        # For each question, create a list containing the student responses
        for i in range (0, len(lst_questions)):
            eval_values = []

            # Student responses are located at specific indexes in scrapedData
            index_of_question = scraped_data.index(lst_questions[i])
            if age_of_evaluation_data == 'before Sep-2019':
                index_lst = [15, 11, 8, 5, 2, 18]
                if i == len(lst_questions)-1:
                    index_lst = [2, 5, 8, 11, 15, 18]
            else: # evaluationDate == 'after Sep-2019':
                index_lst = [2, 6, 10, 14, 18, 21]

            # Scrape value for student responses at the specific indexes
            for j in range (0, 5):
                eval_values.append(int(scraped_data[index_of_question+index_lst[j]]))
            # ^ This code only works if scrapedData has the expected format
            # The next two tests will return an error if the format is invalid

            # 1 of 2: Is question followed by 'Helt uenig' or 'Meget mindre?'
            if i == len(lst_questions)-1:
                expected_answer = answers_to_last_questions
            else:
                expected_answer = answers_to_first_questions
            if scraped_data[index_of_question+1] != expected_answer:
                message = f"{file_name}, {course}: {scraped_data[index_of_question+1]} != {expected_answer}, (i={i}) "
                Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
                return {} # Error
            # 2 of 2: Is sum of evalValues == 'x besvarelser' in scrapedData?
            try:
                response_count = int(str(scraped_data[index_of_question+index_lst[5]]).split(' ')[0])
                if sum(eval_values) != response_count and course != '01005': # 01005 is bugged for some reason
                    message = f"{file_name}, {course}: Data bugged: {sum(eval_values)} != {response_count} (i={i})"
                    # Sometimes the 'x besvarelser' is slightly off
                    if -2 <= sum(eval_values) - response_count <= 2:
                        Utils.logger(message, 'Warning', FileNameConsts.scrape_log_name)
                    else:
                        Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
                        return {} # Error
            except: # sum(eval_values) must not contain strings
                message = f"{file_name}, {course}: sum(evalValues) failed, (i={i}), {eval_values}"
                Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
                return {} # Error

            # Both tests were passed - Adding answers to dictionary
            eval_dict[lst_rephrased_questions[i]] = eval_values
        return eval_dict

    """
    def at_least_one_href_found(driver):
        hrefs = driver.find_elements(By.PARTIAL_LINK_TEXT, '')
        return any(href.get_attribute("href").startswith('https://evaluering.dtu.dk/kursus/') for href in hrefs)
    """

    def at_least_one_href_found(driver):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Get fresh elements each attempt
                hrefs = driver.find_elements(By.PARTIAL_LINK_TEXT, '')
                return any(
                    href.get_attribute("href") is not None and
                    href.get_attribute("href").startswith('https://evaluering.dtu.dk/kursus/')
                    for href in hrefs
                )
            except StaleElementReferenceException:
                if attempt < max_attempts - 1:
                    time.sleep(1.5)
                    continue
                else:
                    Utils.logger("StaleElement error", "Warning", FileNameConsts.scrape_log_name)
                    return False
        return False

    # Constants that specifies how Selenium can find the correct elements
    URL = 'https://evaluering.dtu.dk/CourseSearch'
    COURSE_INPUT = '//*[@id="CourseCodeTextbox"]'
    SEARCH_SUBMIT = '//*[@id="SearchButton"]'

    # Begin the webscrape and initialize the data frame
    df, lst_of_column_names, df_index = Utils.initialize_df(EvalConsts.list_of_evals)
    driver = Utils.launch_selenium()

    # Loop through all courses
    print('Webscrape of evaluations will now begin...')
    iteration_count = 0
    for course in course_numbers:
        df_row = {df_index: course}

        evaluation_urls = []
        driver.get(URL)
        driver.find_element(By.XPATH, COURSE_INPUT).send_keys(course)
        driver.find_element(By.XPATH, SEARCH_SUBMIT).click()

        timeout_after = 3 #seconds
        try:
            # Wait a small amount of time for at least one href link to be found
            WebDriverWait(driver, timeout_after).until(at_least_one_href_found)
        except TimeoutException:
            # If no href is found before timeout, log that no evaluation links exists
            Utils.logger(f"No evaluation links exists for course {course}", "Log", FileNameConsts.scrape_log_name)

        hrefs = driver.find_elements(By.PARTIAL_LINK_TEXT, '')
        for href in hrefs:
            href_as_string = href.get_attribute("href")
            if len(href_as_string) >= 33 and href_as_string[0:33] == 'https://evaluering.dtu.dk/kursus/':
                evaluation_urls.append(href_as_string)

        # Log the search page results
        Utils.logger(f"Search page for course {course}: Found {len(evaluation_urls)} evaluation links", "Log", FileNameConsts.scrape_log_name)

        # Loop through each evaluation for specified course
        for eval_url in evaluation_urls:
            page_source = scrape_url(eval_url)

            # Extract course number and course period from scraped data
            scraped_course_number, course_period = get_course_number_and_period(page_source)
            # Check that the extracted course number matches course[k]
            if scraped_course_number != course:
                message = f"{file_name}, {course_numbers[course]}: Wrong course number ({scraped_course_number})"
                Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
                continue

            # Extract student evaluation data from scrapedData
            semester_data = extract_evaluation_data(page_source, course_period)

            # Log the scraped data for each evaluation page
            Utils.logger(f"Scraped data for {eval_url}: Course: {scraped_course_number}, Period: {course_period}, Data: {json.dumps(semester_data)}", "Log", FileNameConsts.scrape_log_name)

            # If extraction failed, the returned dict will be empty
            df_row.update(semester_data)

        # Concatenate dict to dataframe as a new row
        df = Utils.add_dict_to_df(df_row, lst_of_column_names, df)

        # Print current course to console so user can track the progress
        iteration_count += 1
        if iteration_count % 10 == 0 or iteration_count == 1:
            Utils.print_progress(iteration_count, course_numbers, df_row, file_name)

    # Save all evaluations as df
    Utils.save_scraped_df(df, file_name)
    Utils.save_df_as_csv(df, file_name)

    # End of program
    driver.quit
    # Webscrape for all courses and semesters has been completed
    print()
    print('Webscrape of evaluations is now completed! Check log for details.')
    df.set_index(df_index, inplace=True, drop=True)
    print(f"Sample output: {df}")
    print()

#%%
if __name__ == "__main__":
    # Variables and initialization
    COURSE_NUMBERS = Utils.get_course_numbers()
    #COURSE_NUMBERS = ['01005', '02105']

    eval_df_name = FileNameConsts.eval_df
    scrape_evaluations(COURSE_NUMBERS, eval_df_name)