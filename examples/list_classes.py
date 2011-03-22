# List the names of all loaded Objective-C classes.

from objc_runtime import *


count = objc.objc_getClassList(None, 0)
print '%d classes found:' % count 

classes = (c_void_p * count)()
count = objc.objc_getClassList(classes, count)

class_names = []
for cls in classes:
    class_names.append(objc.class_getName(cls))
    
class_names.sort()

for name in  class_names:
    print name
