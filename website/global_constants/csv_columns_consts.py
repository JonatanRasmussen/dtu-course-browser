import json
from website.global_constants.config import Config
from website.global_constants.eval_consts import EvalConsts
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.grade_consts import GradeConsts
from website.global_constants.info_consts import InfoConsts
from utils import Utils

class CsvColumnConsts:
    # Initialization
    COURSE = FileNameConsts.df_index
    NAME = InfoConsts.name_english

    SEMESTER_ELEMENTS = [GradeConsts.students_total, GradeConsts.grade_average, GradeConsts.percent_failed,
                        GradeConsts.grade_12, GradeConsts.grade_10, GradeConsts.grade_7, GradeConsts.grade_4,
                        GradeConsts.grade_02, GradeConsts.grade_00, GradeConsts.grade_minus_3,
                        EvalConsts.learning_votes, EvalConsts.workload_average_score, EvalConsts.learning_average_score,
                        EvalConsts.motivation_average_score, EvalConsts.feedback_average_score]

    #  If adding a new column_name, be sure to add it to format info script as well!
    PREMADE_COLUMNS = [  # BASIC_COLUMNS
        InfoConsts.danish_name.key_df, InfoConsts.language.key_df, InfoConsts.ects_points.key_df, InfoConsts.course_type.key_df,
        GradeConsts.students_per_semester, InfoConsts.semester_period.key_df, InfoConsts.exam_type.key_df,
        InfoConsts.assignments.key_df, InfoConsts.time_of_week.key_df, InfoConsts.last_updated.key_df
    ] + [  # GRADE_COLUMNS
        GradeConsts.grade_12, GradeConsts.grade_10, GradeConsts.grade_7, GradeConsts.grade_4, GradeConsts.grade_02,
        GradeConsts.grade_00, GradeConsts.grade_minus_3, GradeConsts.grade_passed, GradeConsts.grade_failed,
        GradeConsts.grade_absent, GradeConsts.grade_average, GradeConsts.students_total, GradeConsts.percent_passed,
        GradeConsts.percent_failed, GradeConsts.percent_absent
    ] + [  # GRADE_COLUMNS
        GradeConsts.grade_12, GradeConsts.grade_10, GradeConsts.grade_7, GradeConsts.grade_4, GradeConsts.grade_02,
        GradeConsts.grade_00, GradeConsts.grade_minus_3, GradeConsts.grade_passed, GradeConsts.grade_failed,
        GradeConsts.grade_absent, GradeConsts.grade_average, GradeConsts.students_total, GradeConsts.percent_passed,
        GradeConsts.percent_failed, GradeConsts.percent_absent
    ] + [  # EVAL_COLUMNS
        EvalConsts.rating_tier, EvalConsts.rating_average_score, EvalConsts.rating_votes,
        EvalConsts.learning_tier, EvalConsts.learning_average_score, EvalConsts.learning_votes,
        EvalConsts.motivation_tier, EvalConsts.motivation_average_score, EvalConsts.motivation_votes,
        EvalConsts.feedback_tier, EvalConsts.feedback_average_score, EvalConsts.feedback_votes,
        EvalConsts.workload_tier, EvalConsts.workload_average_score, EvalConsts.workload_votes,
        EvalConsts.workload_4_star, EvalConsts.workload_5_star
    ] + [  # RESPONSIBLE_COLUMNS
        InfoConsts.main_responsible_name.key_df, InfoConsts.main_responsible_pic.key_df,
        InfoConsts.co_responsible_1_name.key_df, InfoConsts.co_responsible_1_pic.key_df,
        InfoConsts.co_responsible_2_name.key_df, InfoConsts.co_responsible_2_pic.key_df,
        InfoConsts.co_responsible_3_name.key_df, InfoConsts.co_responsible_3_pic.key_df,
        InfoConsts.co_responsible_4_name.key_df, InfoConsts.co_responsible_4_pic.key_df
    ] + [  # CONTENT_COLUMNS
        InfoConsts.course_description.key_df, InfoConsts.scope_and_form.key_df, (InfoConsts.exam_type.key_df)+'_'+InfoConsts.raw_key,
        (InfoConsts.exam_aid.key_df)+'_'+InfoConsts.raw_key, (InfoConsts.location.key_df)+'_'+InfoConsts.raw_key,
        InfoConsts.time_of_week_updated.key_df, InfoConsts.exam_duration.key_df, InfoConsts.home_page.key_df,
        InfoConsts.learning_objectives.key_df, InfoConsts.course_content.key_df, InfoConsts.remarks.key_df,
        InfoConsts.old_recommended_prerequisites.key_df, InfoConsts.recommended_prerequisites.key_df,
        InfoConsts.mandatory_prerequisites.key_df, InfoConsts.highlighted_message.key_df,
        InfoConsts.study_lines.key_df, GradeConsts.semesters_total, InfoConsts.institute.key_df
    ] + Utils.generate_columns(Config.course_semesters, SEMESTER_ELEMENTS, add_index = False)

    # A few years ago some friends asked me for specific data for a course planner project. These columns were used for that.S
    COLUMNS_TO_COPY_OVER = [COURSE, NAME, InfoConsts.danish_name.key_df, InfoConsts.language.key_df, InfoConsts.ects_points.key_df,
                            InfoConsts.course_type.key_df, InfoConsts.exam_type.key_df, InfoConsts.time_of_week.key_df,
                            InfoConsts.course_duration.key_df, InfoConsts.exam_aid.key_df, InfoConsts.examiner.key_df, InfoConsts.assignments.key_df,
                            InfoConsts.grade_type.key_df, InfoConsts.location.key_df, InfoConsts.semester_period.key_df,
                            InfoConsts.main_responsible_name.key_df, InfoConsts.co_responsible_1_name.key_df, InfoConsts.co_responsible_2_name.key_df,
                            InfoConsts.co_responsible_3_name.key_df, InfoConsts.co_responsible_4_name.key_df, InfoConsts.study_lines.key_df,
                            GradeConsts.grade_average, GradeConsts.percent_passed, GradeConsts.students_total, EvalConsts.workload_average_score,
                            EvalConsts.learning_average_score, EvalConsts.motivation_average_score, EvalConsts.feedback_average_score]