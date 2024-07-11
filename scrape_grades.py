#%%

# Imports
import pandas as pd
import urllib
# Helper functions and global constants
from utils import Utils
from website.global_constants.config import Config
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.grade_consts import GradeConsts


def scrape_grades(course_numbers, course_semesters, file_name):
    """Scrape grades for a given set of courses and semesters"""

    def exam_period_from_semester(course_semesters):
        """ Convert each semester in a list to its corresponding exam period,
            'F18' becomes 'Summer-2018', and
            'E20' becomes 'Winter-2020', etc. """
        exam_periods = []
        for semester in course_semesters:
            # F stands for Forår, and "Summer" is the corresponding exam period
            if semester[0] == 'F':
                exam_periods.append('Summer-20'+str(semester[-2:]))
            # E stands for Efterår, and "Winter" is the corresponding exam period
            elif semester[0] == 'E':
                exam_periods.append('Winter-20'+str(semester[-2:]))
            # This should never happen
            else:
                exam_periods.append('XXXXXX-20'+str(semester[-2:]))
                message = f"{file_name}: Invalid semester: {course_semesters}"
                Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
        return exam_periods


    def scrape_grades_if_url_exists(url):
        """ Pandas grabs the raw html of the specified url and attempts to extract any tables it can find. If the url links to
            a valid exam period for the course, 3 tables will be found (the 3rd table contains the grades), and the grades are
            formatted into a dict. If the url contains 0 tables, the exam period is invalid and an empty dict is returned instead."""
        df_found = False
        try:
            # We assunme that if pd.read_html finds a table, the url contain grades
            df = pd.read_html(url, header=0)
            # These grades are loaded into a dictionary based on the following code
            table_containing_grades = df[2]
            df_found = True
            table_containing_grades = table_containing_grades.set_index('Karakter')
            table_containing_grades = table_containing_grades.iloc[:,0]
            scraped_dict = table_containing_grades.to_dict()
            scraped_dict = {str(k): v for k, v in scraped_dict.items()}
            scraped_dict = {k.capitalize(): v for k, v in scraped_dict.items()}

        # If url is invalid (no table found), then return an empty dict
        except (urllib.error.HTTPError, IndexError):
            scraped_dict = {}

        # If the following ever happens it probably means that DTU has updated their website and I have to re-write my code
        if scraped_dict == {} and df_found == True:
            message = f"{file_name}: {course}_{exam_periods[i]} Grades found on url but dict is empty (url: {url})"
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
        return scraped_dict


    def format_scraped_dict(scraped_dict, course_number, course_semester):
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


#%% Start of main script

    # Get list of exam periods to be scraped based on list of semesters
    # For example, given E19 and F20 as input, the output is Winter-2019 and Summer-2020
    exam_periods = exam_period_from_semester(course_semesters)

    # Begin the webscrape and initialize the data frame
    print('Webscrape of grades will now begin...')
    df, lst_of_column_names, df_index = Utils.initialize_df(GradeConsts.list_of_grades)
    # Loop through all courses
    iteration_count = 0
    for course in course_numbers:
        df_row = {df_index: course}

        # Loop through all semesters for each course
        for i in range (0, len(exam_periods)):

            # Attempt to scrape grades if the exam period exists
            url = f'https://karakterer.dtu.dk/Histogram/1/{course}/{exam_periods[i]}'
            scraped_grades_dct = scrape_grades_if_url_exists(url)

            # Add grades to dictionary if url exists
            single_semester_dict = format_scraped_dict(scraped_grades_dct, course, course_semesters[i])
            df_row.update(single_semester_dict)

        # Concatenate dict to dataframe as a new row
        df = Utils.add_dict_to_df(df_row, lst_of_column_names, df)

        # Print current course to console so user can track the progress
        iteration_count += 1
        Utils.print_progress(iteration_count, course_numbers, df_row, file_name)


    # Save all grades as df
    Utils.save_scraped_df(df, file_name)
    Utils.save_df_as_csv(df, file_name)

    # Webscrape for all courses and semesters has been completed
    print()
    print('Webscrape of grades is now completed! Check log for details.')
    df.set_index(df_index, inplace=True, drop=True)
    print(f"Sample output: {df}")
    print()


#%%
if __name__ == "__main__":
    # Variables and initialization
    COURSE_NUMBERS = Utils.get_course_numbers()
    #COURSE_NUMBERS = ['01005', '01017']

    course_semesters = Config.course_semesters
    grade_df_name = FileNameConsts.grade_df
    scrape_grades(COURSE_NUMBERS, course_semesters, grade_df_name)