# Simple example of subclassing NSObject and
# creating objective-c callable methods using decorators.

from cocoapy import *

class MySubclass_Implementation(object):
    MySubclass = ObjCSubclass('NSObject', 'MySubclass')

    # Through some magic, the self variable received by these methods is
    # an instance of the python ObjCInstance object.  It has an attribute
    # objc_cmd set to the hidden _cmd argument.
    @MySubclass.method('@')
    def init(self):
        self = ObjCInstance(send_super(self, 'init'))
        #self = ObjCInstance(send_message('NSObject', 'alloc'))
        print 'inside init: self =', self
        self.x = 1
        return self

    # A normal objective-c instance method.  This gets added to the
    # objective-c class.  The type-encoding string says that this method
    # returns void.
    @MySubclass.method('v')
    def doSomething(self):
        print 'doSomething', self
        print 'x =', self.x
        self.x += 1

    @MySubclass.method('v@')
    def doSomethingElse(self, other):
        print 'doSomethingElse', self, other
        other.doSomething()

    @MySubclass.method('v'+PyObjectEncoding)
    def takePyObject(self, pyobject):
        print 'takePyObject', self, pyobject
        print 'x =', self.x

    @MySubclass.method('v')
    def dealloc(self):
        print 'dealloc', self
        send_super(self, 'dealloc')

######################################################################

if __name__ == '__main__':

    MySubclass = ObjCClass('MySubclass')

    myobject1 = MySubclass.alloc().init()
    print 'after init: myobject1 =', myobject1
    
    myobject1.doSomething()

    print
    
    myobject2 = MySubclass.alloc().init()
    print 'after init: myobject2 =', myobject2
    myobject2.doSomething()
    #myobject2.doSomething()
    #myobject2.doSomethingElse()

    print 

    myobject1.doSomethingElse(myobject2)
    class Foo:
        pass
    f = Foo()
    myobject1.takePyObject(f)
    myobject1.release()
    myobject2.release()
