# objective-ctypes
#
# Copyright (c) 2011, Phillip Nguyen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of objective-ctypes nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from ctypes import *
from ctypes import util

import sys, platform
__LP64__ = (sys.maxint > 2**32)
__i386__ = (platform.machine() == 'i386')

if sizeof(c_void_p) == 4:
    c_ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
    c_ptrdiff_t = c_int64

######################################################################

objc = cdll.LoadLibrary(util.find_library('objc'))

######################################################################

# BOOL class_addIvar(Class cls, const char *name, size_t size, uint8_t alignment, const char *types)
objc.class_addIvar.restype = c_bool
objc.class_addIvar.argtypes = [c_void_p, c_char_p, c_size_t, c_uint8, c_char_p]

# BOOL class_addMethod(Class cls, SEL name, IMP imp, const char *types)
objc.class_addMethod.restype = c_bool

# BOOL class_addProtocol(Class cls, Protocol *protocol)
objc.class_addProtocol.restype = c_bool
objc.class_addProtocol.argtypes = [c_void_p, c_void_p]

# BOOL class_conformsToProtocol(Class cls, Protocol *protocol)
objc.class_conformsToProtocol.restype = c_bool
objc.class_conformsToProtocol.argtypes = [c_void_p, c_void_p]

# Ivar * class_copyIvarList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Ivar describing instance variables.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyIvarList.restype = POINTER(c_void_p)
objc.class_copyIvarList.argtypes = [c_void_p, POINTER(c_uint)]

# Method * class_copyMethodList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Method describing instance methods.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyMethodList.restype = POINTER(c_void_p)
objc.class_copyMethodList.argtypes = [c_void_p, POINTER(c_uint)]

# objc_property_t * class_copyPropertyList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type objc_property_t describing properties.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyPropertyList.restype = POINTER(c_void_p)
objc.class_copyPropertyList.argtypes = [c_void_p, POINTER(c_uint)]

# Protocol ** class_copyProtocolList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Protocol* describing protocols.
# The array has *outCount pointers followed by a NULL terminator.
# You must free() the returned array.
objc.class_copyProtocolList.restype = POINTER(c_void_p)
objc.class_copyProtocolList.argtypes = [c_void_p, POINTER(c_uint)]

# id class_createInstance(Class cls, size_t extraBytes)
objc.class_createInstance.restype = c_void_p
objc.class_createInstance.argtypes = [c_void_p, c_size_t]

# Method class_getClassMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
objc.class_getClassMethod.restype = c_void_p
objc.class_getClassMethod.argtpes = [c_void_p, c_void_p]

# Ivar class_getClassVariable(Class cls, const char* name)
objc.class_getClassVariable.restype = c_void_p
objc.class_getClassVariable.argtypes = [c_void_p, c_char_p]

# Method class_getInstanceMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
objc.class_getInstanceMethod.restype = c_void_p
objc.class_getInstanceMethod.argtypes = [c_void_p, c_void_p]

# size_t class_getInstanceSize(Class cls)
objc.class_getInstanceSize.restype = c_size_t
objc.class_getInstanceSize.argtypes = [c_void_p]

# Ivar class_getInstanceVariable(Class cls, const char* name)
objc.class_getInstanceVariable.restype = c_void_p
objc.class_getInstanceVariable.argtypes = [c_void_p, c_char_p]

# const char *class_getIvarLayout(Class cls)
objc.class_getIvarLayout.restype = c_char_p
objc.class_getIvarLayout.argtypes = [c_void_p]

# IMP class_getMethodImplementation(Class cls, SEL name)
objc.class_getMethodImplementation.restype = c_void_p
objc.class_getMethodImplementation.argtypes = [c_void_p, c_void_p]

# IMP class_getMethodImplementation_stret(Class cls, SEL name)
objc.class_getMethodImplementation_stret.restype = c_void_p
objc.class_getMethodImplementation_stret.argtypes = [c_void_p, c_void_p]

# const char * class_getName(Class cls)
objc.class_getName.restype = c_char_p
objc.class_getName.argtypes = [c_void_p]

# objc_property_t class_getProperty(Class cls, const char *name)
objc.class_getProperty.restype = c_void_p
objc.class_getProperty.argtypes = [c_void_p, c_char_p]

# Class class_getSuperclass(Class cls)
objc.class_getSuperclass.restype = c_void_p
objc.class_getSuperclass.argtypes = [c_void_p]

# int class_getVersion(Class theClass)
objc.class_getVersion.restype = c_int
objc.class_getVersion.argtypes = [c_void_p]

# const char *class_getWeakIvarLayout(Class cls)
objc.class_getWeakIvarLayout.restype = c_char_p
objc.class_getWeakIvarLayout.argtypes = [c_void_p]

# BOOL class_isMetaClass(Class cls)
objc.class_isMetaClass.restype = c_bool
objc.class_isMetaClass.argtypes = [c_void_p]

# IMP class_replaceMethod(Class cls, SEL name, IMP imp, const char *types)
objc.class_replaceMethod.restype = c_void_p
objc.class_replaceMethod.argtypes = [c_void_p, c_void_p, c_void_p, c_char_p]

# BOOL class_respondsToSelector(Class cls, SEL sel)
objc.class_respondsToSelector.restype = c_bool
objc.class_respondsToSelector.argtypes = [c_void_p, c_void_p]

# void class_setIvarLayout(Class cls, const char *layout)
objc.class_setIvarLayout.restype = None
objc.class_setIvarLayout.argtypes = [c_void_p, c_char_p]

