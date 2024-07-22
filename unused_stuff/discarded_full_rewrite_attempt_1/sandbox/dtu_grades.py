from grade import Grade


class DtuGrades:
    """ Grade distribution across DTU's different types of grades """

    # CONSTANTS
    _12 = "12"
    _10 = "10"
    _7 = "7"
    _4 = "4"
    _02 = "02"
    _00 = "00"
    _MINUS_3 = "-3"
    _PASS = "pass"
    _FAIL = "fail"
    _ABSENT = "absent"
    _ILL = "ill"
    _NOT_APPROVED = "not_approved"

    @staticmethod
    def generate_grades() -> dict[str:'Grade']:
        grades: dict['Grade'] = {}
        # Numeric grades (seven-step scale)
        grades[DtuGrades._12] = Grade.create_passed(DtuGrades._12, 12)
        grades[DtuGrades._10] = Grade.create_passed(DtuGrades._10, 10)
        grades[DtuGrades._7] = Grade.create_passed(DtuGrades._7, 7)
        grades[DtuGrades._4] = Grade.create_passed(DtuGrades._4, 4)
        grades[DtuGrades._02] = Grade.create_passed(DtuGrades._02, 2)
        grades[DtuGrades._00] = Grade.create_attended_but_failed(DtuGrades._00, 0)
        grades[DtuGrades._MINUS_3] = Grade.create_attended_but_failed(DtuGrades._MINUS_3, -3)
        # Non-numeric grades (Custom grades used at DTU)
        grades[DtuGrades._PASS] = Grade.create_passed(DtuGrades._PASS, None)
        grades[DtuGrades._FAIL] = Grade.create_attended_but_failed(DtuGrades._FAIL, None)
        grades[DtuGrades._ABSENT] = Grade.create_absent(DtuGrades._ABSENT)
        grades[DtuGrades._ILL] = Grade.create_absent(DtuGrades._ILL)
        grades[DtuGrades._NOT_APPROVED] = Grade.create_absent(DtuGrades._NOT_APPROVED)
        return grades