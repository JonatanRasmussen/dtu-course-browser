#%%

# Imports
from io import StringIO
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# Helper functions and global constants
from utils import Utils
from website.global_constants.config import Config
from website.global_constants.dtu_consts import DtuConsts
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts

# TO FIX CHROMEDRIVER, GO TO https://chromedriver.chromium.org/downloads
# AND PLACE NEW VERSION IN C:\Program Files (x86)\ChromeDriver


def scrape_info(course_numbers, academic_year, file_name):
    """Scrape the info screen for a course"""

    def get_course_info_page_source(course_number, academic_year):
        """Open course's info page with webdriver and return the page source"""
        url = 'https://kurser.dtu.dk/course/'+str(academic_year)+course_number
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "viewport")))
        page_source = driver.page_source
        return page_source

    def get_course_responsible_page_source(course_number):
        """Open course's info page with webdriver and return the page source"""
        url = 'https://kurser.dtu.dk/course/'+course_number+'/info'
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "viewport")))
        page_source = driver.page_source
        return page_source

    def convert_html_df_into_dict(html_df):
        """Take a data frame and format it into a dictionary"""
        info_dct = {}
        df_0 = html_df[0].copy(deep=True)
        df_1 = html_df[1].copy(deep=True)
        df_2 = html_df[2].copy(deep=True)
        df = pd.concat([df_0, df_1, df_2], axis=0, ignore_index=True)
        df.columns=['key', 'value']
        df = df.set_index('key')
        df = df.iloc[:,0]
        info_dct = df.to_dict()
        return info_dct

    def scrape_from_page_source(page_source, start, end):
        """Return study lines associated with a course from page_source"""
        # Split the page source and the start and end of study lines string
        page_source = page_source.replace("\r"," ")
        page_source = page_source.replace("\n"," ")
        page_source = page_source.replace("    ","")
        page_source = page_source.replace("   "," ")
        page_source = page_source.replace("  "," ")
        page_source = page_source.replace("<ul><li>","<br />- ")
        page_source = page_source.replace("</li><li>","<br />- ")
        start = page_source.split(start)
        end = start[1].split(end)
        string = end[0]
        return string

    def get_name_and_pic_from_page_source(responsibles_lst, course_responsible_number):
        """Return name and image-link of course responsible"""
        responsible_name = DtuConsts.dtu_no_data_for_responsible
        responsible_pic = DtuConsts.dtu_no_data_for_responsible
        if len(responsibles_lst) > course_responsible_number:
            responsible_source = responsibles_lst[course_responsible_number]
            name_start = '<b>'
            name_end = '</b>'
            responsible_name = scrape_from_page_source(responsible_source, name_start, name_end)
            pic_start = '<img src="'
            pic_end = '"'
            responsible_pic = scrape_from_page_source(responsible_source, pic_start, pic_end)
        return (responsible_name, responsible_pic)