# Class class_setSuperclass(Class cls, Class newSuper)
objc.class_setSuperclass.restype = c_void_p
objc.class_setSuperclass.argtypes = [c_void_p, c_void_p]

# void class_setVersion(Class theClass, int version)
objc.class_setVersion.restype = None
objc.class_setVersion.argtypes = [c_void_p, c_int]

# void class_setWeakIvarLayout(Class cls, const char *layout)
objc.class_setWeakIvarLayout.restype = None
objc.class_setWeakIvarLayout.argtypes = [c_void_p, c_char_p]

######################################################################

# const char * ivar_getName(Ivar ivar)
objc.ivar_getName.restype = c_char_p
objc.ivar_getName.argtypes = [c_void_p]

# ptrdiff_t ivar_getOffset(Ivar ivar)
objc.ivar_getOffset.restype = c_ptrdiff_t
objc.ivar_getOffset.argtypes = [c_void_p]

# const char * ivar_getTypeEncoding(Ivar ivar)
objc.ivar_getTypeEncoding.restype = c_char_p
objc.ivar_getTypeEncoding.argtypes = [c_void_p]

######################################################################

# char * method_copyArgumentType(Method method, unsigned int index)
# You must free() the returned string.
objc.method_copyArgumentType.restype = c_char_p
objc.method_copyArgumentType.argtypes = [c_void_p, c_uint]

# char * method_copyReturnType(Method method)
# You must free() the returned string.
objc.method_copyReturnType.restype = c_char_p
objc.method_copyReturnType.argtypes = [c_void_p]

# void method_exchangeImplementations(Method m1, Method m2)
objc.method_exchangeImplementations.restype = None
objc.method_exchangeImplementations.argtypes = [c_void_p, c_void_p]

# void method_getArgumentType(Method method, unsigned int index, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, parameter_type, dst_len).
objc.method_getArgumentType.restype = None
objc.method_getArgumentType.argtypes = [c_void_p, c_uint, c_char_p, c_size_t]

# IMP method_getImplementation(Method method)
objc.method_getImplementation.restype = c_void_p
objc.method_getImplementation.argtypes = [c_void_p]

# SEL method_getName(Method method)
objc.method_getName.restype = c_void_p
objc.method_getName.argtypes = [c_void_p]

# unsigned method_getNumberOfArguments(Method method)
objc.method_getNumberOfArguments.restype = c_uint
objc.method_getNumberOfArguments.argtypes = [c_void_p]

# void method_getReturnType(Method method, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, return_type, dst_len)
objc.method_getReturnType.restype = None
objc.method_getReturnType.argtypes = [c_void_p, c_char_p, c_size_t]

# const char * method_getTypeEncoding(Method method)
objc.method_getTypeEncoding.restype = c_char_p
objc.method_getTypeEncoding.argtypes = [c_void_p]

# IMP method_setImplementation(Method method, IMP imp)
objc.method_setImplementation.restype = c_void_p
objc.method_setImplementation.argtypes = [c_void_p, c_void_p]

######################################################################

# Class objc_allocateClassPair(Class superclass, const char *name, size_t extraBytes)
objc.objc_allocateClassPair.restype = c_void_p
objc.objc_allocateClassPair.argtypes = [c_void_p, c_char_p, c_size_t]

# Protocol **objc_copyProtocolList(unsigned int *outCount)
# Returns an array of *outcount pointers followed by NULL terminator.
# You must free() the array.
objc.objc_copyProtocolList.restype = POINTER(c_void_p)
objc.objc_copyProtocolList.argtypes = [POINTER(c_int)]

# id objc_getAssociatedObject(id object, void *key)
objc.objc_getAssociatedObject.restype = c_void_p
objc.objc_getAssociatedObject.argtypes = [c_void_p, c_void_p]

# id objc_getClass(const char *name)
objc.objc_getClass.restype = c_void_p
objc.objc_getClass.argtypes = [c_char_p]

# int objc_getClassList(Class *buffer, int bufferLen)
# Pass None for buffer to obtain just the total number of classes.
objc.objc_getClassList.restype = c_int
objc.objc_getClassList.argtypes = [c_void_p, c_int]

# id objc_getMetaClass(const char *name)
objc.objc_getMetaClass.restype = c_void_p
objc.objc_getMetaClass.argtypes = [c_char_p]

# Protocol *objc_getProtocol(const char *name)
objc.objc_getProtocol.restype = c_void_p
objc.objc_getProtocol.argtypes = [c_char_p]

# You should set return and argument types depending on context.
# id objc_msgSend(id theReceiver, SEL theSelector, ...)
# id objc_msgSendSuper(struct objc_super *super, SEL op,  ...)

# void objc_msgSendSuper_stret(struct objc_super *super, SEL op, ...)
objc.objc_msgSendSuper_stret.restype = None

# double objc_msgSend_fpret(id self, SEL op, ...)
# objc.objc_msgSend_fpret.restype = c_double

# void objc_msgSend_stret(void * stretAddr, id theReceiver, SEL theSelector,  ...)
objc.objc_msgSend_stret.restype = None

# void objc_registerClassPair(Class cls)
objc.objc_registerClassPair.restype = None
objc.objc_registerClassPair.argtypes = [c_void_p]

# void objc_removeAssociatedObjects(id object)
objc.objc_removeAssociatedObjects.restype = None
objc.objc_removeAssociatedObjects.argtypes = [c_void_p]

