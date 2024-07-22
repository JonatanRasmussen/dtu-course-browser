from grade import Grade

class GradeSheet:
    """ Grade distribution across DTU's different types of grades """

    #CONSTRUCTOR  
    def __init__(self: 'GradeSheet', course: str, term: str, grades: dict[str:'Grade']) -> 'GradeSheet':
        """ Instantiate each grade used at DTU """
        self._course: str = course
        self._term: str = term
        self._grades: dict[str:'Grade'] = grades

    #MATH  
    def calculate_average(self: 'GradeSheet') -> float | None:
        """ Calculate the mean of the numeric grades
            Return 'None' if there are no numeric grades """
        count: int = 0
        weighted_sum: int = 0
        for grade in self._grades:
            if grade.is_numeric():
                count += grade.get_quantity() 
                weighted_sum += grade.get_quantity() * grade.get_numeric_weight()
        if len(count) == 0:
            return None
        else:
            average: float = weighted_sum / len(count)
            return average

    #MATH            
    def count_grades(self: 'GradeSheet') -> int:
        """ Count the total number of grades on the grade sheet """
        count: int = 0
        for grade in self._grades:
            count += grade.get_quantity()
        return count 

    #SETTER  
    def set_grade(self: 'GradeSheet', grade_name: str, new_quantity: int) -> None:
        """ Set quantity of students that received the grade 'grade_name' """
        if grade_name in self._grades:
            self._grades[grade_name].set_quantity(new_quantity)
        else:
            raise ValueError(f"CustomError: Grade {grade_name} not found in dict: {self._grades}")

    #GETTER  
    def get_grade(self: 'GradeSheet', grade_name: str) -> None:
        """ Get quantity of students that received the grade 'grade_name' """
        if grade_name in self._grades:
            return self._grades[grade_name].get_quantity()
        else:
            raise ValueError(f"CustomError: Grade {grade_name} not found in dict: {self._grades}")


    '''def match_condition(self: 'GradeSheet', condition: any) -> int:
        """ Return the grades that are 'True' for the given condition """
        grade_list: list['Grade'] = []
        for grade in self._grades:
            if getattr(grade, condition):
                grade_list.append(grade)
        return grade_list    '''
