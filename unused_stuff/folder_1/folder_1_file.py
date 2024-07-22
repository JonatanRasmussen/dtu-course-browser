def folder_1_hello_world():
    print("hello world from folder 1")

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from top_level import top_level_hello_world
    else:
        from ..top_level import top_level_hello_world
    top_level_hello_world()