# void objc_setAssociatedObject(id object, void *key, id value, objc_AssociationPolicy policy)
objc.objc_setAssociatedObject.restype = None
objc.objc_setAssociatedObject.argtypes = [c_void_p, c_void_p, c_void_p, c_int]

######################################################################

# id object_copy(id obj, size_t size)
objc.object_copy.restype = c_void_p
objc.object_copy.argtypes = [c_void_p, c_size_t]

# id object_dispose(id obj)
objc.object_dispose.restype = c_void_p
objc.object_dispose.argtypes = [c_void_p]

# Class object_getClass(id object)
objc.object_getClass.restype = c_void_p
objc.object_getClass.argtypes = [c_void_p]

# const char *object_getClassName(id obj)
objc.object_getClassName.restype = c_char_p
objc.object_getClassName.argtypes = [c_void_p]

# Ivar object_getInstanceVariable(id obj, const char *name, void **outValue)
objc.object_getInstanceVariable.restype = c_void_p
objc.object_getInstanceVariable.argtypes=[c_void_p, c_char_p, c_void_p]

# id object_getIvar(id object, Ivar ivar)
objc.object_getIvar.restype = c_void_p
objc.object_getIvar.argtypes = [c_void_p, c_void_p]

# Class object_setClass(id object, Class cls)
objc.object_setClass.restype = c_void_p
objc.object_setClass.argtypes = [c_void_p, c_void_p]

# Ivar object_setInstanceVariable(id obj, const char *name, void *value)
# Set argtypes based on the data type of the instance variable.
objc.object_setInstanceVariable.restype = c_void_p

# void object_setIvar(id object, Ivar ivar, id value)
objc.object_setIvar.restype = None
objc.object_setIvar.argtypes = [c_void_p, c_void_p, c_void_p]

######################################################################

# const char *property_getAttributes(objc_property_t property)
objc.property_getAttributes.restype = c_char_p
objc.property_getAttributes.argtypes = [c_void_p]

# const char *property_getName(objc_property_t property)
objc.property_getName.restype = c_char_p
objc.property_getName.argtypes = [c_void_p]

######################################################################

# BOOL protocol_conformsToProtocol(Protocol *proto, Protocol *other)
objc.protocol_conformsToProtocol.restype = c_bool
objc.protocol_conformsToProtocol.argtypes = [c_void_p, c_void_p]

class OBJC_METHOD_DESCRIPTION(Structure):
    _fields_ = [ ("name", c_void_p), ("types", c_char_p) ]

# struct objc_method_description *protocol_copyMethodDescriptionList(Protocol *p, BOOL isRequiredMethod, BOOL isInstanceMethod, unsigned int *outCount)
# You must free() the returned array.
objc.protocol_copyMethodDescriptionList.restype = POINTER(OBJC_METHOD_DESCRIPTION)
objc.protocol_copyMethodDescriptionList.argtypes = [c_void_p, c_bool, c_bool, POINTER(c_uint)]

# objc_property_t * protocol_copyPropertyList(Protocol *protocol, unsigned int *outCount)
objc.protocol_copyPropertyList.restype = c_void_p
objc.protocol_copyPropertyList.argtypes = [c_void_p, POINTER(c_uint)]

# Protocol **protocol_copyProtocolList(Protocol *proto, unsigned int *outCount)
objc.protocol_copyProtocolList = POINTER(c_void_p)
objc.protocol_copyProtocolList.argtypes = [c_void_p, POINTER(c_uint)]

# struct objc_method_description protocol_getMethodDescription(Protocol *p, SEL aSel, BOOL isRequiredMethod, BOOL isInstanceMethod)
objc.protocol_getMethodDescription.restype = OBJC_METHOD_DESCRIPTION
objc.protocol_getMethodDescription.argtypes = [c_void_p, c_void_p, c_bool, c_bool]

# const char *protocol_getName(Protocol *p)
objc.protocol_getName.restype = c_char_p
objc.protocol_getName.argtypes = [c_void_p]

######################################################################

# const char* sel_getName(SEL aSelector)
objc.sel_getName.restype = c_char_p
objc.sel_getName.argtypes = [c_void_p]

# SEL sel_getUid(const char *str)
# Use sel_registerName instead.

# BOOL sel_isEqual(SEL lhs, SEL rhs)
objc.sel_isEqual.restype = c_bool
objc.sel_isEqual.argtypes = [c_void_p, c_void_p]

# SEL sel_registerName(const char *str)
objc.sel_registerName.restype = c_void_p
objc.sel_registerName.argtypes = [c_char_p]

######################################################################

def get_selector(name):
    return c_void_p(objc.sel_registerName(name))

def get_class(name):
    return c_void_p(objc.objc_getClass(name))

def get_object_class(obj):
    return c_void_p(objc.object_getClass(obj))

def get_metaclass(name):
    return c_void_p(objc.objc_getMetaClass(name))

def get_superclass_of_object(obj):
    cls = c_void_p(objc.object_getClass(obj))
    return c_void_p(objc.class_getSuperclass(cls))


# http://www.sealiesoftware.com/blog/archive/2008/10/30/objc_explain_objc_msgSend_stret.html
# http://www.x86-64.org/documentation/abi-0.99.pdf  (pp.17-23)
# executive summary: on x86-64, who knows?
def x86_should_use_stret(restype):
    """Try to figure out when a return type will be passed on stack."""
    if type(restype) != type(Structure):
        return False
    if not __LP64__ and sizeof(restype) <= 8:
        return False
    if __LP64__ and sizeof(restype) <= 16:  # maybe? I don't know?
        return False
    return True

