# DEPRECATED
# Simple example of subclassing NSObject and
# creating objective-c callable methods using decorators.

from objc_runtime import *

class MySubclass_Implementation(object):
    MySubclass = ObjCSubclass('NSObject', 'MySubclass')

    # The initmethod decorator creates the python "self" object associated
    # with an instance of this class.  This python self object is what
    # gets passed as self to each of the methods.  The initmethod
    # also stores the python self object in a dictionary keyed by the 
    # value of objc_self so that it will persist and so that we can
    # retrieve it for the callback functions.
    @MySubclass.initmethod('@')
    def init(self):
        print 'init', self.objc_self, self.objc_cmd
        self.objc_self = send_super(self, 'init')
        self.x = 1
        return self.objc_self

    # A normal objective-c instance method.  This gets added to the
    # objective-c class.  The type-encoding string says that this method
    # returns void.
    @MySubclass.method('v')
    def doSomething(self):
        print 'doSomething', self.objc_self
        print 'x =', self.x
        self.x += 1

    @MySubclass.method('v')
    def doSomethingElse(self):
        print 'doSomethingElse', self.objc_self
        #send_message(c_void_p(self.objc_self), 'doSomething')
        send_message(self, 'doSomething')
        self.my_python_method()

    # A python method for the python self object.  This is callable
    # from the objective-c method, however it is not registered
    # as an instance method of the objective-c class, and so you 
    # cannot use send_message() to call it.
    @MySubclass.pythonmethod
    def my_python_method(self):
        print 'my_python_method', self.objc_self
        print 'x =', self.x

    # The dealloc decorator takes care of deleting the python
    # self object associated with this objective-c instance.
    @MySubclass.dealloc
    def dealloc(self):
        print 'dealloc', self.objc_self
        send_super(self, 'dealloc')

######################################################################

if __name__ == '__main__':

    myobject1 = alloc_init('MySubclass')
    send_message(myobject1, 'doSomething')    

    print
    
    myobject2 = alloc_init('MySubclass')
    send_message(myobject2, 'doSomething')
    send_message(myobject2, 'doSomething')
    send_message(myobject2, 'doSomethingElse')

    print 

    send_message(myobject1, 'doSomethingElse')
    send_message(myobject1, 'release')
