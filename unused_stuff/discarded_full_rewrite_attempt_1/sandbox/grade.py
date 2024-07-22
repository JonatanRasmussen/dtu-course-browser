from typing import Union


class Grade:
    """ Grade datatype. Contains the following info:
        - Str: The name of the grade
        - Int: The 'quantity' (Number of students that have received the grade)
        - Int: The numerical weight of the grade (can also be None)
        - Bool: The 'attended' value ('True' if it counts as exam attendance)
        - Bool: The 'passed' value ('True' if it counts as passing the exam) """

    #CONSTRUCTOR
    def __init__(self, name: str, weight: Union(int, None), attended: bool, passed: bool) -> 'Grade':
        """ NOTE: Use one of the classmethods to instantiate """
        self._name: bool = name
        self._numeric_weight: Union(int, None) = weight
        self._counts_as_exam_attendance: bool = attended
        self._passes_exam: bool = passed
        self._quantity: int = 0

    @classmethod
    def create_passed(cls: 'Grade', name: str, weight: int) -> 'Grade':
        """ Instantiate a grade for when the exam was attended and passed """
        attended = True
        passed = True
        return Grade(name, weight, attended, passed)

    @classmethod
    def create_absent(cls: 'Grade', name: str) -> 'Grade':
        """ Instantiate a grade for when the exam was not attended (and thereby failed) """
        weight = None
        attended = False
        passed = False
        return Grade(name, weight, attended, passed)

    @classmethod
    def create_attended_but_failed(cls: 'Grade', name: str, weight: int) -> 'Grade':
        """ Instantiate a grade for when the exam was attended but failed """
        attended = True
        passed = False
        return Grade(name, weight, attended, passed)

    #GETTER
    def passes_exam(self: 'Grade') -> bool:
        """ Returns 'True' if the grade passes the exam
            Returns 'False' if the grade does not pass the exam """
        return self._passes_exam

    #GETTER
    def counts_as_exam_attendance(self: 'Grade') -> bool:
        """ Returns 'True' if the grade counts as attending the exam
            Returns 'False' if the grade counts as absence from the exam """
        return self._counts_as_exam_attendance

    #GETTER
    def is_numeric(self: 'Grade') -> bool:
        """ Returns 'True' if the grade has a numeric representation
            Returns 'False' if the grade isn't a number """
        if self._numeric_weight is not None:
            return True
        else:
            return False

    #GETTER
    def get_quantity(self: 'Grade') -> int:
        """ GET the amount of students that have received the grade """
        return self._quantity

    #SETTER
    def set_quantity(self: 'Grade', new_quantity: int) -> None:
        """ SET the amount of students that have received the grade """
        self._quantity = new_quantity

    #GETTER
    def get_name(self: 'Grade') -> bool:
        """ Return the name of the grade """
        return self._name

    #GETTER
    def get_numeric_weight(self: 'Grade') -> Union(int, None):
        """ If the grade is numeric, return its numeric weight
            If the grade is not numeric, return 'None' """
        return self._numeric_weight