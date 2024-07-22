import pandas as pd

def class_test():
    class foo:
        """test"""
        test = 12345
        def __init__(self, real_part, imag_part):
            self.r = real_part
            self.i = imag_part
        def bar(self):
            return 'hello'

    my_first_object = foo(2,3)
    my_second_object = foo(1,4)
    print(my_first_object.test)
    print(my_first_object.r)
    print(my_second_object.i)

#class_test()

def func_name(f):
    def wrap(*args, **kwargs):
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def abc():
    print('hello_world')

def numeric_test():
    testy = int(round(float('9.7'), -1))
    print(testy)

#numeric_test()

my_columns = {"alpha": ["10"], "beta": ["20"], "celta": ["30"]}
my_new_columns = {"alpha": ["70"], "beta": ["80"], "celta": ["90"]}

df = pd.DataFrame(data = my_columns)
new_df = pd.DataFrame(data = my_new_columns)

df = pd.concat((df, new_df), ignore_index = True)
print(df)



#26225
#31783
#42042

#5.5☠️
#5.0💀
#4.5🥵
#4.0😰
#3.5😓
#3.0😅
#2.5😇
#2.0🥱
#1.5😴
#1.0🤡


#🏷️
#🎓
#🕗

#💯
#✅
#📚

#💡
#🔥
#👩🏻‍🏫

#🏅
#🏷️
#✍️
#📜
#📝