# http://www.sealiesoftware.com/blog/archive/2008/11/16/objc_explain_objc_msgSend_fpret.html
def should_use_fpret(restype):
    """Determine if objc_msgSend_fpret is required to return a floating point type."""
    if not __i386__: 
        # Unneeded on non-intel processors
        return False
    if __LP64__ and restype == c_longdouble:
        # Use only for long double on x86_64
        return True
    if not __LP64__ and restype in (c_float, c_double, c_longdouble):
        return True
    return False

# By default, assumes that restype is c_void_p
# and that all arguments are wrapped inside c_void_p.
# Use the restype and argtypes keyword arguments to 
# change these values.  restype should be a ctypes type
# and argtypes should be a list of ctypes types for
# the arguments of the message only.
def send_message(receiver, selName, *args, **kwargs):
    if isinstance(receiver, basestring):
        receiver = get_class(receiver)
    selector = get_selector(selName)
    restype = kwargs.get('restype', c_void_p)
    #print 'send_message', receiver, selName, args, kwargs
    argtypes = kwargs.get('argtypes', [])
    # Choose the correct version of objc_msgSend based on return type.
    if should_use_fpret(restype):
        objc.objc_msgSend_fpret.restype = restype
        objc.objc_msgSend_fpret.argtypes = [c_void_p, c_void_p] + argtypes
        result = objc.objc_msgSend_fpret(receiver, selector, *args)
    elif x86_should_use_stret(restype):
        objc.objc_msgSend_stret.argtypes = [POINTER(restype), c_void_p, c_void_p] + argtypes
        result = restype()
        objc.objc_msgSend_stret(byref(result), receiver, selector, *args)
    else:
        objc.objc_msgSend.restype = restype
        objc.objc_msgSend.argtypes = [c_void_p, c_void_p] + argtypes
        result = objc.objc_msgSend(receiver, selector, *args)
        if restype == c_void_p:
            result = c_void_p(result)
    return result

class OBJC_SUPER(Structure):
    _fields_ = [ ('receiver', c_void_p), ('class', c_void_p) ]

OBJC_SUPER_PTR = POINTER(OBJC_SUPER)

#http://stackoverflow.com/questions/3095360/what-exactly-is-super-in-objective-c
def send_super(receiver, selName, *args, **kwargs):
    #print 'send_super', receiver, selName, args
    if hasattr(receiver, '_as_parameter_'):
        receiver = receiver._as_parameter_
    superclass = get_superclass_of_object(receiver)
    super_struct = OBJC_SUPER(receiver, superclass)
    selector = get_selector(selName)
    restype = kwargs.get('restype', c_void_p)
    argtypes = kwargs.get('argtypes', None)
    objc.objc_msgSendSuper.restype = restype
    if argtypes:
        objc.objc_msgSendSuper.argtypes = [OBJC_SUPER_PTR, c_void_p] + argtypes
    else:
        objc.objc_msgSendSuper.argtypes = None
    result = objc.objc_msgSendSuper(byref(super_struct), selector, *args)
    if restype == c_void_p:
        result = c_void_p(result)
    return result

# After calling create_subclass, you must first register
# it with register_subclass before you may use it.
# You can add new methods after the class is registered,
# but you cannot add any new ivars.
def create_subclass(superclass, name):
    if isinstance(superclass, basestring):
        superclass = get_class(superclass)
    return c_void_p(objc.objc_allocateClassPair(superclass, name, 0))

def register_subclass(subclass):
    objc.objc_registerClassPair(subclass)

# Convenience functions for creating new objects.
def alloc_init(cls):
    return send_message(cls, 'new')

def alloc_init_autorelease(cls):
    return send_message(send_message(cls, 'new'), 'autorelease')

######################################################################

def encoding_for_ctype(vartype):
    typecodes = {c_char:'c', c_int:'i', c_short:'s', c_long:'l', c_longlong:'q',
                 c_ubyte:'C', c_uint:'I', c_ushort:'S', c_ulong:'L', c_ulonglong:'Q',
                 c_float:'f', c_double:'d', c_bool:'B', c_char_p:'*', c_void_p:'@',
                 py_object:'@'}
    return typecodes.get(vartype, '?')

# Note CGBase.h located at
# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreGraphics.framework/Headers/CGBase.h
# defines CGFloat as double if __LP64__, otherwise it's a float.
if __LP64__:
    NSInteger = c_long
    NSUInteger = c_ulong
    CGFloat = c_double
    NSPointEncoding = '{CGPoint=dd}'
    NSSizeEncoding = '{CGSize=dd}'
    NSRectEncoding = '{CGRect={CGPoint=dd}{CGSize=dd}}'
else:
    NSInteger = c_int
    NSUInteger = c_uint
    CGFloat = c_float
    NSPointEncoding = '{_NSPoint=ff}'
    NSSizeEncoding = '{_NSSize=ff}'
    NSRectEncoding = '{_NSRect={_NSPoint=ff}{_NSSize=ff}}'

NSIntegerEncoding = encoding_for_ctype(NSInteger)
NSUIntegerEncoding = encoding_for_ctype(NSUInteger)
CGFloatEncoding = encoding_for_ctype(CGFloat)    

# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSPoint(Structure):
    _fields_ = [ ("x", CGFloat), ("y", CGFloat) ]
CGPoint = NSPoint

class NSSize(Structure):
    _fields_ = [ ("width", CGFloat), ("height", CGFloat) ]

