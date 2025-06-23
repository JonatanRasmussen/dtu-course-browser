#%%

# Imports
# Helper functions and global constants
from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.config import Config
from scrape_archive import ArchiveScraper
from scrape_evaluations import EvalScraper
from scrape_grades import GradeScraper
from scrape_info_new import InfoScraper

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

    # archived course numbers (course code + course title for each course for each academic year)
    archive_file_name = FileNameConsts.archived_courses_json
    course_semesters = Config.course_semesters
    if Config.feature_flag_scrape_archive:
        ArchiveScraper.scrape_archive(course_semesters, archive_file_name)

    # evals (course evaluations)
    eval_df_name = FileNameConsts.eval_df
    all_course_numbers = Utils.get_all_archived_course_numbers()
    if Config.feature_flag_scrape_evals:
        EvalScraper.scrape_evaluations(all_course_numbers, eval_df_name)

    # grades
    grade_df_name = FileNameConsts.grade_df
    if Config.feature_flag_scrape_grades:
        GradeScraper.scrape_grades(all_course_numbers, course_semesters, grade_df_name)

    # info (Language / Schedule / ECTS / Location / Learning Objectives etc. from DTU Course Base)
    if Config.feature_flag_scrape_info:
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
            InfoScraper.scrape_info(current_year_course_numbers, academic_year, info_df_name)



#%%
if __name__ == "__main__":
    run_all_scrape_scripts()
