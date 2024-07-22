from abc import ABC, abstractmethod
from typing import Dict, List, Union, Tuple, Type, Callable, TypeVar, Generic, cast
import json

T = TypeVar('T')

class Registry(Generic[T]):

    def __init__(self) -> None:
        self.dct: Dict[str, T] = {}

    def exists(self, key: str) -> bool:
        return key in self.dct

    def read(self, key: str) -> T:
        self._raise_error_if_key_missing(key)
        return self.dct[key]

    def read_all(self) -> List[T]:
        return List(self.dct.values())

    def write_unique_key(self, key: str, value: T) -> None:
        self._raise_error_if_key_exists(key)
        self._write(key, value)

    def write_if_key_missing(self, key: str, value: T) -> None:
        if not self.exists(key):
            self._write(key, value)

    def _write(self, key: str, value: T) -> None:
        self.dct[key] = value

    def _raise_error_if_key_exists(self, key: str) -> None:
        if not self.exists(key):
            raise KeyError(f"Key '{key}' doesn't exist.")

    def _raise_error_if_key_missing(self, key: str) -> None:
        if self.exists(key):
            raise KeyError(f"Key '{key}' already exists.")

class FileAccess(Registry,Generic[T]):

    FILE_PATH: str = "json_files/"
    FILE_NAME: str = "parsed_data"

    def __init__(self) -> None:
        super().__init__()
        self.file_path: str = f"{FileAccess.FILE_PATH}{FileAccess.FILE_NAME}.json"
        self._load_from_disk()

    def _write(self, key: str, value: T) -> None:
        self.dct[key] = value
        self._save_to_disk()

    def _load_from_disk(self) -> None:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as json_file:
                self.dct = json.load(json_file)
        except FileNotFoundError:
            self.dct = {}

    def _save_to_disk(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.dct, json_file, indent=4)

class DomainAccess(Registry,Generic[T]):

    def __init__(self) -> None:
        super().__init__()
        self._initialize_domains()

    def _get_domain_configs(self) -> List[Type['DomainConfig']]:
        domain_lst: List[Type[DomainConfig]] = []
        domain_lst.append(DtuDomainConfig)
        return domain_lst

    def _initialize_domains(self) -> None:
        for domain_config in self._get_domain_configs():
            dct_key = domain_config.get_domain_name()
            domain: Domain = Domain(domain_config)
            self.dct[dct_key] = domain

class TimePeriod:

    NAME_OF_EMPTY_TIME_PERIOD: str = "timeless"

    def __init__(self, term: str | None, year: int | None) -> None:
        self.term: str | None = term
        self.year: int | None = year

    def get_name(self) -> str:
        if (self.year is None) and (self.term is None):
            return self._get_empty_name()
        elif self.year is None:
            return self._get_yearless_name()
        elif self.term is None:
            return self._get_termless_name()
        else:
            return self._get_term_and_year_name()

    def get_term(self) -> str:
        return str(self.term)

    def get_year(self) -> int:
        numeric_year: int = self._ensure_year_is_numeric()
        return numeric_year

    def _get_empty_name(self) -> str:
        return TimePeriod.NAME_OF_EMPTY_TIME_PERIOD

    def _get_yearless_name(self) -> str:
        return str(self.term)

    def _get_termless_name(self) -> str:
        return str(self.year)

    def _get_term_and_year_name(self) -> str:
        numeric_year: int = self._ensure_year_is_numeric()
        return str(self.term) + str(numeric_year - 2000)

    def _ensure_year_is_numeric(self) -> int:
        if self.year is None:
            raise ValueError(f"Time period {self.get_name()} has no year")
        return self.year

