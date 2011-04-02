# Even more complete attempt at wrapping Objective-C objects in python.
# ObjCClass and ObjCInstance use cached objects with __new__
# Implementation of ObjCSubclass can be made slightly simpler.

import weakref
from cocoapy.runtime import *

class ObjCMethod(object):
    """This represents an unbound Objective-C method (really an IMP)."""

    # Note, need to map 'c' to c_byte rather than c_char, because otherwise
    # ctypes converts the value into a one-character string which is generally
    # not what we want at all, especially when the 'c' represents a bool var.
    typecodes = {'c':c_byte, 'i':c_int, 's':c_short, 'l':c_long, 'q':c_longlong, 
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
        try:
            return f(objc_id, self.selector, *args)
        except ArgumentError as error:
            # Add more useful info to argument error exceptions, then reraise.
            error.args += ('selector: ' + self.name,
                           'argtypes: ' + str(self.argtypes),
                           'encoding: ' + self.encoding)
            raise



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

 
class ObjCClass(object):
    """Python wrapper for an Objective-C class."""

    # We only create one Python object for each Objective-C class.
    # Any future calls with the same class will return the previously
    # created Python object.  Note that these aren't weak references.
    # After you create an ObjCClass, it will exist until the end of the
    # program.
    _registered_classes = {}

    def __new__(cls, class_name_or_ptr):
        """Create a new ObjCClass instance or return a previously created
        instance for the given Objective-C class.  The argument may be either
        the name of the class to retrieve, or a pointer to the class."""
        # Determine name and ptr values from passed in argument.
        if isinstance(class_name_or_ptr, basestring):
            name = class_name_or_ptr
            ptr = c_void_p(objc.objc_getClass(name))
        else:
            ptr = class_name_or_ptr
            # Make sure that ptr value is wrapped in c_void_p object
            # for safety when passing as ctypes argument.
            if not isinstance(ptr, c_void_p):
                ptr = c_void_p(ptr)
            name = objc.class_getName(ptr)
            
        # Check if we've already created a Python object for this class
        # and if so, return it rather than making a new one.
        if name in cls._registered_classes:
            return cls._registered_classes[name]

        # Otherwise create a new Python object and then initialize it.
        objc_class = super(ObjCClass, cls).__new__(cls)
        objc_class.ptr = ptr
        objc_class.name = name
        objc_class.instance_methods = {}   # mapping of name -> instance method
        objc_class.class_methods = {}      # mapping of name -> class method
        objc_class._as_parameter_ = ptr    # for ctypes argument passing

        # Store the new class in dictionary of registered classes.
        cls._registered_classes[name] = objc_class

        # Not sure this is necessary...
        objc_class.cache_instance_methods()
        objc_class.cache_class_methods()

        return objc_class

    def __repr__(self):
        return "<ObjCClass: %s at %s>" % (self.name, str(self.ptr.value))
        
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

    _cached_objects = weakref.WeakValueDictionary()

    def __new__(cls, object_ptr):
        """Create a new ObjCInstance or return a previously created one
        for the given object_ptr which should be an Objective-C id."""
        # Make sure that object_ptr is wrapped in a c_void_p.
        if not isinstance(object_ptr, c_void_p):
            object_ptr = c_void_p(object_ptr)
        
        # Check if we've already created an python ObjCInstance for this
        # object_ptr id and if so, then return it.
        if object_ptr.value in cls._cached_objects:
            return cls._cached_objects[object_ptr.value]

        # Otherwise, create a new ObjCInstance.
        objc_instance = super(ObjCInstance, cls).__new__(cls)
        objc_instance.ptr = object_ptr
        objc_instance._as_parameter = object_ptr
        # Determine class of this object.
        class_ptr = c_void_p(objc.object_getClass(object_ptr))
        objc_instance.objc_class = ObjCClass(class_ptr)

        # Store new object in the dictionary of cached objects, keyed
        # by the (integer) memory address pointed to by the object_ptr.
        cls._cached_objects[object_ptr.value] = objc_instance

        return objc_instance

    def __repr__(self):
        return "<ObjCInstance: %s at %s>" % (self.objc_class.name, str(self.ptr.value))

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
        raise AttributeError('ObjCInstance %s has no attribute %s' % (self.objc_class.name, name))
        


class ObjCSubclass2(object):
    """Use this to create a subclass of an existing Objective-C class.
    It consists primarily of function decorators which you use to add methods
    to the subclass."""
    def __init__(self, superclass, name):
        print 'ObjCSubclass2.init'
        self._imp_table = {}
        self.name = name
        self.objc_cls = create_subclass(superclass, name)
        self._as_parameter_ = self.objc_cls
        self.register()
        self.objc_metaclass = get_metaclass(name)

    def register(self):
        objc.objc_registerClassPair(self.objc_cls)

    def add_ivar(self, varname, vartype):
        return add_ivar(self.objc_cls, varname, vartype)

    def add_method(self, method, name, encoding):
        imp = add_method(self.objc_cls, name, method, encoding)
        self._imp_table[name] = imp

    # http://iphonedevelopment.blogspot.com/2008/08/dynamically-adding-class-objects.html
    def add_class_method(self, method, name, encoding):
        imp = add_method(self.objc_metaclass, name, method, encoding)
        self._imp_table[name] = imp
    
    def method(self, encoding):
        """Function decorator for instance methods."""
        # Add encodings for hidden self and cmd arguments.
        encoding = encoding[0] + '@:' + encoding[1:]
        def decorator(f):
            def objc_method(objc_self, objc_cmd, *args):
                py_self = ObjCInstance(objc_self)
                py_self.objc_self = objc_self
                py_self.objc_cmd = objc_cmd
                result = f(py_self, *args)
                return result
            name = f.func_name.replace('_', ':')
            self.add_method(objc_method, name, encoding)
            return objc_method
        return decorator
    
    def classmethod(self, encoding):
        """Function decorator for class methods."""
        # Add encodings for hidden self and cmd arguments.
        encoding = encoding[0] + '@:' + encoding[1:]
        def decorator(f):
            def objc_class_method(objc_cls, objc_cmd, *args):
                py_cls = ObjCClass(objc_cls)
                py_cls.objc_cmd = objc_cmd
                return f(py_cls, *args)
            name = f.func_name.replace('_', ':')
            self.add_class_method(objc_class_method, name, encoding)
            return objc_class_method
        return decorator

    # This is going to have to pass some information onto the the associated
    # python class so that it knows to add this function to a newly created
    # python instance...
    def pythonmethod(self, f):
        """Function decorator for python-callable methods."""
        #setattr(self.PythonSelf, f.func_name, f)
        #return f
        pass
        

class MySubclassImplementation(object):
    MySubclass = ObjCSubclass2('NSObject', 'MySubclass')
    
    @MySubclass.method('v')
    def doSomething(self):
        if not hasattr(self, 'x'):
            self.x = 0
        self.x += 1
        print 'doSomething', self.x
        self.doSomething2()

    @MySubclass.method('v')
    def doSomething2(self):
        print 'doSomething2', self.x

def run_window():
    NSAutoreleasePool = ObjCClass('NSAutoreleasePool')
    NSApplication = ObjCClass('NSApplication')
    NSWindow = ObjCClass('NSWindow')

    app = NSApplication.sharedApplication()
    
    pool = NSAutoreleasePool.alloc().init()

    window = NSWindow.alloc()
    frame = NSMakeRect(100,100,300,300)
    window.initWithContentRect_styleMask_backing_defer_(
        frame,
        NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask,
        NSBackingStoreBuffered,
        False)
    window.setTitle_(get_NSString("My Awesome Window"))
    window.makeKeyAndOrderFront_(None)

    app.run()


def stupid_stuff():
    NSObject = ObjCClass(class_name)
    print NSObject
    print objc.object_getClassName(NSObject.ptr)

    x = NSObject.alloc()
    print objc.object_getClassName(x.ptr)
    print 'x', x
    print 'x.init', x.init
    print 'x.init()', x.init()
    print 'x.objc_class', x.objc_class
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
    print 'y.objc_class', y.objc_class
    print y.retainCount()
    print y.retain()
    print y.retainCount()

        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: python class_wrapper3.py <Obj-C Class>'
        exit(1)
    
    class_name = sys.argv[1]

    MySubclass = ObjCClass('MySubclass')
    print MySubclass
    x = MySubclass.alloc().init()
    print x
    x.doSomething()
    x.doSomething()
    x.doSomething()

    print ObjCInstance._cached_objects.items()
    x.release()
    del x

    print ObjCInstance._cached_objects.items()
    
    #run_window()
