#%%

# Imports
from io import StringIO
import time
import pandas as pd
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# Helper functions and global constants
from utils import Utils
from website.global_constants.config import Config
from website.global_constants.dtu_consts import DtuConsts
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts


class InfoScraper:

    @staticmethod
    def quick_test_scrape_for_debugging_please_ignore():
        """ Do a quick scrape to see if the code works."""
        course_numbers = ['01001', '02402']  # Example of valid courses for the below semesters
        academic_year = '2023-2024'  # Example of valid academic year
        file_name = "scraped_info_test"
        InfoScraper.scrape_info(course_numbers, academic_year, file_name)

    @staticmethod
    def scrape_info(course_numbers, academic_year, file_name):
        """Scrape DTU Course Base for course info such as language, schedule, ects, learning objectives etc."""
        print(f'Webscrape of info will now begin for academic year {academic_year}...')
        df_index = FileNameConsts.df_index  # Begin the webscrape and initialize the data frame
        df_columns = {}
        lst_of_column_names = [df_index] + InfoConsts.scrape_info_column_names
        for column_name in lst_of_column_names:
            df_columns[column_name] = []
        df = pd.DataFrame(data = df_columns)

        iteration_count = 0
        for course in course_numbers:
            df_row = {df_index: course}
            # Scrape all info inside and outside the dataframe found on the webpage
            page_source_1 = InfoScraper._fetch_course_info_page_source(course, academic_year, file_name)
            df_row.update(InfoScraper._parse_primary_df(page_source_1, course, academic_year, file_name))  #  Parse all info located inside the dataframe
            df_row.update(InfoScraper._parse_info_not_in_primary_df(page_source_1, course, file_name))  #  Parse all info located outside the dataframe
            page_source_2 = InfoScraper._fetch_course_responsible_page_source(course, file_name)
            df_row.update(InfoScraper._scrape_course_responsibles(page_source_2))  #  Parse all info related to teachers and course responsibles
            df = Utils.add_dict_to_df(df_row, lst_of_column_names, df)  # Concatenate dict to dataframe as a new row
            iteration_count += 1  # Print current course to console so user can track the progress
            if iteration_count % 50 == 0 or iteration_count == 1:
                Utils.print_progress(iteration_count, course_numbers, df_row, file_name)
        if len(file_name) != 0:
            Utils.save_scraped_df(df, file_name)  # Save all grades as .pkl
            Utils.save_df_as_csv(df, file_name)  # Save all grades as .csv
        print()  # Webscrape for all courses have been completed
        print('Webscrape of info is now completed! Check log for details.')
        df.set_index(df_index, inplace=True, drop=True)
        print(f"Sample output: {df}")
        print()
        return df

    @staticmethod
    def _fetch_course_info_page_source(course, academic_year, file_name):
        """Open course's info page with a session to handle cookies."""
        # Scrape all info inside and outside the dataframe found on the webpage
        try:
            url = f'https://kurser.dtu.dk/course/{academic_year}/{course}'
            # The first request "primes" the session and gets the necessary cookie.
            # The server returns the JS reload page, which we can ignore.
            session = requests.Session()  # Initialize a single Session object for the entire scrape
            session.get(url, timeout=10, headers={"Accept-Language": "en"})
            # The second request sends the cookie back, and the server returns the real content.
            response = session.get(url, timeout=10, headers={"Accept-Language": "en"})
            response.raise_for_status()
            page_source = response.text
        except ImportError:
            message = f"{file_name}, {course}: Missing import / pipinstall for parsing html"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
            page_source = ""
        except requests.exceptions.RequestException:
            message = f"{file_name}, {course}: Timeout when loading URL"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
            page_source = ""
        return page_source

    @staticmethod
    def _fetch_course_responsible_page_source(course, file_name):
        """Open course's info page with a session to handle cookies."""
        # Scrape course responsibles page source
        try:
            url = f'https://kurser.dtu.dk/course/{course}/info'
            # Same two-step process as in get_course_info_page_source()
            session = requests.Session()  # Initialize a single Session object for the entire scrape
            session.get(url, timeout=10, headers={"Accept-Language": "en"})
            response = session.get(url, timeout=10, headers={"Accept-Language": "en"})
            response.raise_for_status()
            print(response.text)
            return response.text
        except requests.exceptions.RequestException:
            message = f"{file_name}, {course}: Timeout when loading URL for course responsibles"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
            return ""

    @staticmethod
    def _parse_primary_df(page_source, course, academic_year, file_name):
        """Format the info inside the 'Course information' dataframe into a dict"""
        primary_info_dct = {}
        if len(page_source) == 0:
            return primary_info_dct
        try:
            html_io = StringIO(page_source)
            html_df = pd.read_html(html_io)
        except ValueError:
            message = f"{file_name}, {course}: missing df in page_source, ensure {course} exists in {academic_year}"
            Utils.logger(message, 'Warning', FileNameConsts.scrape_log_name)
            return primary_info_dct
        if len(html_df) != 3:  # The current version of the dtu website contains a df of length 3
            message = f"{file_name}, {course}: len(df) is {str(len(html_df))} instead of 3"
            Utils.logger(message, 'Warning', FileNameConsts.scrape_log_name)
        else:
            df_0 = html_df[0].copy(deep=True)
            df_1 = html_df[1].copy(deep=True)
            df_2 = html_df[2].copy(deep=True)
            df = pd.concat([df_0, df_1, df_2], axis=0, ignore_index=True)
            df.columns=['key', 'value']
            df = df.set_index('key')
            df = df.iloc[:,0]
            primary_info_dct = df.to_dict()
        return primary_info_dct

    @staticmethod
    def _parse_info_not_in_primary_df(page_source, course, file_name):
        """ Format the info outside the 'Course information' dataframe into a dict"""
        secondary_info_dct = {}
        if len(page_source) == 0:
            return secondary_info_dct

        # Scrape study lines
        start = 'var lines = '
        end = ";" #var collectedTooltips = {};"    # SOMETIMES <br />
        study_lines = InfoScraper._parse_from_page_source(page_source, start, end)
        if study_lines:
            secondary_info_dct[DtuConsts.dtu_accosiated_study_lines] = study_lines
        else:
            message = f"{file_name}, {course}: Error when splitting page_source at {start}"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape last updated
        start = f'{DtuConsts.dtu_last_updated}</div> '
        end = '<'
        last_updated = InfoScraper._parse_from_page_source(page_source, start, end)
        if last_updated:
            secondary_info_dct[DtuConsts.dtu_last_updated] = last_updated
        else:
            message = f"{file_name}, {course}: Error when splitting page_source at {start}"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape General course objectives
        start = f'{DtuConsts.dtu_general_course_objectives}</div> '
        end = '<div class='
        course_objectives = InfoScraper._parse_from_page_source(page_source, start, end)
        if course_objectives:
            secondary_info_dct[DtuConsts.dtu_general_course_objectives] = course_objectives
        else:
            message = f"{file_name}, {course}: Error when splitting page_source at {start}"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape Learning objectives
        start = f'{DtuConsts.dtu_learning_objectives}</div> '
        end = '<div class='
        learning_objectives = InfoScraper._parse_from_page_source(page_source, start, end)
        if learning_objectives:
            secondary_info_dct[DtuConsts.dtu_learning_objectives] = learning_objectives
        else:
            message = f"{file_name}, {course}: Error when splitting page_source at {start}"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape course content
        start = f'>{DtuConsts.dtu_content}</div> '
        end = '<div class='
        course_content = InfoScraper._parse_from_page_source(page_source, start, end)
        if course_content:
            secondary_info_dct[DtuConsts.dtu_content] = course_content
        else:
            message = f"{file_name}, {course}: Error when splitting page_source at {start}"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape course remarks
        start = f'>{DtuConsts.dtu_remarks}</div> '
        end = '<div class='
        course_remarks = InfoScraper._parse_from_page_source(page_source, start, end)
        if not course_remarks:
            course_remarks = DtuConsts.dtu_no_remarks
        secondary_info_dct[DtuConsts.dtu_remarks] = course_remarks

        # Scrape highlighted message (this is the optional "red text" at the top of the page)
        start = '<div class="row"><div class="col-xs-12">'
        end = '<'
        highlighted_message = InfoScraper._parse_from_page_source(page_source, start, end)
        if not highlighted_message:
            highlighted_message = DtuConsts.dtu_no_highlighted_message
        secondary_info_dct[DtuConsts.dtu_highlighted_message] = highlighted_message
        return secondary_info_dct

    @staticmethod
    def _scrape_course_responsibles(page_source_responsibles):
        df_row = {}
        # Scrape main responsible
        responsibles_lst = page_source_responsibles.split('<div class="row" style="margin:20px">')
        main_name, main_pic = InfoScraper._get_name_and_pic_from_page_source(responsibles_lst, 1)
        df_row[DtuConsts.dtu_name_of_main_responsible] = main_name
        df_row[DtuConsts.dtu_pic_of_main_responsible] = main_pic
        co_1_name, co_1_pic = InfoScraper._get_name_and_pic_from_page_source(responsibles_lst, 2)
        df_row[DtuConsts.dtu_name_of_co_responsible_1] = co_1_name
        df_row[DtuConsts.dtu_pic_of_co_responsible_1] = co_1_pic
        co_2_name, co_2_pic = InfoScraper._get_name_and_pic_from_page_source(responsibles_lst, 3)
        df_row[DtuConsts.dtu_name_of_co_responsible_2] = co_2_name
        df_row[DtuConsts.dtu_pic_of_co_responsible_2] = co_2_pic
        co_3_name, co_3_pic = InfoScraper._get_name_and_pic_from_page_source(responsibles_lst, 4)
        df_row[DtuConsts.dtu_name_of_co_responsible_3] = co_3_name
        df_row[DtuConsts.dtu_pic_of_co_responsible_3] = co_3_pic
        co_4_name, co_4_pic = InfoScraper._get_name_and_pic_from_page_source(responsibles_lst, 5)
        df_row[DtuConsts.dtu_name_of_co_responsible_4] = co_4_name
        df_row[DtuConsts.dtu_pic_of_co_responsible_4] = co_4_pic
        return df_row


    @staticmethod
    def _parse_from_page_source(page_source, start, end):
        """Return study lines associated with a course from page_source"""
        # Split the page source and the start and end of study lines string
        page_source = page_source.replace("\r"," ")
        page_source = page_source.replace("\n"," ")
        page_source = page_source.replace("    ","")
        page_source = page_source.replace("   "," ")
        page_source = page_source.replace("  "," ")
        page_source = page_source.replace("<ul><li>","<br />- ")
        page_source = page_source.replace("</li><li>","<br />- ")
        if start in page_source:
            start = page_source.split(start)
            end = start[1].split(end)
            string = end[0]
            return string
        return ""

    @staticmethod
    def _get_name_and_pic_from_page_source(responsibles_lst, course_responsible_number):
        """Return name and image-link of course responsible"""
        responsible_name = DtuConsts.dtu_no_data_for_responsible
        responsible_pic = DtuConsts.dtu_no_data_for_responsible
        if len(responsibles_lst) > course_responsible_number:
            responsible_source = responsibles_lst[course_responsible_number]
            name_start = '<b>'
            name_end = '</b>'
            responsible_name = InfoScraper._parse_from_page_source(responsible_source, name_start, name_end)
            pic_start = '<img src="'
            pic_end = '"'
            responsible_pic = InfoScraper._parse_from_page_source(responsible_source, pic_start, pic_end)
        return (responsible_name, responsible_pic)


#%%
if __name__ == "__main__":
    InfoScraper.quick_test_scrape_for_debugging_please_ignore()
