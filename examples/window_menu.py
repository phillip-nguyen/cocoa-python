# Example of using ctypes with Cocoa to create an NSWindow with
# an application menu item for quitting.

import sys
from cocoapy import *

NSWindow = ObjCClass('NSWindow')
NSApplication = ObjCClass('NSApplication')
NSMenu = ObjCClass('NSMenu')
NSMenuItem = ObjCClass('NSMenuItem')
NSAutoreleasePool = ObjCClass('NSAutoreleasePool')

def create_window():
    print 'creating window'
    frame = NSMakeRect(100, 100, 300, 300)
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask,
        NSBackingStoreBuffered,
        0)
    window.setTitle_(get_NSString("My Awesome Window"))
    window.makeKeyAndOrderFront_(None)
    return window

def create_menu():
    nsapp = NSApplication.sharedApplication()
    menubar = NSMenu.alloc().init()
    appMenuItem = NSMenuItem.alloc().init()
    menubar.addItem_(appMenuItem)
    nsapp.setMainMenu_(menubar)
    appMenu = NSMenu.alloc().init()

    quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        get_NSString('Quit ' + sys.argv[0]), get_selector('terminate:'), get_NSString('q'))
    appMenu.addItem_(quitItem)

    hideItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        get_NSString('Hide ' + sys.argv[0]), get_selector('hide:'), get_NSString('h'))
    appMenu.addItem_(hideItem)

    appMenuItem.setSubmenu_(appMenu)

def create_autorelease_pool():
    pool = NSAutoreleasePool.alloc().init()
    return pool

def application_run():
    app = NSApplication.sharedApplication()
    create_autorelease_pool()
    create_window()
    create_menu()
    app.run()  # never returns

######################################################################

if __name__ == '__main__':
    application_run()

