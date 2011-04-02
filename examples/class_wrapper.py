# DEPRECATED
# First attempt at wrapping up Objective-C objects using python classes.

from cocoapy.runtime import *

class ObjCMethod(object):

    typecodes = {'c':c_char, 'i':c_int, 's':c_short, 'l':c_long, 'q':c_longlong, 
                 'C':c_ubyte, 'I':c_uint, 'S':c_ushort, 'L':c_ulong, 'Q':c_ulonglong, 
                 'f':c_float, 'd':c_double, 'B':c_bool, 'v':None, 'Vv':None, '*':c_char_p,
                 '@':c_void_p, '#':c_void_p, ':':c_void_p, '^v':c_void_p, 
                 NSPointEncoding:NSPoint, NSSizeEncoding:NSSize, NSRectEncoding:NSRect}

    cfunctype_table = {}
    
    def __init__(self, method):
        self.selector = c_void_p(objc.method_getName(method))
        self.name = objc.sel_getName(self.selector)
        self.pyname = self.name.replace(':', '_')
        self.encoding = objc.method_getTypeEncoding(method)
        self.return_type = objc.method_copyReturnType(method)
        self.nargs = objc.method_getNumberOfArguments(method)
        self.imp = objc.method_getImplementation(method)
        self.argument_types = []
        for i in range(self.nargs):
            buffer = c_buffer(512)
            objc.method_getArgumentType(method, i, buffer, len(buffer))
            self.argument_types.append(buffer.value)

        try:
            self.argtypes = [self.ctype_for_encoding(t) for t in self.argument_types]
        except:
            print 'no argtypes encoding for %s (%s)' % (self.name, self.argument_types)
            self.argtypes = None
        try:
            self.restype = self.ctype_for_encoding(self.return_type)
        except:
            print 'no restype encoding for %s (%s)' % (self.name, self.return_type)
            self.restype = None
        self.func = None

    def ctype_for_encoding(self, encoding):
        if encoding in self.typecodes:
            return self.typecodes[encoding]
        elif encoding[0] == '^' and encoding[1:] in self.typecodes:
            return POINTER(self.typecodes[encoding[1:]])
        elif encoding[0] == 'r' and encoding[1:] in self.typecodes:
            # const decorator, don't care
            return self.typecodes[encoding[1:]]
        else:
            raise Exception('unknown encoding for %s: %s' % (self.name, encoding))
        
    def get_prototype(self):
        self.prototype = CFUNCTYPE(self.restype, *self.argtypes)
        return self.prototype
    
    def __repr__(self):
        return "<ObjCMethod: %s %s>" % (self.name, self.encoding)

    def get_callable(self):
        if not self.func:
            prototype = self.get_prototype()
            self.func = prototype(self.imp)
            self.func.restype = self.restype
            self.func.argtypes = self.argtypes
        return self.func
   
    def __call__(self, objc_id, *args):
        f = self.get_callable()
        return f(objc_id, self.selector, *args)
 
class ObjCClass(object):
    def __init__(self, class_name):
        self.name = class_name
        self.cls = get_class(class_name)
        self.get_instance_methods()
        self._as_parameter_ = self.cls

    def __repr__(self):
        return "<ObjCClass: %s at %d>" % (self.name, self.cls.value)
        
    def get_instance_methods(self):
        count = c_uint()
        method_array = objc.class_copyMethodList(self.cls, byref(count))
        self.instance_methods = {}
        for i in range(count.value):
            method = c_void_p(method_array[i])
            objc_method = ObjCMethod(method)
            self.instance_methods[objc_method.pyname] = objc_method
        
    def list_methods(self):
        for method in self.instance_methods:
            print method

    def __getattr__(self, name):
        if name in self.instance_methods:
            return self.instance_methods[name]


    def alloc(self):
        instance = send_message(self.cls, 'alloc')
        if instance:
            return ObjCInstance(self, instance)
        else:
            return None

class ObjCInstance(object):
    def __init__(self, objc_class, instance):
        self.objc_class = objc_class
        self.instance = instance
        self.name = objc_class.name

    def __repr__(self):
        return "<ObjCInstance: %s at %d>" % (self.name, self.instance.value)

    def __getattr__(self, name):
        if name in self.objc_class.instance_methods:
            def callable(*args):
                method = self.objc_class.instance_methods[name]
                return method(self.instance, *args)
            return callable
        raise AttributeError('%s has no attribute %s' % (self.name, name))
        
    
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: python class_wrapper.py <Obj-C Class>'
        exit(1)
    
    class_name = sys.argv[1]
    NSObject = ObjCClass(class_name)
    print NSObject
    
    x = NSObject.alloc()
    print x
    print x.retainCount()
    print x.retain()
    print x.retainCount()
    print x.retainCount()
    print x.retain()    
    print x.retainCount()
    print x.retain()    
    print x.retainCount()
    print x.blah()



