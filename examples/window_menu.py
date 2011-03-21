# Example of using ctypes with Cocoa to create an NSWindow with
# an application menu item for quitting.

from objc_runtime import *

def create_window():
    print 'creating window'
    window = send_message('NSWindow', 'alloc')
    frame = NSMakeRect(100, 100, 300, 300)
    window = send_message(window, 'initWithContentRect:styleMask:backing:defer:',
                          frame,
                          NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask,
                          NSBackingStoreBuffered,
                          0)
    send_message(window, 'setTitle:', NSString("My Awesome Window"))
    send_message(window, 'makeKeyAndOrderFront:', None)
    return window

def create_menu():
    nsapp = send_message('NSApplication', 'sharedApplication')
    menubar = send_message(send_message('NSMenu', 'alloc'), 'init')
    appMenuItem = send_message(send_message('NSMenuItem', 'alloc'), 'init')
    send_message(menubar, 'addItem:', appMenuItem)
    send_message(nsapp, 'setMainMenu:', menubar)
    appMenu = send_message(send_message('NSMenu', 'alloc'), 'init')
    quitItem = send_message('NSMenuItem', 'alloc')
    send_message(quitItem, 'initWithTitle:action:keyEquivalent:',
                 NSString('Quit!'), get_selector('terminate:'), NSString('q'))
    send_message(appMenu, 'addItem:', quitItem)
    send_message(appMenuItem, 'setSubmenu:', appMenu)

def create_autorelease_pool():
    pool = send_message('NSAutoreleasePool', 'alloc')
    pool = send_message(pool, 'init')
    return pool

def application_run():
    app = send_message('NSApplication', 'sharedApplication')
    create_autorelease_pool()
    create_window()
    create_menu()
    send_message(app, 'run')  # never returns

######################################################################

if __name__ == '__main__':
    application_run()

