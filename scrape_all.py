#%%

# Imports
# Helper functions and global constants
from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.config import Config
from scrape_archive import ArchiveScraper
from scrape_evaluations import EvalScraper
from scrape_grades import GradeScraper
from scrape_info import InfoScraper

class AllInOneScraper:

    @staticmethod
    def quick_test_scrape_for_debugging_please_ignore():
        """ Do a quick scrape to see if the code works."""
        course_numbers = ['01001', '02402']  # Example of valid courses for the below semesters
        course_semesters = ['F23', 'E23', 'F24']  # Example of valid semesters
        year_ranges = Utils.extract_unique_year_ranges(course_semesters)  # Years in format '2023-2024'
        academic_year = year_ranges[-1]  # year_ranges is a list, but only use one to speed up testing
        empty_file_name = ""  # This prevents scraped data from being saved to disk
        GradeScraper.scrape_grades(course_numbers, course_semesters, empty_file_name)
        EvalScraper.scrape_evaluations(course_numbers, course_semesters, empty_file_name)
        InfoScraper.scrape_info(course_numbers, academic_year, empty_file_name)
        ArchiveScraper.scrape_archive(course_semesters, empty_file_name)

    @staticmethod
    def run_all_scrape_scripts():
        """ Run all the scrape scripts. Some of them uses Selenium Webbrowser """
        course_semesters = Config.course_semesters
        AllInOneScraper._print_start_of_scrape_announcements(course_semesters, Config.course_years)

        # archived course numbers (course code + course title for each course for each academic year)
        if Config.feature_flag_scrape_archive:
            archive_file_name = FileNameConsts.archived_courses_json
            ArchiveScraper.scrape_archive(course_semesters, archive_file_name)

        # evals (course evaluations)
        all_course_numbers = Utils.get_all_archived_course_numbers()
        if Config.feature_flag_scrape_evals:
            eval_df_name = FileNameConsts.eval_df
            EvalScraper.scrape_evaluations(all_course_numbers, course_semesters, eval_df_name)

        # grades
        all_course_numbers = Utils.get_all_archived_course_numbers()
        if Config.feature_flag_scrape_grades:
            grade_df_name = FileNameConsts.grade_df
            GradeScraper.scrape_grades(all_course_numbers, course_semesters, grade_df_name)

        # info (Language / Schedule / ECTS / Location / Learning Objectives etc. from DTU Course Base)
        if Config.feature_flag_scrape_info:
            year_ranges = Utils.extract_unique_year_ranges(course_semesters)
            for academic_year in year_ranges:  # academic_year has format '2024-2025'
                current_year_course_numbers = Utils.get_archived_course_numbers(academic_year)
                if academic_year == Config.course_years:
                    info_df_name = FileNameConsts.info_df
                else:
                    info_df_name = f"{FileNameConsts.info_df}_{academic_year[0:4]}_{academic_year[5:9]}"
                InfoScraper.scrape_info(current_year_course_numbers, academic_year, info_df_name)

    @staticmethod
    def run_all_scrape_scripts_one_semester_at_a_time():
        course_semesters = Config.course_semesters
        AllInOneScraper._print_start_of_scrape_announcements(course_semesters, Config.course_years)

        previous_academic_year = ""
        for semester in course_semesters:
            single_semester_lst = [semester]
            current_academic_year = Utils.extract_year_range_from_semester(semester)
            academic_year_is_a_repeat = current_academic_year == previous_academic_year
            previous_academic_year = current_academic_year

            # archived course numbers (course code + course title for each course for each academic year)
            if Config.feature_flag_scrape_archive and not academic_year_is_a_repeat:
                archive_file_name = f"{FileNameConsts.archived_courses_json}_{current_academic_year[0:4]}_{current_academic_year[5:9]}"
                nested_dict = ArchiveScraper.scrape_archive(single_semester_lst, archive_file_name)

                # Get course_numbers from scraped archive
                unique_course_numbers = set()
                for inner_dict in nested_dict.values():
                    unique_course_numbers.update(inner_dict.keys())
                course_numbers = sorted(unique_course_numbers)

            # grades
            if Config.feature_flag_scrape_grades:
                grade_df_name = f"{FileNameConsts.grade_df}_{semester}"
                GradeScraper.scrape_grades(course_numbers, single_semester_lst, grade_df_name)

            # evals (course evaluations)
            if Config.feature_flag_scrape_evals:
                eval_df_name = f"{FileNameConsts.eval_df}_{semester}"
                EvalScraper.scrape_evaluations(course_numbers, single_semester_lst, eval_df_name)

            # info (Language / Schedule / ECTS / Location / Learning Objectives etc. from DTU Course Base)
            if Config.feature_flag_scrape_info and not academic_year_is_a_repeat:
                info_df_name = f"{FileNameConsts.info_df}_{current_academic_year[0:4]}_{current_academic_year[5:9]}"
                InfoScraper.scrape_info(course_numbers, current_academic_year, info_df_name)



    @staticmethod
    def _print_start_of_scrape_announcements(course_semesters, current_year):
        print()
        print("DTU Course scraping will now begin... ")
        print("Check dtu_course_project/website/global_constants/config.py for scrape config.")
        print(f"Config file is currently set to current year = {current_year}...")
        print(f"...With semesters = {course_semesters}.")
        print("Ensure that config file's current year matches the most recent year on DTU's website!")
        print("Otherwise you will get warnings/errors for missing data during the scraping.")
        print()


#%%
if __name__ == "__main__":
    AllInOneScraper.quick_test_scrape_for_debugging_please_ignore()
    AllInOneScraper.run_all_scrape_scripts_one_semester_at_a_time()
    AllInOneScraper.run_all_scrape_scripts()
