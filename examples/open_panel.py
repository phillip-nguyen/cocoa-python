# Minimal example of displaying an NSOpenPanel.

import sys
from cocoapy import *

NSApplication = ObjCClass('NSApplication')
NSAutoreleasePool = ObjCClass('NSAutoreleasePool')
NSOpenPanel = ObjCClass('NSOpenPanel')

def show_open_panel():
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(True)
    if panel.runModal():
        return cfstring_to_string(panel.URL().path())
    return None

if __name__ == '__main__':
    # Must create the shared application instance.
    app = NSApplication.sharedApplication()
    # Then we also need an autorelease pool.
    pool = NSAutoreleasePool.alloc().init()
    # Finally we can create and display an NSOpenPanel.
    path = show_open_panel()
    print path
