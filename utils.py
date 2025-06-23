
#%%
# Imports
import logging
import os
import json
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Helper functions and global constants
from website.global_constants.config import Config
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.dtu_consts import DtuConsts

class Utils:
    """A collection of various functions that are used across the project"""

    @staticmethod
    def replace_spaces_in_dict_keys(dct):
        replace = True
        dct_no_spaces = {k.replace(" ","_") if replace else k:v for k,v in dct.items()}
        return dct_no_spaces

    @staticmethod
    def replace_commas_in_dict_keys(dct):
        replace = True
        dct_no_commas = {k.replace(",","-") if replace else k:v for k,v in dct.items()}
        return dct_no_commas

    @staticmethod
    def replace_special_characters_in_dict_keys(dct):
        dct = Utils.replace_spaces_in_dict_keys(dct)
        dct = Utils.replace_commas_in_dict_keys(dct)
        return dct

    @staticmethod
    def launch_selenium():
        """Initialize selenium webdriver and return driver"""
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install(), log_path=os.devnull)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    @staticmethod
    def access_url_via_selenium(url, driver):
        """Return page source from url. Return an empty string if 10-second timeout"""
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "viewport")))
            page_source = driver.page_source
            return page_source
        except TimeoutException:
            message = f"{FileNameConsts.scrape_log_name}, Timeout exception at url: {url}"
            Utils.logger(message, 'Error', FileNameConsts.scrape_log_name)
            empty_string = ''
            return empty_string

    @staticmethod
    def access_url_via_requests_get(url):
        """Return page source from url."""
        response = requests.get(url, timeout=10)
        page_source = response.text
        return page_source

    @staticmethod
    def generate_columns(semesters, elements, add_index = True):
        """ Given x elements and y semesters, 'concatenate' all x*y combinations, i.e.:
            df_index, sem1_elem1, sem2_elem1, sem1_elem1, sem2_elem2, etc. """
        combined_list = [FileNameConsts.df_index]
        if add_index is False:
            combined_list = []
        for element in elements:
            for semester in semesters:
                combined_list.append(semester+'_'+element)
        return combined_list

    @staticmethod
    def initialize_df(semesters, list_of_possible_elements):
        """Create empty pandas data frame with given column names and 0 rows"""
        df_index = FileNameConsts.df_index
        lst_of_column_names = Utils.generate_columns(semesters, list_of_possible_elements)
        df_columns = {}
        for column_name in lst_of_column_names:
            df_columns[column_name] = []
        df = pd.DataFrame(data = df_columns)
        return [df, lst_of_column_names, df_index]

    @staticmethod
    def extract_unique_year_ranges(semesters):
        """Convert a list of semesters like ['E23', 'F24', 'E24'] into a list of academic years like ['2023-2024', '2024-2025']."""
        if isinstance(semesters, str):
            semesters = [semesters]
        year_ranges = set()
        for semester in semesters:
            year_range = Utils.extract_year_range_from_semester(semester)
            year_ranges.add(year_range)
        return sorted(year_ranges)  # sorted for consistency

    @staticmethod
    def extract_year_range_from_semester(semester):
        """Convert a single semester such as 'E23' into its corresponding academic year, such as '2023-2024'."""
        term_code = semester[0]
        year_suffix = int(semester[1:])
        year = 2000 + year_suffix
        if term_code == 'E':  #Autumn / Efteraar
            start_year = year
        elif term_code == 'F':  #Spring / Foraar
            start_year = year - 1
        else:
            raise ValueError(f"Invalid term code '{term_code}' in term '{semester}'")
        year_range = f"{start_year}-{start_year + 1}"
        return year_range

    @staticmethod
    def exam_period_from_semester(course_semesters):
        """ Convert each semester in a list to its corresponding exam period,
            'F18' becomes 'Summer-2018', and
            'E20' becomes 'Winter-2020', etc. """
        exam_periods = []
        for semester in course_semesters:
            if semester[0] == 'F':  # F is foraar, and "Summer" is its exam period
                exam_periods.append('Summer-20'+str(semester[-2:]))
            elif semester[0] == 'E':  # E is efteraar, and "Winter" is its exam period
                exam_periods.append('Winter-20'+str(semester[-2:]))
            else:  # This is not supposed to ever happen
                raise ValueError(f"Invalid semester: {course_semesters}")
        return exam_periods

    @staticmethod
    def get_archived_course_numbers(academic_year):
        """Open JSON file with archived course numbers and return the course names for {semester} as a list"""
        with open(FileNameConsts.scraped_data_folder_name+'/'+FileNameConsts.archived_courses_json+'.json') as f:
            nested_course_dict = json.load(f)
        return nested_course_dict.get(academic_year, {})

    @staticmethod
    def get_archived_course_names(academic_year):
        """Open JSON file with archived course names and return the course names for {semester} as a list"""
        with open(FileNameConsts.scraped_data_folder_name+'/'+FileNameConsts.archived_courses_json+'.json') as f:
            nested_course_dict = json.load(f)
        return list(nested_course_dict.get(academic_year, {}).values())

    @staticmethod
    def get_all_archived_course_numbers():
        """Return a list of all unique course numbers across all semesters in the archived data."""
        path = f"{FileNameConsts.scraped_data_folder_name}/{FileNameConsts.archived_courses_json}.json"
        with open(path) as f:
            nested_course_dict = json.load(f)
        course_number_set = set()
        for inner_dict in nested_course_dict.values():
            course_number_set.update(inner_dict.keys())
        return sorted(course_number_set)

    @staticmethod
    def get_course_numbers():
        """Open JSON file with {current_year} course numbers and return them as a list"""
        with open(FileNameConsts.scraped_data_folder_name+'/'+FileNameConsts.course_number_json+'.json') as f:
            course_dict = json.load(f)
        course_numbers = list(course_dict.keys())
        return course_numbers

    @staticmethod
    def get_course_names():
        """Open JSON file with {current_year} course names and return them as a list"""
        with open(FileNameConsts.scraped_data_folder_name+'/'+FileNameConsts.course_number_json+'.json') as f:
            course_dict = json.load(f)
        course_names = list(course_dict.values())
        return course_names

    @staticmethod
    def create_folder(folder_name):
        """Create a folder with folderName if it does not already exist"""
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    @staticmethod
    def print_progress(iteration, course_numbers, dct, file_name):
        """Print current course to console so user can track the progress"""
        print(f'{file_name}: {iteration} of {len(course_numbers)} courses has been scraped')
        # Log the result in log file
        if len(dct) <= 0:
            message = f"{file_name}, {course_numbers[iteration]}: No elements found for this course"
            Utils.logger(message, 'log', FileNameConsts.scrape_log_name)

    @staticmethod
    def display_progress(iteration, course_numbers, file_name, frequency):
        """Display progress to user. Note that the first iteration is the 0th iteration"""
        if (iteration % frequency) == 0:
            print(f'{file_name}: {iteration} of {len(course_numbers)} course dicts complete')
        if iteration == len(course_numbers)-1:
            print(f'{file_name}: {len(course_numbers)} of {len(course_numbers)} course dicts complete')
            print()

    @staticmethod
    def rename_dict_keys(dct, front, back):
        """Append new_name to all dictionary keys"""
        length_of_dict = len(dct)
        dct_keys = list(dct.keys())
        for i in range(0, length_of_dict):
            dct[front+dct_keys[i]+back] = dct.pop(dct_keys[i])
        return dct

    @staticmethod
    def add_dict_to_df(dct, lst_of_column_names, df):
        "Add dict elements to df if dict keys matches column name"
        df_input = {}
        for element in lst_of_column_names:
            if element in dct:
                df_input[element] = [dct[element]]
            else:
                df_input[element] = [Config.data_null_value]
        new_df_row = pd.DataFrame(data = df_input)
        df = pd.concat([df, new_df_row], ignore_index=True)
        return df

    """
    @staticmethod
    def save_df_as_csv(file_name, df_index, df):
        "Save dataframe as csv file on harddisk in location specified by file_name"
        folder_name = FileNameConsts.scraped_data_folder_name
        Utils.create_folder(folder_name)
        file_location = f'{folder_name}/{file_name}.csv'
        df.set_index(df_index, inplace=True, drop=False)
        df.to_csv(file_location, index = False, header=True)"""

    @staticmethod
    def save_dct_as_json(file_name, dct):
        """Save dictionary as JSON file in location specified by file_name"""
        folder_name = FileNameConsts.scraped_data_folder_name
        Utils.create_folder(folder_name)
        file_location = f'{folder_name}/{file_name}.json'
        with open(file_location, 'w') as fp:
            json.dump(dct, fp)
        print(f'Output has been saved at {file_location}.json')

    @staticmethod
    def save_scraped_df(df, file_name):
        "Save dataframe as pkl file on harddisk in location specified by file_name"
        folder_name = FileNameConsts.scraped_data_folder_name
        Utils.create_folder(folder_name)
        df_index = FileNameConsts.df_index
        file_location = f'{folder_name}/{file_name}.pkl'
        df.set_index(df_index, inplace=True, drop=False)
        df.to_pickle(file_location)

    @staticmethod
    def save_df_as_csv(df, file_name):
        "Save dataframe as csv file on harddisk in location specified by file_name"
        folder_name = FileNameConsts.scraped_data_folder_name
        Utils.create_folder(folder_name)
        df_index = FileNameConsts.df_index
        file_location = f'{folder_name}/{file_name}.csv'
        df.set_index(df_index, inplace=True, drop=False)
        df.to_csv(file_location, index = False, header=True)

    @staticmethod
    def load_scraped_df(file_name):
        """Load in df from specified location and return it """
        folder_name = FileNameConsts.scraped_data_folder_name
        file_location = f'{folder_name}/{file_name}.pkl'
        df_index = FileNameConsts.df_index
        df = pd.read_pickle(file_location)
        df.set_index(df_index, inplace=True, drop=False)
        return df

    @staticmethod
    def logger(message, logtype = 'info', log_file_name = 'unspecified'):
        """Log message in log file. Also prints message unless type is 'log'"""

        if logtype.lower() != 'none':
            Utils.create_folder(FileNameConsts.log_folder_name+'/'+log_file_name)
            logging.basicConfig(filename=FileNameConsts.log_folder_name+'/'+log_file_name+'.log',
                                format='(%(asctime)s) %(levelname)s: %(message)s',
                                level=logging.INFO)

        # Print message to console (format varies based on 'type')
        if logtype.lower() == 'info':
            print(message)
        elif logtype.lower() == 'log':
            pass
        elif logtype.lower() == 'none':
            pass
        else:
            print(f'{logtype.capitalize()}: {message}')

        # Write message to log file (severity status based on 'type')
        if logtype.lower() == 'debug':
            logging.debug(message)
        elif logtype.lower() == 'info' or logtype.lower() == 'log':
            logging.info(message)
        elif logtype.lower() == 'warning':
            logging.warning(message)
        elif logtype.lower() == 'error':
            logging.error(message)
        elif logtype.lower() == 'critical':
            logging.critical(message)
        elif logtype.lower() == 'print':
            pass
        elif logtype.lower() == 'none':
            pass
        else:
            #logging.debug(f'{message} (INVALID LOG TYPE!)')
            logging.debug('%s (INVALID LOG TYPE!)', message)