#%%

    # Begin the webscrape and initialize the data frame
    df_index = FileNameConsts.df_index
    df_columns = {}
    lst_of_column_names = [df_index] + InfoConsts.scrape_info_column_names
    for column_name in lst_of_column_names:
        df_columns[column_name] = []
    df = pd.DataFrame(data = df_columns)
    driver = Utils.launch_selenium()

    # Loop through all courses
    print('Webscrape of info will now begin...')
    iteration_count = 0
    for course in course_numbers:
        df_row = {df_index: course}

        # Scrape all info inside the dataframe found on the webpage
        try:
            page_source = get_course_info_page_source(course, academic_year)
            html_io = StringIO(page_source)
            html_df = pd.read_html(html_io)
            # DEPRACATED html_df = pd.read_html(page_source)
            # The current version of the dtu website contains a df of length 3
            if len(html_df) != 3:
                message = f"{file_name}, {course}: len(df) is {str(len(html_df))} instead of 3"
                Utils.logger(message, 'Warning', FileNameConsts.scrape_log_name)
            info_dct = convert_html_df_into_dict(html_df)
            df_row.update(info_dct)
        except ImportError:
            message = f"{file_name}, {course}: Missing import / pipinstall for parsing html"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
        except:
            message = f"{file_name}, {course}: Timeout when loading URL"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape study lines
        try:
            start = 'var lines = '
            end = ";" #var collectedTooltips = {};"    # SOMETIMES <br />
            study_lines = scrape_from_page_source(page_source, start, end)
            df_row[DtuConsts.dtu_accosiated_study_lines] = study_lines
        except:
            message = f"{file_name}, {course}: Error when splitting page_source"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape last updated
        try:
            start = f'{DtuConsts.dtu_last_updated}</div> '
            end = '<'
            last_updated = scrape_from_page_source(page_source, start, end)
            df_row[DtuConsts.dtu_last_updated] = last_updated
        except:
            message = f"{file_name}, {course}: Error when splitting page_source"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape General course objectives
        try:
            start = f'{DtuConsts.dtu_general_course_objectives}</div> '
            end = '<div class='
            course_objectives = scrape_from_page_source(page_source, start, end)
            df_row[DtuConsts.dtu_general_course_objectives] = course_objectives
        except:
            message = f"{file_name}, {course}: Error when splitting page_source"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape Learning objectives
        try:
            start = f'{DtuConsts.dtu_learning_objectives}</div> '
            end = '<div class='
            learning_objectives = scrape_from_page_source(page_source, start, end)
            df_row[DtuConsts.dtu_learning_objectives] = learning_objectives
        except:
            message = f"{file_name}, {course}: Error when splitting page_source"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape course content
        try:
            start = f'>{DtuConsts.dtu_content}</div> '
            end = '<div class='
            course_content = scrape_from_page_source(page_source, start, end)
            df_row[DtuConsts.dtu_content] = course_content
        except:
            message = f"{file_name}, {course}: Error when splitting page_source"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Scrape course remarks
        try:
            start = f'>{DtuConsts.dtu_remarks}</div> '
            end = '<div class='
            if DtuConsts.dtu_remarks in page_source:
                course_remarks = scrape_from_page_source(page_source, start, end)
            else:
                course_remarks = DtuConsts.dtu_no_remarks
            df_row[DtuConsts.dtu_remarks] = course_remarks
        except:
            pass

        # Scrape highlighted message
        try:
            start = '<div class="row"><div class="col-xs-12">'
            end = '<div class=</div></div><div class="row"><div class="col-md-6 col-sm-12 col-xs-12">'
            if start in page_source:
                course_remarks = scrape_from_page_source(page_source, start, end)
            else:
                course_remarks = DtuConsts.dtu_no_highlighted_message
            df_row[DtuConsts.dtu_highlighted_message] = course_remarks
        except:
            pass

        if academic_year == Config.course_years:
            # Scrape course responsibles page source
            try:
                page_source_responsibles = get_course_responsible_page_source(course)
            except:
                message = f"{file_name}, {course}: Timeout when loading URL for course responsibles"
                Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
        else:
            page_source_responsibles = ""

        # Scrape main responsible
        try:
            responsibles_lst = page_source_responsibles.split('<div class="row" style="margin:20px">')
            main_name, main_pic = get_name_and_pic_from_page_source(responsibles_lst, 1)
            df_row[DtuConsts.dtu_name_of_main_responsible] = main_name
            df_row[DtuConsts.dtu_pic_of_main_responsible] = main_pic
            co_1_name, co_1_pic = get_name_and_pic_from_page_source(responsibles_lst, 2)
            df_row[DtuConsts.dtu_name_of_co_responsible_1] = co_1_name
            df_row[DtuConsts.dtu_pic_of_co_responsible_1] = co_1_pic
            co_2_name, co_2_pic = get_name_and_pic_from_page_source(responsibles_lst, 3)
            df_row[DtuConsts.dtu_name_of_co_responsible_2] = co_2_name
            df_row[DtuConsts.dtu_pic_of_co_responsible_2] = co_2_pic
            co_3_name, co_3_pic = get_name_and_pic_from_page_source(responsibles_lst, 4)
            df_row[DtuConsts.dtu_name_of_co_responsible_3] = co_3_name
            df_row[DtuConsts.dtu_pic_of_co_responsible_3] = co_3_pic
            co_4_name, co_4_pic = get_name_and_pic_from_page_source(responsibles_lst, 5)
            df_row[DtuConsts.dtu_name_of_co_responsible_4] = co_4_name
            df_row[DtuConsts.dtu_pic_of_co_responsible_4] = co_4_pic
        except:
            message = f"{file_name}, {course}: Error when scraping main responsible"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Concatenate dict to dataframe as a new row
        df = Utils.add_dict_to_df(df_row, lst_of_column_names, df)

        # Print current course to console so user can track the progress
        iteration_count += 1
        if iteration_count % 50 == 0 or iteration_count == 1:
            Utils.print_progress(iteration_count, course_numbers, df_row, file_name)

    # Save all info as df
    Utils.save_scraped_df(df, file_name)
    Utils.save_df_as_csv(df, file_name)

    # End of program
    driver.quit
    # Webscrape for all courses have been completed
    print()
    print('Webscrape of info is now completed! Check log for details.')
    df.set_index(df_index, inplace=True, drop=True)
    print(f"Sample output: {df}")
    print()

#%%
if __name__ == "__main__":
    # Variables and initialization
    COURSE_NUMBERS = Utils.get_course_numbers()
    #COURSE_NUMBERS = ['01005', '01017']

    info_df_name = FileNameConsts.info_df
    scrape_info(COURSE_NUMBERS, Config.course_years, info_df_name)