class NSRect(Structure):
    _fields_ = [ ("origin", NSPoint), ("size", NSSize) ]
CGRect = NSRect

def NSMakeSize(w, h):
    return NSSize(w, h)

def NSMakeRect(x, y, w, h):
    return NSRect(NSPoint(x, y), NSSize(w, h))

# NSDate.h
NSTimeInterval = c_double

CFIndex = c_long
UniChar = c_ushort
unichar = c_wchar  # (actually defined as c_ushort in NSString.h, but need ctypes to convert properly)
CGGlyph = c_ushort

# CFRange struct defined in CFBase.h
# This replaces the CFRangeMake(LOC, LEN) macro.
class CFRange(Structure):
    _fields_ = [ ("location", CFIndex), ("length", CFIndex) ]

# NSRange.h  (Note, not defined the same as CFRange)
class NSRange(Structure):
    _fields_ = [ ("location", NSUInteger), ("length", NSUInteger) ]

NSZeroPoint = NSPoint(0,0)

######################################################################

cfunctype_table = {}

def tokenize_encoding(encoding):
    token_list = []
    brace_count = 0
    token = ''
    for c in encoding:
        token += c
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count < 0: # bad encoding
                brace_count = 0
        if brace_count == 0:
            token_list.append(token)
            token = ''
    return token_list

# Limited to basic types and pointers to basic types.
# Does not try to handle arrays, structs, unions, or bitfields.
def cfunctype_for_encoding(encoding):
    # Check if we've already created a CFUNCTYPE for this encoding.
    # If so, then return the cached CFUNCTYPE.
    if encoding in cfunctype_table:
        return cfunctype_table[encoding]

    # Otherwise, create a new CFUNCTYPE for the encoding.
    typecodes = {'c':c_char, 'i':c_int, 's':c_short, 'l':c_long, 'q':c_longlong, 
                 'C':c_ubyte, 'I':c_uint, 'S':c_ushort, 'L':c_ulong, 'Q':c_ulonglong, 
                 'f':c_float, 'd':c_double, 'B':c_bool, 'v':None, '*':c_char_p,
                 '@':c_void_p, '#':c_void_p, ':':c_void_p, NSPointEncoding:NSPoint,
                 NSSizeEncoding:NSSize, NSRectEncoding:NSRect}
    argtypes = []
    pointer = False
    for token in tokenize_encoding(encoding):
        if pointer:
            if token in typecodes:
                argtypes.append(POINTER(typecodes[token]))
                pointer = False
            else:
                raise Exception('unknown encoding')
        else:
            if token in typecodes:
                argtypes.append(typecodes[token])
            elif token == '^':
                pointer = True
            else:
                raise Exception('unknown encoding: ' + token)
    cfunctype = CFUNCTYPE(*argtypes)
    # Cache the new CFUNCTYPE in the cfunctype_table.
    # We do this mainly because it prevents the CFUNCTYPE 
    # from being garbage-collected while we need it.
    cfunctype_table[encoding] = cfunctype
    return cfunctype

######################################################################

# types is a string encoding the argument types of the method.
# The first char of types is the return type ('v' if void)
# The second char must be '@' for id self.
# The third char must be ':' for SEL cmd.
# Additional chars are for types of other arguments if any.
def add_method(cls, selName, method, types):
    assert(types[1:3] == '@:')
    selector = get_selector(selName)
    cfunctype = cfunctype_for_encoding(types)
    imp = cfunctype(method)
    objc.class_addMethod.argtypes = [c_void_p, c_void_p, cfunctype, c_char_p]
    objc.class_addMethod(cls, selector, imp, types)
    return imp

def add_ivar(cls, name, vartype):
    return objc.class_addIvar(cls, name, sizeof(vartype), alignment(vartype), encoding_for_ctype(vartype))

def set_instance_variable(obj, varname, value, vartype):
    objc.object_setInstanceVariable.argtypes = [c_void_p, c_char_p, vartype]
    objc.object_setInstanceVariable(obj, varname, value)
    
def get_instance_variable(obj, varname, vartype):
    variable = vartype()
    objc.object_getInstanceVariable(obj, varname, byref(variable))
    return variable.value

def cast_to_pyobject(obj):
    return cast(obj, py_object).value

######################################################################

cf = cdll.LoadLibrary(util.find_library('CoreFoundation'))

kCFStringEncodingUTF8 = 0x08000100
CFAllocatorRef = c_void_p
CFStringEncoding = c_uint32

cf.CFStringCreateWithCString.restype = c_void_p
cf.CFStringCreateWithCString.argtypes = [CFAllocatorRef, c_char_p, CFStringEncoding]

cf.CFRelease.restype = c_void_p
cf.CFRelease.argtypes = [c_void_p]

cf.CFStringGetLength.restype = CFIndex
cf.CFStringGetLength.argtypes = [c_void_p]

cf.CFStringGetMaximumSizeForEncoding.restype = CFIndex
cf.CFStringGetMaximumSizeForEncoding.argtypes = [CFIndex, CFStringEncoding]

cf.CFStringGetCString.restype = c_bool
cf.CFStringGetCString.argtypes = [c_void_p, c_char_p, CFIndex, CFStringEncoding]

def CFSTR(string):
    return c_void_p(cf.CFStringCreateWithCString(
            None, string.encode('utf8'), kCFStringEncodingUTF8))

def get_NSString(string):
    """Autoreleased version of CFSTR"""
    return send_message(CFSTR(string), 'autorelease')

