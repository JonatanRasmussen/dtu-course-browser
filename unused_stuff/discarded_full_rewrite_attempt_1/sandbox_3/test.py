from abc import ABC, abstractmethod
from typing import Dict, List, Union, Tuple, Type, Callable, TypeVar, Generic, cast
import json

class DataObject(ABC):

    KEY_SEPARATOR: str = "__"

    def __init__(self, domain: str, time_period: str, name: str) -> None:
        self.domain: str = domain
        self.time_period: str = time_period
        self.name: str = name

    def get_name(self) -> str:
        return self.name

    def serialize(self) -> str:
        domain_name: str = self.domain
        time_name: str = self.time_period
        class_id: str = self.get_class_id()
        name: str = self.get_name()
        sep: str = DataObject.KEY_SEPARATOR
        return domain_name + sep + time_name + sep + class_id + sep + name

    @staticmethod
    @abstractmethod
    def get_class_id() -> str:
        pass

class Container(DataObject):

    def __init__(self, domain: str, time_period: str, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.children: Dict[str,List[DataObject]] = {}

    def _add_child(self, child: 'DataObject') -> None:
        key: str = child.get_class_id()
        self.children[key].append(child)

    def get_children(self, key) -> List['DataObject']:
        return self.children[key]

    def get_primary_children(self) -> List[DataObject]:
        lst_of_children: List[DataObject] = []
        lst_of_keys = self._get_primary_child_class_keys()
        for key in lst_of_keys:
            if key in self.children:
                lst_of_children.extend(self.children[key])
        return lst_of_children

    def _get_primary_child_class_keys(self) -> List[str]:
        main_child_classes: List[Type[Container]] = self.get_primary_child_classes()
        lst_of_keys: List[str] = []
        for main_child_class in main_child_classes:
            lst_of_keys.append(main_child_class.get_class_id())
        return lst_of_keys

    @staticmethod
    def _get_all_child_classes() -> List[Type[DataObject]]:
        return Container.get_primary_child_classes() + Container.get_secondary_child_classes()

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return []

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return []

class DataPoint(DataObject):

    def __init__(self, domain: str, time_period: str, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.data: Dict[str,str] = {}

class School(Container):

    CLASS_ID: str = "school"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Year]

class Year(Container):

    CLASS_ID: str = "year"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Course]

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return [StudyLine, Teacher]

class Course(Container):

    CLASS_ID: str = "course"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Term]

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return [InfoPage]

class Term(Container):

    CLASS_ID: str = "term"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_secondary_child_classes() -> List[Type[DataObject]]:
        return [Evaluation, GradeSheet]

class Teacher(Container):

    CLASS_ID: str = "teacher"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Course]

class StudyLine(Container):

    CLASS_ID: str = "study_line"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

    @staticmethod
    def get_primary_child_classes() -> List[Type['Container']]:
        return [Course]

class Evaluation(DataPoint):

    CLASS_ID: str = "evaluation"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class GradeSheet(DataPoint):

    CLASS_ID: str = "grade_sheet"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID

class InfoPage(DataPoint):

    CLASS_ID: str = "info_page"

    @staticmethod
    def get_class_id() -> str:
        return School.CLASS_ID