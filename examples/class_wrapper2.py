# DEPRECATED
# More complete attempt at wrapping Objective-C objects in python.

from cocoapy.runtime import *

class ObjCMethod(object):
    """This represents an unbound Objective-C method (really an IMP)."""

    typecodes = {'c':c_char, 'i':c_int, 's':c_short, 'l':c_long, 'q':c_longlong,
                 'C':c_ubyte, 'I':c_uint, 'S':c_ushort, 'L':c_ulong, 'Q':c_ulonglong,
                 'f':c_float, 'd':c_double, 'B':c_bool, 'v':None, 'Vv':None, '*':c_char_p,
                 '@':c_void_p, '#':c_void_p, ':':c_void_p, '^v':c_void_p,
                 NSPointEncoding:NSPoint, NSSizeEncoding:NSSize, NSRectEncoding:NSRect}

    cfunctype_table = {}

    def __init__(self, method):
        """Initialize with an Objective-C Method pointer.  We then determine
        the return type and argument type information of the method."""
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
        # Get types for all the arguments.
        try:
            self.argtypes = [self.ctype_for_encoding(t) for t in self.argument_types]
        except:
            #print 'no argtypes encoding for %s (%s)' % (self.name, self.argument_types)
            self.argtypes = None
        # Get types for the return type.
        try:
            if self.return_type == '@':
                self.restype = ObjCInstance
            elif self.return_type == '#':
                self.restype = ObjCClass
            else:
                self.restype = self.ctype_for_encoding(self.return_type)
        except:
            #print 'no restype encoding for %s (%s)' % (self.name, self.return_type)
            self.restype = None
        self.func = None

    def ctype_for_encoding(self, encoding):
        """Return ctypes type for an encoded Objective-C type."""
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
        """Returns a ctypes CFUNCTYPE for the method."""
        self.prototype = CFUNCTYPE(self.restype, *self.argtypes)
        return self.prototype

    def __repr__(self):
        return "<ObjCMethod: %s %s>" % (self.name, self.encoding)

    def get_callable(self):
        """Returns a python-callable version of the method's IMP."""
        if not self.func:
            prototype = self.get_prototype()
            self.func = prototype(self.imp)
            self.func.restype = self.restype
            self.func.argtypes = self.argtypes
        return self.func

    def __call__(self, objc_id, *args):
        """Call the method with the given id and arguments.  You do not need
        to pass in the selector as an argument since it will be automatically
        provided."""
        f = self.get_callable()
        return f(objc_id, self.selector, *args)


class ObjCBoundMethod(object):
    """This represents an Objective-C method (an IMP) which has been bound
    to some id which will be passed as the first parameter to the method."""

    def __init__(self, method, objc_id):
        """Initialize with a method and Objective-C id (class or object)."""
        self.method = method
        self.objc_id = objc_id

    def __repr__(self):
        return '<ObjCBoundMethod %s (%s)>' % (self.method.name, self.objc_id)

    def __call__(self, *args):
        """Call the method with the given arguments."""
        return self.method(self.objc_id, *args)


class ObjCClassRegistry(object):
    """Keeps track of all Objective-C classes that we've pythonized."""

    registered_classes = {}

    def register(self, class_name_or_ptr):
        """This method is used to retrieve a class object.  You may
        pass it either a name or a pointer value."""

        if isinstance(class_name_or_ptr, basestring):
            name = class_name_or_ptr
            ptr = c_void_p(objc.objc_getClass(name))
        else:
            ptr = class_name_or_ptr
            name = objc.class_getName(ptr)

        if name in self.registered_classes:
            objc_class = self.registered_classes[name]
        else:
            objc_class = ObjCClass(ptr)
            self.registered_classes[name] = objc_class
        return objc_class

objc_class_registry = ObjCClassRegistry()

