from ctypes import *
class strprint(object):
    def __init__ (self,num,StrPrint):
        windll.Kernel32.GetStdHandle.restype = c_ulong
        h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
        windll.Kernel32.SetConsoleTextAttribute(h, num)
        print StrPrint
        windll.Kernel32.SetConsoleTextAttribute(h, 15)
        
