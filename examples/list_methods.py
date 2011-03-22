# List all the methods of an Objective-C class.

from objc_runtime import *

def list_methods(cls):
    count = c_uint()
    method_array = objc.class_copyMethodList(cls, byref(count))
    print count.value, 'methods'
    print '------------------'
    names = []
    for i in range(count.value):
        method = c_void_p(method_array[i])
        sel = c_void_p(objc.method_getName(method))
        name = objc.sel_getName(sel)
        encoding = objc.method_getTypeEncoding(method)
        return_type = objc.method_copyReturnType(method)
        names.append((name, encoding, return_type))

    names.sort()
    for x, y, z in names: 
        print x, y

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: python list_methods.py <Obj-C Class>'
        exit(1)
    
    class_name = sys.argv[1]
    cls = get_class(class_name)

    print class_name, 'instance methods:'
    list_methods(cls)
        
    print
    print class_name, 'class methods:'
    list_methods(get_object_class(cls))
