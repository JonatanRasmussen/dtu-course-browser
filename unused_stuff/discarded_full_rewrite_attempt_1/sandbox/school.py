from abc import ABC, abstractmethod

class School(ABC):

    @abstractmethod
    def instantiate_grades(self: 'School') -> dict[str:'Grade']:
        pass