from abc import ABC, abstractmethod

class DataSource(ABC):

    @abstractmethod
    def obtain_data(self):
        pass
