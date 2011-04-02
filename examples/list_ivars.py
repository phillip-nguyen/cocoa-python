# List all the instance variables of an Objective-C class.

from cocoapy.runtime import *

def list_ivars(cls):
    count = c_uint()
    ivar_array = objc.class_copyIvarList(cls, byref(count))
    print count.value, 'ivars'
    print '------------------'
    names = []
    for i in range(count.value):
        ivar = c_void_p(ivar_array[i])
        name = objc.ivar_getName(ivar)
        encoding = objc.ivar_getTypeEncoding(ivar)
        names.append((name, encoding))

    names.sort()
    for x, y in names: 
        print x, y

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: python list_ivars.py <Obj-C Class>'
        exit(1)
    
    class_name = sys.argv[1]
    cls = get_class(class_name)

    print class_name, 'instance variables:'
    list_ivars(cls)
        