def cfstring_to_string(cfstring):
    length = cf.CFStringGetLength(cfstring)
    size = cf.CFStringGetMaximumSizeForEncoding(length, kCFStringEncodingUTF8)
    buffer = c_buffer(size + 1)
    result = cf.CFStringGetCString(cfstring, buffer, len(buffer), kCFStringEncodingUTF8)
    if result:
        return unicode(buffer.value, 'utf-8')

cf.CFArrayGetValueAtIndex.restype = c_void_p
cf.CFArrayGetValueAtIndex.argtypes = [c_void_p, CFIndex]

def cfarray_to_list(cfarray):
    count = cf.CFArrayGetCount(cfarray)
    return [ c_void_p(cf.CFArrayGetValueAtIndex(cfarray, i))
             for i in range(count) ]

cf.CFDataCreate.restype = c_void_p
cf.CFDataCreate.argtypes = [c_void_p, c_void_p, CFIndex]

cf.CFDictionaryGetValue.restype = c_void_p
cf.CFDictionaryGetValue.argtypes = [c_void_p, c_void_p]

# Helper function to convert CFNumber to a Python float.
kCFNumberFloatType = 12
def cfnumber_to_float(cfnumber):
    result = c_float()
    if cf.CFNumberGetValue(cfnumber, kCFNumberFloatType, byref(result)):
        return result.value

######################################################################

# This is a factory class which creates Objective-C subclasses.
# The python object created when you instantiate this class
# represents the Objective-C *class*.  It does not represent
# an instance of that class.  Instances are created by using 
# the normal Ojective-C alloc & init messages sent to the
# subclass with send_message.
class ObjCSubclass(object):

    def __init__(self, superclass, name):
        class PythonSelf(object):
            def __init__(self, objc_self):
                self.objc_self = objc_self
                # _as_parameter_ is used if this is passed as an argument
                # and argtypes not set.
                self._as_parameter_ = c_void_p(objc_self)
            def from_param(self):
                # Only called when PythonSelf is given as argtypes
                return c_void_p(self.objc_self)
        self.PythonSelf = PythonSelf

        self._object_table = {}
        self._imp_table = {}
        self.name = name
        self.objc_cls = create_subclass(superclass, name)
        self._as_parameter_ = self.objc_cls
        self.register()
        self.objc_metaclass = get_metaclass(name)

    def register(self):
        register_subclass(self.objc_cls)

    def add_ivar(self, varname, vartype):
        add_ivar(self.objc_cls, varname, vartype)

    def add_method(self, method, name, encoding):
        imp = add_method(self.objc_cls, name, method, encoding)
        self._imp_table[name] = imp

    # http://iphonedevelopment.blogspot.com/2008/08/dynamically-adding-class-objects.html
    def add_class_method(self, method, name, encoding):
        imp = add_method(self.objc_metaclass, name, method, encoding)
        self._imp_table[name] = imp
        
    def get_python_self_for_instance(self, objc_self):
        if isinstance(objc_self, c_void_p):
            objc_self = objc_self.value
        if objc_self in self._object_table:
            py_self = self._object_table[objc_self]
        else:
            py_self = self.PythonSelf(objc_self)
            self._object_table[objc_self] = py_self
        return py_self

    def delete_python_self(self, py_self):
        key = py_self.objc_self
        if hasattr(key, 'value'):
            key = key.value
        if key in self._object_table:
            del self._object_table[key]
        py_self.objc_self = None
        
    def method(self, encoding):
        """Function decorator for instance methods."""
        # Add encodings for hidden self and cmd arguments.
        encoding = encoding[0] + '@:' + encoding[1:]
        def decorator(f):
            def objc_method(objc_self, objc_cmd, *args):
                py_self = self.get_python_self_for_instance(objc_self)
                py_self.objc_cmd = objc_cmd
                result = f(py_self, *args)
                py_self.objc_self = objc_self   # restore in case accidentally changed
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
                self.objc_cmd = objc_cmd
                return f(self, *args)
            name = f.func_name.replace('_', ':')
            self.add_class_method(objc_class_method, name, encoding)
            return objc_class_method
        return decorator

    def initmethod(self, encoding):
        """Function decorator for instance initializer method."""
        # Add encodings for hidden self and cmd arguments.
        encoding = encoding[0] + '@:' + encoding[1:]
        def decorator(f):
            def objc_init_method(objc_self, objc_cmd, *args):
                py_self = self.get_python_self_for_instance(objc_self)
                py_self.objc_cmd = objc_cmd
                result = f(py_self, *args)
                if isinstance(result, self.PythonSelf):
                    result = result.objc_self
                if isinstance(result, c_void_p):
                    result = result.value
                # Check if the value of objc_self was changed.
                if result != objc_self:
                    # Update entry in object_table.
                    del self._object_table[objc_self]
                    self._object_table[result] = py_self
                return result
            name = f.func_name.replace('_', ':')
            self.add_method(objc_init_method, name, encoding)
            return objc_init_method
        return decorator

    # Your subclass MUST define a dealloc method, otherwise the
    # association PythonSelf object won't get deleted.
    def dealloc(self, f):
        """Function decorator for dealloc method."""
        def objc_method(objc_self, objc_cmd):
            py_self = self.get_python_self_for_instance(objc_self)
            py_self.objc_cmd = objc_cmd
            f(py_self)
            self.delete_python_self(py_self)
        self.add_method(objc_method, 'dealloc', 'v@:')
        return objc_method        

    def pythonmethod(self, f):
        """Function decorator for python-callable methods."""
        setattr(self.PythonSelf, f.func_name, f)
        return f