class ObjCClass(object):
    """Python wrapper for an Objective-C class."""

    def __init__(self, class_ptr):
        """Initialize with an Objective-C Class pointer."""
        if not isinstance(class_ptr, c_void_p):
            class_ptr = c_void_p(class_ptr)
        self.ptr = class_ptr
        self.name = objc.class_getName(self.ptr)
        self.instance_methods = {}
        self.class_methods = {}
        self.cache_instance_methods()
        self.cache_class_methods()
        self._as_parameter_ = self.ptr

    def __repr__(self):
        return "<ObjCClass: %s at %d>" % (self.name, self.ptr.value)

    def cache_instance_methods(self):
        """Create and store python representations of all instance methods
        implemented by this class (but does not find methods of superclass)."""
        count = c_uint()
        method_array = objc.class_copyMethodList(self.ptr, byref(count))
        for i in range(count.value):
            method = c_void_p(method_array[i])
            objc_method = ObjCMethod(method)
            self.instance_methods[objc_method.pyname] = objc_method

    def cache_class_methods(self):
        """Create and store python representations of all class methods
        implemented by this class (but does not find methods of superclass)."""
        count = c_uint()
        method_array = objc.class_copyMethodList(objc.object_getClass(self.ptr), byref(count))
        for i in range(count.value):
            method = c_void_p(method_array[i])
            objc_method = ObjCMethod(method)
            self.class_methods[objc_method.pyname] = objc_method

    def get_instance_method(self, name):
        """Returns a python representation of the named instance method,
        either by looking it up in the cached list of methods or by searching
        for and creating a new method object."""
        if name in self.instance_methods:
            return self.instance_methods[name]
        else:
            # If method name isn't in the cached list, it might be a method of
            # the superclass, so call class_getInstanceMethod to check.
            method = c_void_p(objc.class_getInstanceMethod(self.ptr, get_selector(name)))
            if method.value:
                objc_method = ObjCMethod(method)
                self.instance_methods[name] = objc_method
                return objc_method
        return None

    def get_class_method(self, name):
        """Returns a python representation of the named class method,
        either by looking it up in the cached list of methods or by searching
        for and creating a new method object."""
        if name in self.class_methods:
            return self.class_methods[name]
        else:
            # If method name isn't in the cached list, it might be a method of
            # the superclass, so call class_getInstanceMethod to check.
            method = c_void_p(objc.class_getClassMethod(self.ptr, get_selector(name)))
            if method.value:
                objc_method = ObjCMethod(method)
                self.class_methods[name] = objc_method
                return objc_method
        return None

    def __getattr__(self, name):
        """Returns a callable method object with the given name."""
        # If name refers to a class method, then return a callable object
        # for the class method with self.ptr as hidden first parameter.
        method = self.get_class_method(name)
        if method:
            return ObjCBoundMethod(method, self.ptr)
        # If name refers to an instance method, then simply return the method.
        # The caller will need to supply an instance as the first parameter.
        method = self.get_instance_method(name)
        if method:
            return method
        # Otherwise, raise an exception.
        raise AttributeError('ObjCClass %s has no attribute %s' % (self.name, name))


class ObjCInstance(object):
    """Python wrapper for an Objective-C instance."""

    def __init__(self, object_ptr):
        """Initialize with an Objective-C id pointer."""
        if not isinstance(object_ptr, c_void_p):
            object_ptr = c_void_p(object_ptr)
        self.ptr = object_ptr
        class_ptr = c_void_p(objc.object_getClass(self.ptr))
        # Make sure that this class has been registered.
        self.objc_class = objc_class_registry.register(class_ptr)
        self.name = self.objc_class.name

    def __repr__(self):
        return "<ObjCInstance: %s at %d>" % (self.name, self.ptr.value)

    def __getattr__(self, name):
        """Returns a callable method object with the given name."""
        # Search for named instance method in the class object and if it
        # exists, return callable object with self.ptr as hidden argument.
        method = self.objc_class.get_instance_method(name)
        if method:
            return ObjCBoundMethod(method, self.ptr)
        # Else, search for class method with given name in the class object.
        # If it exists, return callable object with a pointer to the class
        # as a hidden argument.
        method = self.objc_class.get_class_method(name)
        if method:
            return ObjCBoundMethod(method, self.objc_class.ptr)
        # Otherwise raise an exception.
        raise AttributeError('ObjCInstance %s has no attribute %s' % (self.name, name))



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: python class_wrapper2.py <Obj-C Class>'
        exit(1)

    class_name = sys.argv[1]
    NSObject = objc_class_registry.register(class_name)
    print NSObject
    print objc.object_getClassName(NSObject.ptr)

    x = NSObject.alloc()
    print objc.object_getClassName(x.ptr)
    print 'x', x
    print 'x.init', x.init
    print 'x.init()', x.init()
    print x.retainCount()
    print x.retain()
    print x.retainCount()
    print x.retainCount()
    print x.retain()
    print x.retainCount()
    print x.retain()
    print x.retainCount()
    y = NSObject.alloc()
    print 'y', y
    print 'y.init()', y.init()
    print y.retainCount()
    print y.retain()
    print y.retainCount()
    #print x.blah()
