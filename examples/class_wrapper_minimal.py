# An extremely minimal (too minimal?) python wrapper 
# around the Objective-C id type.

from objc_runtime import *

class ObjCId(object):
    def __init__(self, objc_id):
        self.ptr = objc_id
        
    def __repr__(self):
        return '<ObjId: %d at %#x>' % (self.ptr, id(self))

    def __getattr__(self, name):
        selName = name.replace('_', ':')
        def callable(*args, **kwargs):
            return send_message(self.ptr, selName, *args, **kwargs)
        return callable

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: python class_wrapper_minimal.py <Obj-C Class>'
        exit(1)


class_name = sys.argv[1]
obj = ObjCId(get_class(class_name))
x = obj.alloc(restype=ObjCId).init(restype=ObjCId)
print x
print x.retainCount(restype=c_int)
print x.retain(restype=ObjCId)
print x.retainCount(restype=c_int)
