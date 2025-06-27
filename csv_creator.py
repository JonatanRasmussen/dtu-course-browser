#%%

import pandas as pd
import json

from format_evaluations import EvalFormatter
from format_grades import GradeFormatter
from format_info import InfoFormatter
from format_study_lines import create_teacher_course_lst
from utils import Utils
from website.global_constants import website_consts
from website.global_constants.config import Config
from website.global_constants.csv_columns_consts import CsvColumnConsts
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
    def load_course_dict_from_disk_and_create_csv():
        with open(FileNameConsts.scraped_data_folder_name+'/'+FileNameConsts.course_number_json+'.json') as f:
            course_dict = json.load(f)
        CsvCreator.create_csv(course_dict)

    @staticmethod
    def create_csv(course_dict):
        """ Clean, format and parse the scraped_data into a csv and other files used by my website """

        name_and_path_of_csv = FileNameConsts.path_of_csv + FileNameConsts.name_of_csv + ".csv"
        name_and_path_of_pkl = FileNameConsts.path_of_pkl + FileNameConsts.name_of_pkl + ".pkl"
        print()
        print("Part 1 of 3: Creating csv file with specified columns: "+name_and_path_of_csv)
        print()
        premade_columns = CsvColumnConsts.PREMADE_COLUMNS
        premade_columns_df = CsvCreator._build_combined_df(course_dict, name_and_path_of_csv, premade_columns)
        print(f"Success! Saving df {name_and_path_of_csv} to both csv and pickle format...")
        premade_columns_df.to_csv(name_and_path_of_csv, index = False, header=True)
        premade_columns_df.to_pickle(name_and_path_of_pkl)

        name_and_path_of_extended_csv = FileNameConsts.path_of_csv + FileNameConsts.extended_csv_name + ".csv"
        name_and_path_of_extended_pkl = FileNameConsts.path_of_csv + FileNameConsts.extended_pkl_name + ".pkl"
        print()
        print("Part 2 of 3: Creating extended csv file with all columns: "+name_and_path_of_extended_csv)
        print()
        no_premade_columns = []
        all_columns_df = CsvCreator._build_combined_df(course_dict, name_and_path_of_extended_csv, no_premade_columns)
        print()
        print(f"Success! Saving df {name_and_path_of_csv} to both csv and pickle format...")
        all_columns_df.to_csv(name_and_path_of_extended_csv, index = False, header=True)
        all_columns_df.to_pickle(name_and_path_of_extended_pkl)

        print()
        print("Part 3 of 3: Creating json files used for website search and filter functionality...")
        print()
        if premade_columns != []:
            #save specific columns as json dct that are used by the website
            WebsiteConsts.create_website_data_dct(premade_columns_df)  # Use premade column df
        else:
            print()
            CsvCreator._filter_dct_to_json(all_columns_df)  # Use all columns df
            print()

        # Success!
        print("Success! Program will now terminate.")

    @staticmethod
    def _build_combined_df(course_dict, file_name, premade_columns):
        """Create and save .csv file with data for all courses"""
        course_numbers = list(course_dict.keys())
        course_names = list(course_dict.values())
        grade_df = Utils.load_scraped_df(FileNameConsts.grade_df)
        eval_df = Utils.load_scraped_df(FileNameConsts.eval_df)
        info_df = Utils.load_scraped_df(FileNameConsts.info_df)
        # Adding data dicts to the data frame, one course at a time
        semesters = Config.course_semesters
        column_names = []  # Create list with column names, this will be the data frame columns
        for i in range (0, len(course_numbers)):
            grades_formatted_dct = GradeFormatter.format_grades(grade_df, course_numbers[i], semesters)
            evals_formatted_dct = EvalFormatter.format_evaluations(eval_df, course_numbers[i], semesters)
            info_formatted_dct = InfoFormatter.format_info(info_df, course_numbers[i])
            data_dct = {**grades_formatted_dct, **evals_formatted_dct, **info_formatted_dct}
            if i == 0:  # Initialize columns
                if premade_columns == []:  # Create a column for all keys in data_dct if no premade columns exist
                    column_names = [FileNameConsts.df_index] + [InfoConsts.name_english] + list(data_dct.keys())
                else:
                    column_names = [FileNameConsts.df_index] + [InfoConsts.name_english] + premade_columns
            for i in range (0, len(course_numbers)):
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
            Utils.display_progress(i, course_numbers, file_name, 50)  # Display progress to user
        CsvCreator.build_df(course_numbers, course_names, file_name, premade_columns, data_dct)
        df = df.copy() # df is copied to 'fix fragmentation', which prevents an annoying pandas PerformanceWarning that is polluting the terminal
        df.set_index(FileNameConsts.df_index, inplace=True, drop=False)  # Set course ID as df index
        print(df)
        if (InfoConsts.main_responsible_name.key_df) in premade_columns or premade_columns == []:
            df = create_teacher_course_lst(df, course_numbers)  # Append columns containing each responsibles' course list. Must be done after rest of the df is finalized
        return df

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
    CsvCreator.load_course_dict_from_disk_and_create_csv()