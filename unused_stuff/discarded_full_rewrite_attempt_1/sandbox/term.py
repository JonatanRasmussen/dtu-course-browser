class Term:
    """ A class to handle the relation between DTU's semesters,
        academic years and exam periods. It was initially designed
        as a data type to be used in other scripts, but I ended
        up representing terms via strings throughout the project.
        Only within this class is Term used as a data type """

    def __init__(self: 'Term', calender_year: int, semester: str) -> 'Term':
        self._YEAR: int = calender_year # 2014, 2019, 2023, etc.
        self._SEMESTER: str = semester # E (Efterår) or F (Forår)
        self._validate_year()
        self._validate_semester()

    @classmethod
    def from_string(cls: 'Term', term_as_string: str) -> 'Term':
        if len(term_as_string) == 3 and term_as_string[1:3].isdigit():
            dtu_semester: str = term_as_string[0]
            calender_year: int = 2000 + int(term_as_string[1:3])
            return cls(calender_year, dtu_semester)
        else:
            raise ValueError(f"Invalid term: {term_as_string}")

    @staticmethod
    def validate_string(term_as_string: str) -> str:
        term: 'Term' = Term.from_string(term_as_string)
        return term.get_term_name()

    @staticmethod
    def get_exam_period_from_str(term_as_string: str) -> str:
        term: 'Term' = Term.from_string(term_as_string)
        return term.get_exam_period()

    @staticmethod
    def get_academic_year_from_str(term_as_string: str) -> str:
        term: 'Term' = Term.from_string(term_as_string)
        return term.get_academic_year()

    @staticmethod
    def convert_term_names_to_academic_years(terms: list[str]) -> list[str]:
        academic_years_set: set[str] = set()
        for term_as_string in terms:
            term: 'Term' = Term.from_string(term_as_string)
            academic_years_set.add(term.get_academic_year())
        academic_years_list: list[str] = list(academic_years_set)
        return academic_years_list

    def get_term_name(self: 'Term'):
        YEAR_LOWER_BOUND: int = 2000
        if self._YEAR > YEAR_LOWER_BOUND:
            return f'{self._SEMESTER}{self._YEAR-2000}'
        else:
            assert False, f"Invalid term: {self._YEAR-2000}{self._SEMESTER}"

    def get_exam_period(self: 'Term'):
        if self._SEMESTER == 'E':
            return f'Winter-{self._YEAR}'
        elif self._SEMESTER == 'F':
            return f'Summer-{self._YEAR}'
        else:
            assert False, f"Invalid term: {self._YEAR-2000}{self._SEMESTER}"

    def get_academic_year(self: 'Term') -> str:
        if self._SEMESTER == 'E':
            return f'{self._YEAR}-{1 + self._YEAR}'
        elif self._SEMESTER == 'F':
            return f'{self._YEAR - 1}-{self._YEAR}'
        else:
            assert False, f"Invalid term: {self._YEAR-2000}{self._SEMESTER}"

    def _validate_year(self: 'Term'):
        """ The term year should be in-between 2000 and 2059 """
        LOWER_BOUND: int = 2000 # Years 19XX break the shortened names E16 / F18 / E21 / F23 / etc.
        UPPER_BOUND: int = 2059 # 2060 and 1960 might collide when shortened to F60 or E60
        if (self._YEAR < LOWER_BOUND) or (self._YEAR > UPPER_BOUND):
            raise ValueError("CustomError: Invalid year, outside of "+
                            f"bounds:{LOWER_BOUND} - {UPPER_BOUND}")

    def _validate_semester(self: 'Term'):
        """ The term semester should be E (Efterår) or F (Forår) """
        SUPPORTED_SEMESTERS: set[str] = {'E', 'F'}
        if self._SEMESTER not in SUPPORTED_SEMESTERS:
            raise ValueError("CustomError: Invalid semester, "+ 
                            f"not supported: {SUPPORTED_SEMESTERS}")


if __name__ == "__main__":
    # Test code, remove later
    my_term = Term(2020, 'E')
    my_new_term = Term(2011, 'F')
    print(my_term.get_term_name())
    print(my_term.get_exam_period())
    print(my_term.get_academic_year())
    Term.convert_term_names_to_academic_years({my_term, my_new_term})
    #my_fake_term = Term(30, 'G')