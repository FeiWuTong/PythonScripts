# -*- coding: utf-8 -*-
import pyHook
import pythoncom
import threading

flag = False

def onKeyboardevt(evt):
    print evt.KeyID
    print type(evt.KeyID)

    global flag
    
    if evt.KeyID in [162, 163]:
        flag = True
    else:
        if evt.KeyID == 190 and flag:
            print 'get it'
        flag = False

    return True

class main(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        hm = pyHook.HookManager()
        hm.KeyDown = onKeyboardevt
        hm.HookKeyboard()
        pythoncom.PumpMessages()

if __name__ == '__main__':
    t = main()
    t.start()
