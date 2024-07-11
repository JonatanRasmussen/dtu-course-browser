#%%

# Imports
# Helper functions and global constants
from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.config import Config
from scrape_course_numbers import scrape_course_numbers
from scrape_evaluations import scrape_evaluations
from scrape_grades import scrape_grades
from scrape_info import scrape_info

def run_all_scrape_scripts():
    """ Run all the scrape scripts. Some of them uses Selenium Webbrowser """
    # course numbers
    scrape_course_numbers()
    COURSE_NUMBERS = Utils.get_course_numbers()

    # evals
    eval_df_name = FileNameConsts.eval_df
    scrape_evaluations(COURSE_NUMBERS, eval_df_name)

    # grades
    course_semesters = Config.course_semesters
    grade_df_name = FileNameConsts.grade_df
    scrape_grades(COURSE_NUMBERS, course_semesters, grade_df_name)

    # info
    info_df_name = FileNameConsts.info_df
    scrape_info(COURSE_NUMBERS, info_df_name)

#%%
if __name__ == "__main__":
    run_all_scrape_scripts()
