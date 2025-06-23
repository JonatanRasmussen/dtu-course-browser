#%%

# Imports
import pandas as pd
import urllib
# Helper functions and global constants
from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.grade_consts import GradeConsts


class GradeScraper:

    @staticmethod
    def quick_test_scrape_for_debugging_please_ignore():
        """ Do a quick scrape to see if the code works."""
        course_numbers = ['01001', '02402']  # Example of valid courses for the below semesters
        course_semesters = ['F23', 'E23', 'F24']  # Example of valid semesters
        file_name = "scraped_grades_test"
        GradeScraper.scrape_archive(course_numbers, course_semesters, file_name)

    @staticmethod
    def scrape_grades(course_numbers, course_semesters, file_name):
        """Scrape grades for a given set of courses and semesters"""
        print('Webscrape of grades will now begin...')
        exam_periods = Utils.exam_period_from_semester(course_semesters)  # Get exam periods from semesters, for example E19 and F20 becomes Winter-2019 and Summer-2020
        df, lst_of_column_names, df_index = Utils.initialize_df(course_semesters, GradeConsts.list_of_grades)  # Begin webscrape and initialize data frame
        iteration_count = 0
        for course in course_numbers:
            df_row = {df_index: course}
            for i in range (0, len(exam_periods)):  # Loop through all semesters for each course
                url = f'https://karakterer.dtu.dk/Histogram/1/{course}/{exam_periods[i]}'
                scraped_grades_dct = GradeScraper._scrape_grades_if_url_exists(url, course, exam_periods[i], file_name)  # If the exam period exists, attempt to scrape grades
                single_semester_dict = GradeScraper._format_scraped_dict(scraped_grades_dct, course, course_semesters[i], file_name)  # Add grades to dictionary if url exists
                df_row.update(single_semester_dict)
            df = Utils.add_dict_to_df(df_row, lst_of_column_names, df)  # Concatenate dict to dataframe as a new row
            iteration_count += 1  # Print current course to console so user can track the progress
            if iteration_count % 50 == 0 or iteration_count == 1:
                Utils.print_progress(iteration_count, course_numbers, df_row, file_name)
        if len(file_name) != 0:
            Utils.save_scraped_df(df, file_name)  # Save all grades as .pkl
            Utils.save_df_as_csv(df, file_name)  # Save all grades as .csv
        print()  # Webscrape for all courses and semesters has been completed
        print('Webscrape of grades is now completed! Check log for details.')
        df.set_index(df_index, inplace=True, drop=True)
        print(f"Sample output: {df}")
        print()
        return df

    @staticmethod
    def _scrape_grades_if_url_exists(url, course, exam_period, file_name):
        """ Pandas grabs the raw html of the specified url and attempts to extract any tables it can find. If the url links to
            a valid exam period for the course, 3 tables will be found (the 3rd table contains the grades), and the grades are
            formatted into a dict. If the url contains 0 tables, the exam period is invalid and an empty dict is returned instead."""
        df_found = False
        try:
            # We assunme that if pd.read_html finds a table, the url contain grades
            df = pd.read_html(url, header=0)
            if len(df) >= 3:
                # These grades are loaded into a dictionary based on the following code
                table_containing_grades = df[2]
                df_found = True
                table_containing_grades = table_containing_grades.set_index('Karakter')
                table_containing_grades = table_containing_grades.iloc[:,0]

                scraped_dict = table_containing_grades.to_dict()
                scraped_dict = {str(k): v for k, v in scraped_dict.items()}
                scraped_dict = {k.capitalize(): v for k, v in scraped_dict.items()}

                Utils.logger(f"Scraped data for {url}: {scraped_dict}", "Log", FileNameConsts.scrape_log_name)
            elif len(df) == 2:
                scraped_dict = {}
                Utils.logger(f"Scraped data for {url}: {scraped_dict} Grades are not public due to there being 3 or fewer grades", "Log", FileNameConsts.scrape_log_name)
            else:
                scraped_dict = {}
                Utils.logger(f"Scraped data for {url}: {scraped_dict} Not enough tables. Expected at least 3, got {len(df)}", "Warning", FileNameConsts.scrape_log_name)

        # If url is invalid (no table found), then return an empty dict
        except (urllib.error.HTTPError, IndexError) as _:
            Utils.logger(f"Scraped data for {url}: Grade page returns 404 and likely does not exist", "Log", FileNameConsts.scrape_log_name)
            scraped_dict = {}

        # If the following ever happens it probably means that DTU has updated their website and I have to re-write my code
        if scraped_dict == {} and df_found is True:
            message = f"{file_name}: {course}_{exam_period} Grades found on url but dict is empty (url: {url})"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)

        # Quick fix for "02" becoming "2" and "00" becoming "0" if "Ej mødt" grade is missing, causing the table to be parsed as ints rather than strs
        if "0" in scraped_dict:
            scraped_dict["00"] = scraped_dict.pop("0")
        if "2" in scraped_dict:
            scraped_dict["02"] = scraped_dict.pop("2")

        return scraped_dict

    @staticmethod
    def _format_scraped_dict(scraped_dict, course_number, course_semester, file_name):
        """ Extract grades from the dict scraped from url by pandas """
        grades_dict = {}
        grade_renaming = {"12": GradeConsts.grade_12,
                          "10": GradeConsts.grade_10,
                          "7": GradeConsts.grade_7,
                          "4": GradeConsts.grade_4,
                          "02": GradeConsts.grade_02,
                          "00": GradeConsts.grade_00,
                          "-3": GradeConsts.grade_minus_3,
                          "Bestået": GradeConsts.grade_passed,
                          "Ikke bestået": GradeConsts.grade_failed,
                          "Ej mødt": GradeConsts.grade_absent,
                          "Syg": "ILL",
                          "Godkendt": "APPROVED",
                          "Ikke Godkendt": "REJECTED"}
        absent_count = 0
        for key in grade_renaming:
            # If grade does not exist in scraped data, insert our custom null-value
            if key not in scraped_dict:
                new_key = f"{course_semester}_{grade_renaming[key]}"
                grades_dict[new_key] = GradeConsts.grade_none
            # Grade exists in scraped data; is it an "absent" value or a "grade" value?
            else:
                # Bundle all reasons for exam absense into a single catagory
                if key == "Syg" or key == "Ej mødt" or key == "Ikke Godkendt":
                    absent_count += scraped_dict[key]

                # The table row "Godkendt" exists on DTU grades website, but the value is always 0. I would like to be notified if this changes at some point.
                elif key == "Godkendt":
                    if scraped_dict["Godkendt"] != 0:
                        message = f"{file_name}: {course_number}_{course_semester} grade 'Godkendt' now exists!"
                        Utils.logger(message, "Warning", FileNameConsts.scrape_log_name)
                else:
                # For current semester, add to dict how many students optained the grade in question
                    new_key = f"{course_semester}_{grade_renaming[key]}"
                    grades_dict[new_key] = scraped_dict[key]
        # Finally, if any students didn't attend exam for whatever reason, add that to dict as well
        if absent_count != 0:
            grades_dict[f"{course_semester}_{GradeConsts.grade_absent}"] = absent_count
        return grades_dict


#%%
if __name__ == "__main__":
    GradeScraper.quick_test_scrape_for_debugging_please_ignore()