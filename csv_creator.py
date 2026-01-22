#%%

import pandas as pd
import json
import re

from format_evaluations import EvalFormatter
from format_grades import GradeFormatter
from format_info import InfoFormatter
from format_study_lines import create_teacher_course_lst
from utils import Utils
from website.global_constants import website_consts
from website.global_constants.config import Config
from website.global_constants.csv_columns_consts import CsvColumnConsts
from website.global_constants.dtu_consts import DtuConsts
from website.global_constants.eval_consts import EvalConsts
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.grade_consts import GradeConsts
from website.global_constants.info_consts import InfoConsts
from website.global_constants.website_consts import WebsiteConsts


class CsvCreator:

    @staticmethod
    def quick_test_for_debugging_please_ignore():
        """ Do a quick formatting test to see if the code works."""
        GradeFormatter.quick_test_for_debugging_please_ignore()
        EvalFormatter.quick_test_for_debugging_please_ignore()
        InfoFormatter.quick_test_for_debugging_please_ignore()

    @staticmethod
    def create_csv():
        """ Clean, format and parse the scraped_data into a csv and other files used by my website """
        name_and_path_of_csv = FileNameConsts.path_of_csv + FileNameConsts.name_of_csv + ".csv"
        name_and_path_of_pkl = FileNameConsts.path_of_pkl + FileNameConsts.name_of_pkl + ".pkl"
        print()
        print("Part 1 of 3: Creating csv file with specified columns: "+name_and_path_of_csv)
        print()
        premade_columns = CsvColumnConsts.PREMADE_COLUMNS
        premade_columns_df = CsvCreator._build_combined_df(name_and_path_of_csv, premade_columns)
        print(f"Success! Saving df {name_and_path_of_csv} to both csv and pickle format...")
        premade_columns_df.to_csv(name_and_path_of_csv, index = False, header=True)
        premade_columns_df.to_pickle(name_and_path_of_pkl)

        name_and_path_of_extended_csv = FileNameConsts.path_of_csv + FileNameConsts.extended_csv_name + ".csv"
        name_and_path_of_extended_pkl = FileNameConsts.path_of_pkl + FileNameConsts.extended_pkl_name + ".pkl"
        print()
        print("Part 2 of 3: Creating extended csv file with all columns: "+name_and_path_of_extended_csv)
        print()
        no_premade_columns = []
        all_columns_df = CsvCreator._build_combined_df(name_and_path_of_extended_csv, no_premade_columns)
        print()
        print(f"Success! Saving df {name_and_path_of_csv} to both csv and pickle format...")
        all_columns_df.to_csv(name_and_path_of_extended_csv, index = False, header=True)
        all_columns_df.to_pickle(name_and_path_of_extended_pkl)

        print()
        print("Part 3 of 3: Creating json files used for website search and filter functionality...")
        print()
        #save specific columns as json dct that are used by the website
        data_dct = WebsiteConsts.create_website_data_dct(premade_columns_df)  # Use premade column df
        CsvCreator._data_dct_to_json(data_dct)
        CsvCreator._filter_dct_to_json(all_columns_df)  # Use all columns df
        print()

        # Success!
        print("Success! Program will now terminate.")

    @staticmethod
    def _build_combined_df(file_name, premade_columns):
        """Create and save .csv file with data for all courses"""
        all_course_numbers = Utils.get_all_archived_course_numbers()
        course_numbers = Utils.get_archived_course_numbers(Config.course_years)
        course_names = Utils.get_archived_course_names(Config.course_years)
        grade_df = Utils.load_scraped_df(FileNameConsts.grade_df)
        eval_df = Utils.load_scraped_df(FileNameConsts.eval_df)
        info_df = Utils.load_scraped_df(f"{FileNameConsts.info_df}_{Config.course_years.replace('-','_')}")
        # Adding data dicts to the data frame, one course at a time
        semesters = Config.course_semesters
        column_names = []  # Create list with column names, this will be the data frame columns
        df = pd.DataFrame()

        for i in range(0, len(course_numbers)):
            info_formatted_dct = InfoFormatter.format_info(info_df, course_numbers[i])
            if InfoConsts.previous_course.key_df in info_formatted_dct:
                previous_courses = InfoFormatter.parse_previous_courses_from_dtu_website_rawstring(info_formatted_dct[InfoConsts.previous_course.key_df])
                for previous_course in previous_courses:
                    if previous_course in all_course_numbers:
                        for df, _ in [(eval_df, ""), (grade_df, "")]:
                            current_row = df.loc[course_numbers[i]]
                            if course_numbers[i] not in df.index or previous_course not in df.index:
                                continue  # No data at all for previous course
                            prev_row = df.loc[previous_course]
                            for col in df.columns:
                                if not isinstance(col, str) or not col.startswith((DtuConsts.dtu_term_spring, DtuConsts.dtu_term_autumn)):
                                    continue  # Skip columns that are not semester-specific
                                current_val = current_row[col]
                                if current_val == "" or current_val is None or current_val == GradeConsts.grade_none: # or pd.isna(current_val):
                                    prev_val = prev_row[col]  # Only fill in missing data ("", "No data", or NaN) in the current course
                                    if prev_val != "" and prev_val is not None and prev_val != GradeConsts.grade_none:
                                        df.at[course_numbers[i], col] = prev_val  # Only copy if the previous course actually has data

        for i in range(0, len(course_numbers)):
            grades_formatted_dct = GradeFormatter.format_grades(grade_df, course_numbers[i], semesters)
            evals_formatted_dct = EvalFormatter.format_evaluations(eval_df, course_numbers[i], semesters)
            info_formatted_dct = InfoFormatter.format_info(info_df, course_numbers[i])
            data_dct = {**grades_formatted_dct, **evals_formatted_dct, **info_formatted_dct}
            if i == 0:  # Initialize columns
                if premade_columns == []:  # Create a column for all keys in data_dct if no premade columns exist
                    column_names = [FileNameConsts.df_index] + [InfoConsts.name_english] + list(data_dct.keys())
                else:
                    column_names = [FileNameConsts.df_index] + [InfoConsts.name_english] + premade_columns
            # Insert each value from data_dct into the matching column in the df.
            df_input = {FileNameConsts.df_index: [str(course_numbers[i])], InfoConsts.name_english: [str(course_names[i])]}
            for j in range(2, len(column_names)):  # 2 because first two columns are COURSE and NAME
                if str(column_names[j]) in data_dct:
                    df_input[str(column_names[j])] = [data_dct[column_names[j]]]
                else:
                    df_input[str(column_names[j])] = [None]
            if i == 0:  # On first loop, create df, then add a new row to data frame on each loop
                df = pd.DataFrame(data = df_input)
            else:
                new_df_row = pd.DataFrame(data = df_input)
                df = pd.concat([df, new_df_row], ignore_index=True)
            Utils.display_progress(i, course_numbers, file_name, 100)  # Display progress to user
        df = df.copy() # df is copied to 'fix fragmentation', which prevents an annoying pandas PerformanceWarning that is polluting the terminal
        df.set_index(FileNameConsts.df_index, inplace=True, drop=False)  # Set course ID as df index
        if (InfoConsts.main_responsible_name.key_df) in premade_columns or premade_columns == []:
            df = create_teacher_course_lst(df, course_numbers)  # Append columns containing each responsibles' course list. Must be done after rest of the df is finalized
        if (InfoConsts.subsequent_courses.key_df) in premade_columns or premade_columns == []:
            df = CsvCreator._add_subsequent_courses(df, course_numbers)

        for col in df.columns:  # Quick and dirty test: flag columns where all values are identical (incl. None/empty/NaN)
            unique_vals = pd.Series(df[col].unique()).dropna()  # drop NaN
            unique_vals = unique_vals.replace("", None)  # treat empty string as None
            if len(unique_vals) <= 1 and col != InfoConsts.old_recommended_prerequisites.key_df and col[0] != DtuConsts.dtu_term_autumn[0] and col[0] != DtuConsts.dtu_term_spring[0]:  # I know this will impact all columns starting with E and F but I kinda don't care
                print(f"[Warning] Column '{col}' has identical values for all rows: {unique_vals.iloc[0] if not unique_vals.empty else None}")
        return df

    @staticmethod
    def _add_subsequent_courses(df, course_numbers):
        """Generate reversed course prerequisites (the courses a course gives access to)"""
        prereq_keys = [InfoConsts.recommended_prerequisites.key_df, InfoConsts.old_recommended_prerequisites.key_df, InfoConsts.mandatory_prerequisites.key_df]
        valid_courses_set = set(str(c) for c in course_numbers)
        subsequent_map = {str(c): set() for c in course_numbers} # course_numbers is converted to a set for O(1) lookups
        for current_course_id, row in df.iterrows():  # Iterate over every course in the dataframe to find what prerequisites they require
            combined_prereq_text = ""  # Combine text from all prerequisite columns into one string
            for key in prereq_keys:
                if key in df.columns:
                    val = row[key]
                    if val and pd.notna(val):
                        combined_prereq_text += " " + str(val)
            # Use Regex to find all 5-digit course numbers in the text
            found_prereqs = re.findall(r"\b\d{5}\b", combined_prereq_text)  # Pattern \b\d{5}\b ensures we match exactly 5 digits surrounded by word boundaries
            for prereq in found_prereqs:  # For every prerequisite found, record that the 'current_course_id' comes after it
                if prereq in valid_courses_set:
                    subsequent_map[prereq].add(str(current_course_id))  # If Course A requires Course B (prereq), then Course A is a subsequent course for Course B.
        for course_id in df.index:  # Populate the dataframe with the formatted strings
            course_id_str = str(course_id)
            if course_id_str in subsequent_map and subsequent_map[course_id_str]:
                sorted_subsequent = sorted(list(subsequent_map[course_id_str]))  # Sort the courses to ensure deterministic order
                formatted_str = ', '.join(sorted_subsequent)  # Format as: 01002, 02003, 42604
                df.at[course_id, InfoConsts.subsequent_courses.key_df] = formatted_str
            else:
                df.at[course_id, InfoConsts.subsequent_courses.key_df] = InfoConsts.no_subsequent_courses
        return df

    @staticmethod
    def _data_dct_to_json(data_dct):
        json_name = WebsiteConsts.json_course_data
        path_and_file_name = FileNameConsts.path_of_pkl + json_name + '.json'
        with open(path_and_file_name, 'w') as fp:
            json.dump(data_dct, fp)
        print(f"The dictionary {json_name}.json has been saved...")
        print()

    @staticmethod
    def _filter_dct_to_json(df):
        """ Create and save a nested dict dct used for website filter functionality.
            Each inner dict covers a filter category, such as "Language" or "Schedule"
            For example, the nested dict for "Language" contains the keys "Danish" and "English"
            The value for each of those keys is a list of all the danish courses and english courses
            To access the list of all courses in english, access filter_dct[Language][English] """
        filter_dct = {}
        # Add columns used for website filtering, one by one
        info_lst = InfoConsts.info_to_format
        for info in info_lst:
            if info.values_df != []:
                lst_of_column_names = list(dict.fromkeys(info.values_df))
                translated_lst_of_column_names = info.values_url
                dct_of_column_names = {}
                for column_name in lst_of_column_names:
                    # Transpose a df column into a dct with courses as key and sort it by value
                    if column_name in df:
                        dct = df.set_index(FileNameConsts.df_index)[column_name].to_dict()
                    else:
                        # Raise an error if column_name does not exist as a column in df
                        message = f"Filter list creator; {column_name} not found in df!"
                        Utils.logger(message, "warning", FileNameConsts.format_log_name)
                        dct = {}
                    # For each course in df's column_name, if value == 1, append it to list
                    lst_of_courses_with_val_1 = []
                    for course in dct.keys():
                        if dct[course] == 1:
                            lst_of_courses_with_val_1.append(course)
                    column_name_translations = dict(zip(lst_of_column_names, translated_lst_of_column_names))
                    # Make sure values_df is the same length as values_url, otherwise the translation above will fail
                    if len(lst_of_column_names) != len(translated_lst_of_column_names):
                        print(f"Error, {len(lst_of_column_names)} != {len(translated_lst_of_column_names)}: Go to info_consts file and ensure that values_df is the same length as values_url. First element: {lst_of_column_names[0]}, {translated_lst_of_column_names[0]}")
                    translated_column_name = column_name_translations[column_name]
                    dct_of_column_names[translated_column_name] = lst_of_courses_with_val_1
                filter_dct[info.key_url] = dct_of_column_names
        # save as JSON
        json_name  = WebsiteConsts.json_filter_dct
        path_and_file_name = FileNameConsts.path_of_pkl + json_name + '.json'
        with open(path_and_file_name, 'w') as fp:
            json.dump(filter_dct, fp)
        print(f"The dictionary {json_name}.json has been saved...")


#%%
if __name__ == "__main__":
    #CsvCreator.quick_test_for_debugging_please_ignore()
    CsvCreator.create_csv()