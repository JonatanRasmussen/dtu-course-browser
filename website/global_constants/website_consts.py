import json
from website.global_constants.eval_consts import EvalConsts
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.grade_consts import GradeConsts
from website.global_constants.info_consts import InfoConsts

class WebsiteConsts:

    # Sort by
    sort_by = "sort_by"
    sort_reverse = "sort_reverse"
    url_arg_key = "args"

    # Browse page
    name = 'name'
    ects = 'ects'
    language = 'language'
    course_type = 'course_type' #UPDATE
    season = 'season'
    schedule = 'schedule'
    signups = 'signups'
    grade = 'grade'
    fail = 'fail'
    exam = 'exam'
    workload = 'workload'
    rating = 'rating'
    workload_tier = 'workload_tier'
    rating_tier = 'rating_tier'
    votes = 'votes'
    responsible = 'responsible'

    # Filter
    json_filter_dct = "json_filter_dct"

    # Json dict names
    json_number = "course_numbers"
    json_name_english = "course_english_names"
    json_course_data = "course_data"
    json_course_ects = "course_ects"
    json_course_type = "course_type"
    json_course_language = "course_language"
    json_course_season = "course_season"
    json_course_schedule = "course_schedule"
    json_course_signups = "course_signups"
    json_course_grade = "course_grade"
    json_course_fail = "course_fail"
    json_course_exam = "course_exam"
    json_course_workload = "course_workload"
    json_course_rating = "course_rating"
    json_course_workload_tier = "course_workload_tier"
    json_course_rating_tier = "course_rating_tier"
    json_course_votes = "course_votes"
    json_course_responsible = "course_responsible"
    json_course_eval_learning = "course_eval_learning"
    json_course_eval_motivation = "course_eval_motivation"
    json_course_eval_feedback = "course_eval_feedback"

    # Sorting courses in numerical/alphabetic order
    # Boolean states if list should be reversed (top grades first, low grades last)
    json_as_sort_catagory ={json_number: False,
                            json_name_english: False,
                            json_course_ects: True,
                            json_course_type: False,
                            json_course_language: False,
                            json_course_season: False,
                            json_course_schedule: False,
                            json_course_signups: True,
                            json_course_grade: True,
                            json_course_fail: True,
                            json_course_exam: False,
                            json_course_workload: True,
                            json_course_rating: True,
                            json_course_workload_tier: True,
                            json_course_rating_tier: True,
                            json_course_votes: True,
                            json_course_responsible: False,
                            json_course_eval_learning: True,
                            json_course_eval_motivation: True,
                            json_course_eval_feedback: True}

    # Format info rename values
    no_data = "No data"
    shortened_no_evaluations = "–"
    shortened_no_grades = "–"
    shortened_pass_fail = "P/F"
    shortened_autumn = "Fall"
    shortened_written_oral = "Oral exam"
    multiple_unknowns = "Multi_Unknown"
    multiple_timeslots = "2+ Timeslots"
    exam_project = "Exam project"

    # Course page
    semester_name = "SEMESTER_NAME"

    # Last updated
    last_updated = "last_updated"
    current_year = "current_year"

    @staticmethod
    def create_website_data_dct(df):
        """Turn csv columns into dictionary files stored in jsons"""
        # This jsons are the database that gets accessed whenever the "discovery" page (home page) is loaded.

        empty_json_name = ""
        json_data = {
            WebsiteConsts.json_name_english: WebsiteConsts._create_dct_as_json(df, InfoConsts.name_english, empty_json_name),
            WebsiteConsts.json_course_ects: WebsiteConsts._create_dct_as_json(df, InfoConsts.ects_points.key_df, empty_json_name),
            WebsiteConsts.json_course_type: WebsiteConsts._create_dct_as_json(df, InfoConsts.course_type.key_df, empty_json_name),
            WebsiteConsts.json_course_language: WebsiteConsts._create_dct_as_json(df, InfoConsts.language.key_df, empty_json_name),
            WebsiteConsts.json_course_season: WebsiteConsts._create_dct_as_json(df, InfoConsts.semester_period.key_df, empty_json_name),
            WebsiteConsts.json_course_schedule: WebsiteConsts._create_dct_as_json(df, InfoConsts.time_of_week.key_df, empty_json_name),
            WebsiteConsts.json_course_signups: WebsiteConsts._create_dct_as_json(df, GradeConsts.students_per_semester, empty_json_name),
            WebsiteConsts.json_course_grade: WebsiteConsts._create_dct_as_json(df, GradeConsts.grade_average, empty_json_name),
            WebsiteConsts.json_course_fail: WebsiteConsts._create_dct_as_json(df, GradeConsts.percent_failed, empty_json_name),
            WebsiteConsts.json_course_exam: WebsiteConsts._create_dct_as_json(df, InfoConsts.exam_type.key_df, empty_json_name),
            WebsiteConsts.json_course_workload: WebsiteConsts._create_dct_as_json(df, EvalConsts.workload_average_score, empty_json_name),
            WebsiteConsts.json_course_rating: WebsiteConsts._create_dct_as_json(df, EvalConsts.rating_average_score, empty_json_name),
            WebsiteConsts.json_course_workload_tier: WebsiteConsts._create_dct_as_json(df, EvalConsts.workload_tier, empty_json_name),
            WebsiteConsts.json_course_rating_tier: WebsiteConsts._create_dct_as_json(df, EvalConsts.rating_tier, empty_json_name),
            WebsiteConsts.json_course_votes: WebsiteConsts._create_dct_as_json(df, EvalConsts.motivation_votes, empty_json_name),
            WebsiteConsts.json_course_responsible: WebsiteConsts._create_dct_as_json(df, InfoConsts.main_responsible_pic.key_df, empty_json_name),
            WebsiteConsts.json_course_eval_learning: WebsiteConsts._create_dct_as_json(df, EvalConsts.learning_average_score, empty_json_name),
            WebsiteConsts.json_course_eval_motivation: WebsiteConsts._create_dct_as_json(df, EvalConsts.motivation_average_score, empty_json_name),
            WebsiteConsts.json_course_eval_feedback: WebsiteConsts._create_dct_as_json(df, EvalConsts.feedback_average_score, empty_json_name)
        }
        return json_data

    @staticmethod
    def _create_dct_as_json(df, column, json_name):
        """Load a column from csv as dictionary and save it as json"""

        def _turn_to_float(item):
            if ((column == GradeConsts.grade_average) or
                (column == GradeConsts.percent_failed) or
                (column == EvalConsts.workload_average_score) or
                (column == EvalConsts.rating_average_score) or
                (column == EvalConsts.learning_average_score) or
                (column == EvalConsts.motivation_average_score) or
                (column == EvalConsts.feedback_average_score)):
                if isinstance(item, str):
                    return -0.1
            elif (column == InfoConsts.main_responsible_pic.key_df):
                return str(item)
            return item

        dct = df.to_dict()[column]
        dct_data = WebsiteConsts.rename_dct_value(dct, column)
        sorted_dct = dict(sorted(dct_data.items(), key=lambda item: _turn_to_float(item[1]))) # Be careful, this line will do absolutely nothing WITHOUT RAISING A WARNING if dct_data contains a mix of strings and numbers
        if json_name != "":
            path_and_file_name = FileNameConsts.path_of_pkl + json_name + '.json'
            with open(path_and_file_name, 'w') as fp:
                json.dump(sorted_dct, fp)
            print(f"The dictionary {json_name}.json has been saved...")
        return sorted_dct

    @staticmethod
    def _rename_dct_value(dct, column):
        """Loop through dct and rename certain values so they fit the cards on the home page"""
        if column == InfoConsts.course_type.key_df:
            for key in dct:
                if dct[key] == InfoConsts.bsc + InfoConsts.separator_plus + InfoConsts.msc:
                    dct[key] = InfoConsts.bsc+"/"+InfoConsts.msc
                elif dct[key] == InfoConsts.deltidsmaster:
                    dct[key] = InfoConsts.msc
                elif dct[key] == InfoConsts.deltidsdiplom:
                    dct[key] = InfoConsts.beng
        elif column == InfoConsts.semester_period.key_df:
            for key in dct:
                if dct[key] == "Autumn":
                    dct[key] = WebsiteConsts.shortened_autumn
                elif dct[key] == InfoConsts.not_yet_assigned_value or dct[key] == InfoConsts.unknown_value:
                    dct[key] = WebsiteConsts.no_data
                elif dct[key] == "January" or dct[key] == "June" or dct[key] == "July" or dct[key] == "August" or dct[key] == "Spring":
                    pass
                else:
                    dct[key] = WebsiteConsts.multiple_timeslots
        elif column == InfoConsts.time_of_week.key_df:
            for key in dct: # Do not touch these, it will break stuff
                if dct[key] == "E1A (Autumn, Mon 8-12)" or dct[key] == "F1A (Spring, Mon 8-12)":
                    dct[key] = "Mon_8_12" # Do not touch these, it will break stuff
                elif dct[key] == "E1B (Autumn, Thurs 13-17)" or dct[key] == "F1B (Spring, Thurs 13-17)":
                    dct[key] = "Thurs_13_17"
                elif dct[key] == "E2A (Autumn, Mon 13-17)" or dct[key] == "F2A (Spring, Mon 13-17)":
                    dct[key] = "Mon_13_17"
                elif dct[key] == "E2B (Autumn, Thurs 8-12)" or dct[key] == "F2B (Spring, Thurs 8-12)":
                    dct[key] = "Thurs_8_12"
                elif dct[key] == "E3A (Autumn, Tues 8-12)" or dct[key] == "F3A (Spring, Tues 8-12)":
                    dct[key] = "Tues_8_12"
                elif dct[key] == "E3B (Autumn, Fri 13-17)" or dct[key] == "F3B (Spring, Fri 13-17)":
                    dct[key] = "Fri_13_17"
                elif dct[key] == "E4A (Autumn, Tues 13-17)" or dct[key] == "F4A (Spring, Tues 13-17)":
                    dct[key] = "Tues_13_17"
                elif dct[key] == "E4B (Autumn, Fri 8-12)" or dct[key] == "F4B (Spring, Fri 8-12)":
                    dct[key] = "Fri_8_12"
                elif dct[key] == "E5A (Autumn, Wed 8-12)" or dct[key] == "F5A (Spring, Wed 8-12)":
                    dct[key] = "Wed_8_12"
                elif dct[key] == "E5B (Autumn, Wed 13-17)" or dct[key] == "F5B (Spring, Wed 13-17)":
                    dct[key] = "Wed_13_17"
                elif dct[key] == "E7 (Autumn, Tues 18-22)" or dct[key] == "F7 (Spring, Tues 18-22)":
                    dct[key] = "Tues_18_22"
                elif dct[key] == "E1A (Autumn, Mon 8-12)<br />E1B (Autumn, Thurs 13-17)" or dct[key] == "F1A (Spring, Mon 8-12)<br />F1B (Spring, Thurs 13-17)":
                    dct[key] = "Multi_Mon_8_12_Thurs_13_17"
                elif dct[key] == "E2A (Autumn, Mon 13-17)<br />E2B (Autumn, Thurs 8-12)" or dct[key] == "F2A (Spring, Mon 13-17)<br />F2B (Spring, Thurs 8-12)":
                    dct[key] = "Multi_Mon_13_17_Thurs_8_12"
                elif dct[key] == "E3A (Autumn, Tues 8-12)<br />E3B (Autumn, Fri 13-17)" or dct[key] == "F3A (Spring, Tues 8-12)<br />F3B (Spring, Fri 13-17)":
                    dct[key] = "Multi_Tues_8_12_Fri_13_17"
                elif dct[key] == "E4A (Autumn, Tues 13-17)<br />E4B (Autumn, Fri 8-12)" or dct[key] == "F4A (Spring, Tues 13-17)<br />F4B (Spring, Fri 8-12)":
                    dct[key] = "Multi_Tues_13_17_Fri_8_12"
                elif dct[key] == "E5A (Autumn, Wed 8-12)<br />E5B (Autumn, Wed 13-17)" or dct[key] == "F5A (Spring, Wed 8-12)<br />F5B (Spring, Wed 13-17)":
                    dct[key] = "Multi_Wed_8_12_Wed_13_17"
                else:
                    dct[key] = WebsiteConsts.multiple_unknowns
        elif column == GradeConsts.grade_average or column == EvalConsts.workload_average_score or column == EvalConsts.rating_average_score or column == EvalConsts.learning_average_score or column == EvalConsts.motivation_average_score or column == EvalConsts.feedback_average_score:
            for key in dct:
                if dct[key] == GradeConsts.pass_fail:
                    dct[key] = WebsiteConsts.shortened_pass_fail
                elif dct[key] == GradeConsts.grade_none:
                    dct[key] = WebsiteConsts.shortened_no_grades
                elif dct[key] == EvalConsts.no_evaluations:
                    dct[key] = WebsiteConsts.shortened_no_evaluations
                else:
                    try:
                        dct[key] = round(float(dct[key]), 1)
                    except (ValueError, TypeError):
                        print(f"Warning: {dct[key]} was expected to be numeric, yet it could not be rounded!")
        elif column == GradeConsts.percent_failed:
            for key in dct:
                if dct[key] == GradeConsts.grade_none:
                    dct[key] = "0"
                else:
                    try:
                        if float(dct[key]) < 10:
                            dct[key] = round(float(dct[key]), 1)
                        else:
                            dct[key] = int(round(float(dct[key]), 0))
                    except (ValueError, TypeError):
                        print(f"Warning: {dct[key]} was expected to be numeric, yet it could not be rounded!")
        elif column == InfoConsts.exam_type.key_df:
            for key in dct:
                if dct[key] == InfoConsts.exam_both:
                    dct[key] = WebsiteConsts.shortened_written_oral
                elif (dct[key] == InfoConsts.exam_none) or (dct[key] == InfoConsts.unknown_value):
                    dct[key] = WebsiteConsts.exam_project
        return dct