######################################################################

# Even though we don't use this directly, it must be loaded so that
# we can find the NSApplication, NSWindow, and NSView classes.
appkit = cdll.LoadLibrary(util.find_library('AppKit'))

NSDefaultRunLoopMode = c_void_p.in_dll(appkit, 'NSDefaultRunLoopMode')
NSEventTrackingRunLoopMode = c_void_p.in_dll(appkit, 'NSEventTrackingRunLoopMode')

# /System/Library/Frameworks/AppKit.framework/Headers/NSEvent.h
NSAnyEventMask = 0xFFFFFFFFL     # NSUIntegerMax

NSKeyDown            = 10
NSKeyUp              = 11
NSFlagsChanged       = 12
NSApplicationDefined = 15

NSAlphaShiftKeyMask         = 1 << 16
NSShiftKeyMask              = 1 << 17
NSControlKeyMask            = 1 << 18
NSAlternateKeyMask          = 1 << 19
NSCommandKeyMask            = 1 << 20
NSNumericPadKeyMask         = 1 << 21
NSHelpKeyMask               = 1 << 22
NSFunctionKeyMask           = 1 << 23

NSInsertFunctionKey   = 0xF727
NSDeleteFunctionKey   = 0xF728
NSHomeFunctionKey     = 0xF729
NSBeginFunctionKey    = 0xF72A
NSEndFunctionKey      = 0xF72B
NSPageUpFunctionKey   = 0xF72C
NSPageDownFunctionKey = 0xF72D

# /System/Library/Frameworks/AppKit.framework/Headers/NSWindow.h
NSBorderlessWindowMask		= 0
NSTitledWindowMask		= 1 << 0
NSClosableWindowMask		= 1 << 1
NSMiniaturizableWindowMask	= 1 << 2
NSResizableWindowMask		= 1 << 3

# /System/Library/Frameworks/AppKit.framework/Headers/NSPanel.h
NSUtilityWindowMask		= 1 << 4

# /System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h
NSBackingStoreRetained	        = 0
NSBackingStoreNonretained	= 1
NSBackingStoreBuffered	        = 2

# /System/Library/Frameworks/AppKit.framework/Headers/NSTrackingArea.h
NSTrackingMouseEnteredAndExited  = 0x01
NSTrackingMouseMoved             = 0x02
NSTrackingCursorUpdate 		 = 0x04
NSTrackingActiveInActiveApp 	 = 0x40

# /System/Library/Frameworks/AppKit.framework/Headers/NSOpenGL.h
NSOpenGLPFAAllRenderers       =   1   # choose from all available renderers          
NSOpenGLPFADoubleBuffer       =   5   # choose a double buffered pixel format        
NSOpenGLPFAStereo             =   6   # stereo buffering supported                   
NSOpenGLPFAAuxBuffers         =   7   # number of aux buffers                        
NSOpenGLPFAColorSize          =   8   # number of color buffer bits                  
NSOpenGLPFAAlphaSize          =  11   # number of alpha component bits               
NSOpenGLPFADepthSize          =  12   # number of depth buffer bits                  
NSOpenGLPFAStencilSize        =  13   # number of stencil buffer bits                
NSOpenGLPFAAccumSize          =  14   # number of accum buffer bits                  
NSOpenGLPFAMinimumPolicy      =  51   # never choose smaller buffers than requested  
NSOpenGLPFAMaximumPolicy      =  52   # choose largest buffers of type requested     
NSOpenGLPFAOffScreen          =  53   # choose an off-screen capable renderer        
NSOpenGLPFAFullScreen         =  54   # choose a full-screen capable renderer        
NSOpenGLPFASampleBuffers      =  55   # number of multi sample buffers               
NSOpenGLPFASamples            =  56   # number of samples per multi sample buffer    
NSOpenGLPFAAuxDepthStencil    =  57   # each aux buffer has its own depth stencil    
NSOpenGLPFAColorFloat         =  58   # color buffers store floating point pixels    
NSOpenGLPFAMultisample        =  59   # choose multisampling                         
NSOpenGLPFASupersample        =  60   # choose supersampling                         
NSOpenGLPFASampleAlpha        =  61   # request alpha filtering                      
NSOpenGLPFARendererID         =  70   # request renderer by ID                       
NSOpenGLPFASingleRenderer     =  71   # choose a single renderer for all screens     
NSOpenGLPFANoRecovery         =  72   # disable all failure recovery systems         
NSOpenGLPFAAccelerated        =  73   # choose a hardware accelerated renderer       
NSOpenGLPFAClosestPolicy      =  74   # choose the closest color buffer to request   
NSOpenGLPFARobust             =  75   # renderer does not need failure recovery      
NSOpenGLPFABackingStore       =  76   # back buffer contents are valid after swap    
NSOpenGLPFAMPSafe             =  78   # renderer is multi-processor safe             
NSOpenGLPFAWindow             =  80   # can be used to render to an onscreen window  
NSOpenGLPFAMultiScreen        =  81   # single window can span multiple screens      
NSOpenGLPFACompliant          =  83   # renderer is opengl compliant                 
NSOpenGLPFAScreenMask         =  84   # bit mask of supported physical screens       
NSOpenGLPFAPixelBuffer        =  90   # can be used to render to a pbuffer           
NSOpenGLPFARemotePixelBuffer  =  91   # can be used to render offline to a pbuffer   
NSOpenGLPFAAllowOfflineRenderers = 96 # allow use of offline renderers               
NSOpenGLPFAAcceleratedCompute =  97   # choose a hardware accelerated compute device 
NSOpenGLPFAVirtualScreenCount = 128   # number of virtual screens in this format     

