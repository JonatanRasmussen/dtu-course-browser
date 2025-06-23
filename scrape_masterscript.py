#%%

# Imports
# Helper functions and global constants
from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.config import Config
from scrape_archive import scrape_archive
from scrape_evaluations import scrape_evaluations
from scrape_grades import scrape_grades
from scrape_info import scrape_info

def run_all_scrape_scripts():
    """ Run all the scrape scripts. Some of them uses Selenium Webbrowser """
    print()
    print("DTU Course scraping will now begin... ")
    print("Check dtu_course_project/website/global_constants/config.py for scrape config.")
    print(f"Config file is currently set to current year = {Config.course_years}...")
    print(f"...With semesters = {Config.course_semesters}.")
    print("Ensure that config file's current year matches the most recent year on DTU's website!")
    print("Otherwise you will get warnings/errors for missing data during the scraping.")
    print()

    # archived course numbers
    course_semesters = Config.course_semesters
    #scrape_archive(course_semesters)

    # evals
    eval_df_name = FileNameConsts.eval_df
    all_course_numbers = Utils.get_all_archived_course_numbers()
    #scrape_evaluations(all_course_numbers, eval_df_name)

    # grades
    grade_df_name = FileNameConsts.grade_df
    #scrape_grades(all_course_numbers, course_semesters, grade_df_name)

    # info
    year_ranges = Utils.extract_unique_year_ranges(course_semesters)
    for year_range in year_ranges:  # academic_year has format '2024-2025'
        academic_year = f"{year_range}/"
        print(f'Scraping course info for academic years {year_ranges[0]} to {year_ranges[-1]}...')
        print(f'Academic year about to be scraped: {year_range}')
        current_year_course_numbers = Utils.get_archived_course_numbers(year_range)
        if academic_year == Config.course_years:
            info_df_name = FileNameConsts.info_df
        else:
            info_df_name = f"{FileNameConsts.info_df}_{academic_year[0:4]}_{academic_year[5:9]}"
        scrape_info(current_year_course_numbers, academic_year, info_df_name)



#%%
if __name__ == "__main__":
    run_all_scrape_scripts()