class TimeUnitChecker(ABC):

    @staticmethod
    @abstractmethod
    def is_term_based(class_id: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def is_time_based(class_id: str) -> bool:
        pass

class DefaultTimeUnitChecker(TimeUnitChecker):

    @staticmethod
    def is_term_based(class_id: str) -> bool:
        if class_id == "TODO: REMOVE":
            return True
        else:
            return False

    @staticmethod
    def is_time_based(class_id: str) -> bool:
        if class_id == School.get_class_id():
            return False
        else:
            return True

class DomainSpecificTimeConfig(ABC):

    @staticmethod
    def get_time_unit_checker() -> Type[TimeUnitChecker]:
        return DefaultTimeUnitChecker

    @staticmethod
    @abstractmethod
    def ordered_terms() -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def oldest_year() -> int:
        pass

    @staticmethod
    @abstractmethod
    def newest_year() -> int:
        pass

    @staticmethod
    @abstractmethod
    def oldest_term() -> str:
        pass

    @staticmethod
    @abstractmethod
    def newest_term() -> str:
        pass

class DtuTimeConfig(DomainSpecificTimeConfig):

    SEMESTERS: List[str] = ['F', 'E']
    OLDEST_TIME_PERIOD: TimePeriod = TimePeriod('F', 2018)
    NEWEST_TIME_PERIOD: TimePeriod = TimePeriod('E', 2023)

    @staticmethod
    def ordered_terms() -> List[str]:
        return DtuTimeConfig.SEMESTERS

    @staticmethod
    def oldest_year() -> int:
        return DtuTimeConfig.OLDEST_TIME_PERIOD.get_year()

    @staticmethod
    def newest_year() -> int:
        return DtuTimeConfig.NEWEST_TIME_PERIOD.get_year()

    @staticmethod
    def oldest_term() -> str:
        return DtuTimeConfig.OLDEST_TIME_PERIOD.get_term()

    @staticmethod
    def newest_term() -> str:
        return DtuTimeConfig.NEWEST_TIME_PERIOD.get_term()


class TimeRegistry:

    def __init__(self) -> None:
        self.time_dict: Dict[str, TimePeriod] = {}

    def get_time_from_registry(self, keyname: str) -> TimePeriod:
        if keyname not in self.time_dict:
            raise KeyError(f"{keyname} not found in {TimeRegistry.__name__} dict")
        return self.time_dict[keyname]

    def register_time(self, time_period: TimePeriod) -> None:
        self.time_dict[time_period.get_name()] = time_period

class TimePeriodGenerator:

    def __init__(self, config: Type[DomainSpecificTimeConfig]) -> None:
        self.ordered_terms: List[str] = config.ordered_terms()
        self.oldest_year: int = config.oldest_year()
        self.newest_year: int = config.newest_year()
        self.oldest_term: str = config.oldest_term()
        self.newest_term: str = config.newest_term()
        self.initialized_time_periods: TimeRegistry = TimeRegistry()

    def create_years(self) -> List[TimePeriod]:
        lst: List[TimePeriod] = []
        for year in self._calculate_years():
            time_period: TimePeriod = TimePeriod(None, year)
            self._add_to_registry(time_period)
            lst.append(time_period)
        return lst

    def create_all(self) -> List[TimePeriod]:
        lst: List[TimePeriod] = []
        for year in self._calculate_years():
            lst = lst + self.create_single_year(year)
        return lst

    def create_single_year(self, year: int) -> List[TimePeriod]:
        lst: List[TimePeriod] = []
        for term in self.ordered_terms:
            time_period: TimePeriod = TimePeriod(term, year)
            self._add_to_registry(time_period)
            lst.append(time_period)
        updated_lst: List[TimePeriod] = self._remove_invalid_terms(lst)
        return updated_lst

    def create_empty(self) -> TimePeriod:
        time_period: TimePeriod = TimePeriod(None, None)
        self._add_to_registry(time_period)
        return time_period

    def fetch_time_from_registry(self, name: str) -> TimePeriod:
        return self.initialized_time_periods.get_time_from_registry(name)

    def _add_to_registry(self, time_period: TimePeriod):
        self.initialized_time_periods.register_time(time_period)

    def _calculate_years(self) -> List[int]:
        year_lst: List[int] = []
        for year in range(self.oldest_year, self.newest_year + 1):
            year_lst.append(year)
        return year_lst

    def _remove_invalid_terms(self, lst: List[TimePeriod]) -> List[TimePeriod]:
        oldest: TimePeriod = TimePeriod(self.oldest_term, self.oldest_year)
        if oldest in lst:
            oldest_time_index = lst.index(oldest)
        else:
            oldest_time_index = 0
        newest: TimePeriod = TimePeriod(self.newest_term, self.newest_year)
        if newest in lst:
            newest_time_index = lst.index(newest)
        else:
            newest_time_index = len(lst) - 1
        return lst[oldest_time_index : newest_time_index + 1]

class TimeManager:

    def __init__(self, domain_config: Type[DomainSpecificTimeConfig]) -> None:
        self.domain_config: Type[DomainSpecificTimeConfig] = domain_config
        self.generator: TimePeriodGenerator = TimePeriodGenerator(self.domain_config)
        self.time_units_checker: Type[TimeUnitChecker] = self.domain_config.get_time_unit_checker()

    def read_time_from_keyname(self, keyname: str) -> TimePeriod:
        return self.generator.fetch_time_from_registry(keyname)

    def generate_all_time_periods(self) -> List[TimePeriod]:
        return self.generator.create_all()

    def generate_years(self) -> List[TimePeriod]:
        return self.generator.create_years()

    def generate_specific_year(self, year: int) -> List[TimePeriod]:
        return self.generator.create_single_year(year)

    def generate_empty_time_period(self) -> TimePeriod:
        return self.generator.create_empty()

    def data_class_is_term_based(self, class_id: str) -> bool:
        return self.time_units_checker.is_term_based(class_id)

    def data_class_is_time_based(self, class_id: str) -> bool:
        return self.time_units_checker.is_time_based(class_id)

    def number_of_terms(self) -> int:
        return len(self.domain_config.ordered_terms())

class StrategyCollection(ABC):

    @staticmethod
    @abstractmethod
    def get_evaluation(time: str, name: str) -> Dict[str,str]:
        pass
    @staticmethod
    @abstractmethod
    def get_grade_sheet(time: str, name: str) -> Dict[str,str]:
        pass
    @staticmethod
    @abstractmethod
    def get_info_page(time: str, name: str) -> Dict[str,str]:
        pass

    @staticmethod
    @abstractmethod
    def from_school_get_years(time: str, name: str) -> List[str]:
        pass
    @staticmethod
    @abstractmethod
    def from_year_get_study_lines(time: str, name: str) -> List[str]:
        pass
    @staticmethod
    @abstractmethod
    def from_year_get_teachers(time: str, name: str) -> List[str]:
        pass
    @staticmethod
    @abstractmethod
    def from_year_get_courses(time: str, name: str) -> List[str]:
        pass
    @staticmethod
    @abstractmethod
    def from_course_get_terms(time: str, name: str) -> List[str]:
        pass

class DtuStrategyCollection(StrategyCollection):

    @staticmethod
    def get_evaluation(time: str, name: str) -> Dict[str,str]:
        return {}
    @staticmethod
    def get_grade_sheet(time: str, name: str) -> Dict[str,str]:
        return {}
    @staticmethod
    def get_info_page(time: str, name: str) -> Dict[str,str]:
        return {}

    @staticmethod
    def from_school_get_years(time: str, name: str) -> List[str]:
        return []
    @staticmethod
    def from_year_get_study_lines(time: str, name: str) -> List[str]:
        return []
    @staticmethod
    def from_year_get_teachers(time: str, name: str) -> List[str]:
        return []
    @staticmethod
    def from_year_get_courses(time: str, name: str) -> List[str]:
        return []
    @staticmethod
    def from_course_get_terms(time: str, name: str) -> List[str]:
        return []

class StrategySwitch:

    @staticmethod
    def get_data_dict(data_point: 'DataPoint') -> Dict[str,str]:
        domain: Domain = data_point.domain
        time: str = data_point.time_period.get_name()
        name: str = data_point.get_name()
        if isinstance(data_point, Evaluation):
            return domain.strategy_collection.get_evaluation(time, name)
        elif isinstance(data_point, GradeSheet):
            return domain.strategy_collection.get_grade_sheet(time, name)
        elif isinstance(data_point, InfoPage):
            return domain.strategy_collection.get_info_page(time, name)
        else:
            raise ValueError(f"Strategy switch error at {data_point.get_class_id()}")

    @staticmethod
    def get_child_list(container: 'Container', child_id: str) -> List[str]:
        domain: Domain = container.domain
        time: str = container.time_period.get_name()
        name: str = container.get_name()
        if isinstance(container, School) and child_id == Year.get_class_id():
            return domain.strategy_collection.from_school_get_years(time, name)
        elif isinstance(container, Year) and child_id == StudyLine.get_class_id():
            return domain.strategy_collection.from_year_get_study_lines(time, name)
        elif isinstance(container, Year) and child_id == Teacher.get_class_id():
            return domain.strategy_collection.from_year_get_teachers(time, name)
        elif isinstance(container, Year) and child_id == Course.get_class_id():
            return domain.strategy_collection.from_year_get_courses(time, name)
        elif isinstance(container, Course) and child_id == Term.get_class_id():
            return domain.strategy_collection.from_course_get_terms(time, name)
        else:
            raise ValueError(f"Strategy switch error at {container.get_class_id()}+{child_id}")

class DataFetcher:

    def __init__(self) -> None:
        self._strategy_switch: Type[StrategySwitch] = StrategySwitch
        self._data_objects: Registry = Registry[DataObject]()
        self._data_dicts: FileAccess = FileAccess[Dict[str,str]]()
        self._child_lists: FileAccess = FileAccess[List[str]]()

    def get_data_object(self, data_obj: 'DataObject') -> 'DataObject':
        key: str = data_obj.serialize()
        if self._data_objects.exists(key):
            return self._data_objects.read(key)
        else:
            return data_obj

    def get_data_dict(self, data_point: 'DataPoint') -> Dict[str,str]:
        key: str = data_point.serialize()
        if self._data_dicts.exists(key):
            return self._data_dicts.read(key)
        else:
            data_dct: Dict[str,str] = self._strategy_switch.get_data_dict(data_point)
            self._data_dicts.write_unique_key(key, data_dct)
            return data_dct

    def get_child_list(self, container: 'Container', child_id: str) -> List[str]:
        key: str = container.serialize() + DataObject.KEY_SEPARATOR + child_id
        if self._child_lists.exists(key):
            return self._child_lists.read(key)
        else:
            child_list: List[str] = self._strategy_switch.get_child_list(container, child_id)
            self._child_lists.write_unique_key(key, child_list)
            return child_list

class DomainConfig(ABC):
    @staticmethod
    def get_data_fetcher() -> DataFetcher:
        return DataFetcher()

    @staticmethod
    @abstractmethod
    def get_domain_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_time_manager() -> TimeManager:
        pass

    @staticmethod
    @abstractmethod
    def get_strategy_collection() -> StrategyCollection:
        pass

class DtuDomainConfig(DomainConfig):

    DOMAIN_NAME: str = "dtu"
    TIME_MANAGER: TimeManager = TimeManager(DtuTimeConfig)
    STRATEGY_COLLECTION: DtuStrategyCollection

    @staticmethod
    def get_domain_name() -> str:
        return DtuDomainConfig.DOMAIN_NAME

    @staticmethod
    def get_time_manager() -> TimeManager:
        return DtuDomainConfig.TIME_MANAGER

    @staticmethod
    def get_strategy_collection() -> StrategyCollection:
        return DtuDomainConfig.STRATEGY_COLLECTION

class Domain:

    def __init__(self, domain_config: Type[DomainConfig]) -> None:
        self.name: str = domain_config.get_domain_name()
        self.data_fetcher: DataFetcher = domain_config.get_data_fetcher()
        self.time_manager: TimeManager = domain_config.get_time_manager()
        self.strategy_collection: StrategyCollection = domain_config.get_strategy_collection()

    def get_name(self) -> str:
        return self.name

    def get_data_object(self, data_class: Type['DataObject'], name: str) -> 'DataObject':
        time_period = self.time_manager.generate_empty_time_period()
        fabricated_obj: DataObject = data_class(self, time_period, name)
        return self.data_fetcher.get_data_object(fabricated_obj)

    def get_child_list(self, container: 'Container', child_id: str) -> List[str]:
        return self.data_fetcher.get_child_list(container, child_id)

    def get_data_dictionary(self, data_point: 'DataPoint') -> Dict[str,str]:
        return self.data_fetcher.get_data_dict(data_point)


class DataObject(ABC):

    KEY_SEPARATOR: str = "__"

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        self.domain: Domain = domain
        self.time_period: TimePeriod = time_period
        self.name: str = name

    def get_name(self) -> str:
        return self.name

    def serialize(self) -> str:
        domain_name: str = self.domain.get_name()
        time_name: str = self.time_period.get_name()
        class_id: str = self.get_class_id()
        name: str = self.get_name()
        sep: str = DataObject.KEY_SEPARATOR
        return domain_name + sep + time_name + sep + class_id + sep + name

    @staticmethod
    @abstractmethod
    def get_class_id() -> str:
        pass

    @abstractmethod
    def cascade_build(self) -> None:
        pass

class Container(DataObject):

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.children: Dict[str,List[DataObject]] = {}
        self.data_operations: DataOperations = DataOperations(self)

    def cascade_build(self) -> None:
        child_classes: List[Type[DataObject]] = self._get_all_child_classes()
        for child_class in child_classes:
            child_id: str = child_class.get_class_id()
            child_names: List[str] = self.domain.get_child_list(self, child_id)
            for name in child_names:
                child: DataObject = self.domain.get_data_object(child_class, name)
                self._add_child(child)
                child.cascade_build()

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

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.data: Dict[str,str] = {}

    def cascade_build(self) -> None:
        self.data = self.domain.get_data_dictionary(self)

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

    def __init__(self, domain: Domain, time_period: TimePeriod, name: str) -> None:
        super().__init__(domain, time_period, name)
        self.num: float = 1.0

    def get_float(self) -> float:
        return self.num

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

S = TypeVar('S', bound=DataPoint)
class ActionCascader(Generic[S]):

    def __init__(self, class_type: Type[DataPoint], action: Callable[[S], float]) -> None:
        self.key = class_type.get_class_id()
        self.action: Callable[[S], float] = action

    def cascade_perform_action(self, container: Container) -> float:
        if self.key in container.children:
            return self._perform_action(container)
        elif len(container.get_primary_children()) > 0:
            return self._continue_action_cascade(container)
        else:
            raise ValueError(f"Key {self.key} not found in {container.serialize()}")

    def _perform_action(self, container: Container) -> float:
        child_list: List[DataObject] = container.get_children(self.key)
        if len(child_list) != 1:
            raise ValueError(f"There should be exactly 1 child in {container.serialize()}")
        return self.action(cast(S,child_list[0]))

    def _continue_action_cascade(self, container: Container) -> float:
        child_sum: float = 0.0
        for child in container.get_primary_children():
            child_sum += self.cascade_perform_action(cast(Container, child))
        return child_sum / len(container.get_primary_children())

class DataOperations:

    _ACTION_CASCADER: Type[ActionCascader] = ActionCascader

    def __init__(self, container: Container) -> None:
        self.container: Container = container

    def do_thing_a(self) -> float:
        action: Callable[[Evaluation], float] = Evaluation.get_float
        action_cascader: ActionCascader = ActionCascader[Evaluation](Evaluation, action)
        return action_cascader.cascade_perform_action(self.container)

class Main:
    def __init__(self) -> None:
        self._domains: Registry = DomainAccess[Domain]()

    def get_domain(self, key: str) -> Domain:
        return self._domains.read(key)

    def get_all_domains(self) -> List[Domain]:
        return self._domains.read_all()

    def do_stuff(self) -> None:
        for domain in self.get_all_domains():
            terms: List[TimePeriod] = domain.time_manager.generate_all_time_periods()
            years: List[TimePeriod] = domain.time_manager.generate_years()
            empty_time: TimePeriod = domain.time_manager.generate_empty_time_period()
            print(terms)
            print(years)
            print(empty_time)

#School
#Year
#Course
#Term
#Teacher
#StudyLine
#Evaluation
#GradeSheet
#InfoPage

if __name__ == "__main__":
    Main().do_stuff()