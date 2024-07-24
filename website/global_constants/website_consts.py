

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