import os
class Singleton(type):
    instance = None
    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance

class Reg(metaclass=Singleton):
    
    def __init__(self):
        print("dupa")
#    self.__home=os.environ.get('KOSTKA_HOME')
#        if (self.__home is None): exit(1)
#
#        if(os.path.isdir(value)):
#            self.__hampath=value
