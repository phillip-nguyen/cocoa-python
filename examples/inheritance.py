# Print out the inheritance chain for a given class.

from cocoapy.runtime import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: python inheritance.py <Obj-C Class>'
        exit(1)
    
    class_name = sys.argv[1]
    cls = get_class(class_name)
    
    while cls:
        name = objc.class_getName(cls)
        print name
        cls = c_void_p(objc.class_getSuperclass(cls))