NSOpenGLCPSwapInterval        = 222


# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     CoreGraphics.framework/Headers/CGImage.h
kCGImageAlphaNone                   = 0
kCGImageAlphaPremultipliedLast      = 1
kCGImageAlphaPremultipliedFirst     = 2
kCGImageAlphaLast                   = 3
kCGImageAlphaFirst                  = 4
kCGImageAlphaNoneSkipLast           = 5
kCGImageAlphaNoneSkipFirst          = 6
kCGImageAlphaOnly                   = 7

kCGBitmapAlphaInfoMask              = 0x1F
kCGBitmapFloatComponents            = 1 << 8

kCGBitmapByteOrderMask              = 0x7000
kCGBitmapByteOrderDefault           = 0 << 12
kCGBitmapByteOrder16Little          = 1 << 12
kCGBitmapByteOrder32Little          = 2 << 12
kCGBitmapByteOrder16Big             = 3 << 12
kCGBitmapByteOrder32Big             = 4 << 12

# NSApplication.h
NSApplicationPresentationDefault = 0
NSApplicationPresentationHideDock = 1 << 1
NSApplicationPresentationHideMenuBar = 1 << 3
NSApplicationPresentationDisableProcessSwitching = 1 << 5
NSApplicationPresentationDisableHideApplication = 1 << 8

######################################################################

quartz = cdll.LoadLibrary(util.find_library('quartz'))

CGDirectDisplayID = c_uint32     # CGDirectDisplay.h
CGError = c_int32                # CGError.h

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     ImageIO.framework/Headers/CGImageProperties.h
kCGImagePropertyGIFDictionary = c_void_p.in_dll(quartz, 'kCGImagePropertyGIFDictionary')
kCGImagePropertyGIFDelayTime = c_void_p.in_dll(quartz, 'kCGImagePropertyGIFDelayTime')

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     CoreGraphics.framework/Headers/CGColorSpace.h
kCGRenderingIntentDefault = 0

quartz.CGDisplayIDToOpenGLDisplayMask.restype = c_uint32
quartz.CGDisplayIDToOpenGLDisplayMask.argtypes = [c_uint32]

quartz.CGMainDisplayID.restype = c_uint32

quartz.CGShieldingWindowLevel.restype = c_int32

quartz.CGCursorIsVisible.restype = c_bool

quartz.CGDisplayCopyAllDisplayModes.restype = c_void_p
quartz.CGDisplayCopyAllDisplayModes.argtypes = [CGDirectDisplayID, c_void_p]

quartz.CGDisplayModeGetRefreshRate.restype = c_double
quartz.CGDisplayModeGetRefreshRate.argtypes = [c_void_p]

quartz.CGDisplayModeCopyPixelEncoding.restype = c_void_p
quartz.CGDisplayModeCopyPixelEncoding.argtypes = [c_void_p]

quartz.CGGetActiveDisplayList.restype = CGError
quartz.CGGetActiveDisplayList.argtypes = [c_uint32, POINTER(CGDirectDisplayID), POINTER(c_uint32)]

quartz.CGDisplayBounds.restype = CGRect
quartz.CGDisplayBounds.argtypes = [CGDirectDisplayID]

quartz.CGImageSourceCreateWithData.restype = c_void_p
quartz.CGImageSourceCreateWithData.argtypes = [c_void_p, c_void_p]

quartz.CGImageSourceCreateImageAtIndex.restype = c_void_p
quartz.CGImageSourceCreateImageAtIndex.argtypes = [c_void_p, c_size_t, c_void_p]

quartz.CGImageSourceCopyPropertiesAtIndex.restype = c_void_p
quartz.CGImageSourceCopyPropertiesAtIndex.argtypes = [c_void_p, c_size_t, c_void_p]

quartz.CGImageGetDataProvider.restype = c_void_p
quartz.CGImageGetDataProvider.argtypes = [c_void_p]

quartz.CGDataProviderCopyData.restype = c_void_p
quartz.CGDataProviderCopyData.argtypes = [c_void_p]

quartz.CGDataProviderCreateWithCFData.restype = c_void_p
quartz.CGDataProviderCreateWithCFData.argtypes = [c_void_p]

quartz.CGImageCreate.restype = c_void_p
quartz.CGImageCreate.argtypes = [c_size_t, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, c_uint32, c_void_p, c_void_p, c_bool, c_int]

quartz.CGColorSpaceCreateDeviceRGB.restype = c_void_p

quartz.CGDataProviderRelease.restype = None
quartz.CGDataProviderRelease.argtypes = [c_void_p]

quartz.CGColorSpaceRelease.restype = None
quartz.CGColorSpaceRelease.argtypes = [c_void_p]

quartz.CGWarpMouseCursorPosition.restype = CGError
quartz.CGWarpMouseCursorPosition.argtypes = [CGPoint]

quartz.CGDisplayMoveCursorToPoint.restype = CGError
quartz.CGDisplayMoveCursorToPoint.argtypes = [CGDirectDisplayID, CGPoint]

quartz.CGAssociateMouseAndMouseCursorPosition.restype = CGError
quartz.CGAssociateMouseAndMouseCursorPosition.argtypes = [c_bool]

######################################################################

foundation = cdll.LoadLibrary(util.find_library('Foundation'))
foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]
