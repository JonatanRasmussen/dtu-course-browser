def convert_semester_to_exam_period(semester):
    if semester[0] == 'F': #F stands for Forår, and "Summer" is the corresponding exam period
        return f'Summer-20{semester[-2:]}'
    elif semester[0] == 'E': #E stands for Efterår, and "Winter" is the corresponding exam period
        return f'Winter-20{semester[-2:]}'
    else:
        raise Exception(f"Error, invalid semester: {semester}")


def get_url_for_grade(course, semester):
    exam_period = convert_semester_to_exam_period(semester)
    url = f'https://karakterer.dtu.dk/Histogram/1/{course}/{exam_period}'
    return url