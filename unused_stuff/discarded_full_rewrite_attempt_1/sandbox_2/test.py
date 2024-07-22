
from abc import ABC

class MyBaseClass(ABC):
    def __init__(self):
        self.name = "Base"
        self.my_var_1 = "A"
        self.my_var_2 = "B"

class MySubBaseClass(MyBaseClass):
    def __init__(self):
        super().__init__()
        self.name = "SubBase"
        self.this_instance = self.name
        self.my_var_3 = "C"
        self.my_var_4 = "D"

    @classmethod
    def get_instance(self):
        # Return the current class instance
        return self

class MyConcreteClass(MySubBaseClass):
    def __init__(self):
        super().__init__()
        self.name = "Concrete"
        self.my_var_5 = "E"
        self.my_var_6 = "F"

test = MyConcreteClass()
print(test.my_var_1)
print(test.my_var_2)
print(test.my_var_3)
print(test.my_var_4)
print(test.my_var_5)
print(test.my_var_6)
print(test.my_var_6)
print(test.name)
print(test.this_instance)