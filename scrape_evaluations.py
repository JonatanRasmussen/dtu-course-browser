#%%

import time
import bs4 as bs
import urllib.request
import requests
from requests.exceptions import Timeout, RequestException

from utils import Utils
from website.global_constants.config import Config
from website.global_constants.eval_consts import EvalConsts
from website.global_constants.file_name_consts import FileNameConsts
import json


class EvalScraper:

    @staticmethod
    def quick_test_scrape_for_debugging_please_ignore():
        """ Do a quick scrape to see if the code works."""
        course_numbers = ['01001', '02402']  # Example of valid courses for the below semesters
        course_semesters = ['F23', 'E23', 'F24']  # Example of valid semesters
        file_name = "scraped_evals_test"
        EvalScraper.scrape_evaluations(course_numbers, course_semesters, file_name)

    @staticmethod
    def scrape_evaluations(course_numbers, course_semesters, file_name):
        """Scrape grades for a given set of courses and href digits"""
        print('Webscrape of evaluations will now begin...')
        df, lst_of_column_names, df_index = Utils.initialize_df(course_semesters, EvalConsts.list_of_evals)
        iteration_count = 0
        for course in course_numbers:
            df_row = {df_index: course}
            search_page_source = EvalScraper._search_for_eval_urls(course, file_name, False)
            evaluation_urls = EvalScraper._parse_eval_urls(search_page_source, course, file_name)
            for semester in course_semesters:
                if semester in evaluation_urls:
                    evaluation_url = evaluation_urls[semester]
                    if evaluation_url != "":  # This is the intended behavior and works 99.9% of the time.
                        uncut_source = urllib.request.urlopen(evaluation_url).read()
                        page_source = EvalScraper._format_eval_page_source(uncut_source)
                    else:  # Very rarely, _parse_eval_urls will return a dict key with an empty string as value
                        page_source = EvalScraper._format_eval_page_source(search_page_source)  # Edge case for search page being a redirect to the eval page if exactly 1 search result is returned
                    semester_eval_data = EvalScraper._extract_evaluation_data(page_source, semester, course, file_name)
                    df_row.update(semester_eval_data)  # If extraction failed, the returned dict will be empty
            df = Utils.add_dict_to_df(df_row, lst_of_column_names, df)  # Concatenate dict to dataframe as a new row
            iteration_count += 1  # Print current course to console so user can track the progress
            if iteration_count % 50 == 0 or iteration_count == 1 or iteration_count == 2 or iteration_count == 5 or iteration_count == 10:
                Utils.print_progress(iteration_count, course_numbers, df_row, file_name)
        if len(file_name) != 0:
            Utils.save_scraped_df(df, file_name)  # Save all grades as .pkl
            Utils.save_df_as_csv(df, file_name)  # Save all grades as .csv
        print()  # Webscrape for all courses and semesters has been completed
        print('Webscrape of evaluations is now completed! Check log for details.')
        df.set_index(df_index, inplace=True, drop=True)
        print(f"Sample output: {df}")
        print()
        return df

    @staticmethod
    def _search_for_eval_urls(course, file_name, is_timeout):
        """Search for all evaluations for a given course and return the page source"""
        # Scrape page source of course info, as this page contain links to the 5 most recent evaluations
        try:
            search_url = "https://evaluering.dtu.dk/CourseSearch"
            payload = {'courseNumber': course, 'termUid': "", 'SearchButton': 'Søg'} # 'Søg' is the value of the submit button
            session = requests.Session()
            response = session.post(search_url, data=payload, timeout=10, headers={"Accept-Language": "en"})
            response.raise_for_status() # Raise an error for bad status codes (like 404 or 500)
            return response.text
        except requests.exceptions.RequestException:
            if not is_timeout:  # Try one more time
                return EvalScraper._search_for_eval_urls(course, file_name, True)
            message = f"{file_name}, {course}: Timeout when loading URL for course responsibles"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
            return ""

    @staticmethod
    def _parse_eval_urls(page_source, course, file_name):
        """Parse out all evaluation urls from search page source. If page source"""
        # Searching for urls works a bit odd. If the search only returns a single evaluation...
        # ...rather than displaying it as a list with a single element, it instead takes you
        # directly to its evaluation page. We must counteract this somehow
        href_urls = {}
        lst_of_split_html = page_source.split('href="/kursus/')
        if len(lst_of_split_html) >= 2:  # There are 2 or more evaluation urls for our search
            for split_html in lst_of_split_html:
                potential_href = split_html[6:12]
                if potential_href.isdigit():
                    url_with_href_digits = f"https://evaluering.dtu.dk/kursus/{course}/{split_html[6:12]}"
                    term_part = split_html.split('<div class="Term">')[1]
                    term = term_part.split('</div>')[0].strip()
                    if (term[0] == 'F' or term[0] == 'E') and term[2:4].isdigit():
                        formatted_term = f"{term[0]}{term[2:4]}"
                        href_urls[formatted_term] = url_with_href_digits
            return href_urls
        elif "Ingen kurser matchede s" in page_source:  #  There are 0 evaluation urls for our search
            pass
        elif "Der er 6 undervisningsperioder:" in page_source:  # There is 1 evaluation url in search and it seems we got redirected to it
            formatted_page_source = EvalScraper._format_eval_page_source(page_source)
            parsed_term = EvalScraper._parse_semester_from_page_source(formatted_page_source, course, file_name)
            href_urls[parsed_term] = ""
        else:
            message = f"{file_name}, {course}: Eval urls could not be parsed for ({course})"
            Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
        return href_urls



    @staticmethod
    def _format_eval_page_source(page_source):
        """ Get page source from url, split it at /n and return it as list.
            Note that this is some old and ugly code that I have not bothered to clean up"""
        # Load page source from url
        soup = bs.BeautifulSoup(page_source,'lxml')
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

    @staticmethod
    def _parse_semester_from_page_source(scraped_html, expected_course, file_name):
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
            course_period = 'X00'
        if course_number != expected_course:  # Check that the extracted course number matches course[k]
            message = f"{file_name}, {expected_course}: Wrong course number ({course_number})"
            Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
        return course_period

    @staticmethod
    def _extract_evaluation_data(scraped_data, semester, course, file_name):
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
        lst_rephrased_questions.append(str(semester)+'_'+EvalConsts.learning)
        lst_rephrased_questions.append(str(semester)+'_'+EvalConsts.motivation)
        lst_rephrased_questions.append(str(semester)+'_'+EvalConsts.feedback)
        lst_rephrased_questions.append(str(semester)+'_'+EvalConsts.workload)

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
                response_count = int(str(scraped_data[index_of_question+index_lst[5]]).split(' ', maxsplit=1)[0])
                if sum(eval_values) != response_count and course != '01005': # 01005 is bugged for some reason
                    message = f"{file_name}, {course}: Data bugged: {sum(eval_values)} != {response_count} (i={i})"
                    # Sometimes the 'x besvarelser' is slightly off
                    if -2 <= sum(eval_values) - response_count <= 2:
                        Utils.logger(message, 'Warning', FileNameConsts.scrape_log_name)
                    else:
                        Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
                        return {} # Error
            except (ValueError, TypeError, IndexError): # sum(eval_values) must not contain strings
                message = f"{file_name}, {course}: sum(evalValues) failed, (i={i}), {eval_values}"
                Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
                return {} # Error

            # Both tests were passed - Adding answers to dictionary
            eval_dict[lst_rephrased_questions[i]] = eval_values
        message = f"Scraped data for Course: {course} in term {semester}, Data: {json.dumps(eval_dict)}"
        Utils.logger(message, "Log", FileNameConsts.scrape_log_name)  # Log the scraped data for each evaluation page
        return eval_dict

#%%
if __name__ == "__main__":
    EvalScraper.quick_test_scrape_for_debugging_please_ignore()
