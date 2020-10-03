# -*- coding: utf-8 -*-
import pyHook
import pythoncom

flag = False

# 鼠标事件监听同理
def onKeyboardevt(evt):
    print "MessageName:", evt.MessageName   
    print "Message:", evt.Message   
    print "Time:", evt.Time   
    print "Window:", evt.Window   
    print "WindowName:", evt.WindowName   
    print "Ascii:", evt.Ascii, chr(evt.Ascii)   
    print "Key:", evt.Key   
    print "KeyID:", evt.KeyID   
    print "ScanCode:", evt.ScanCode   
    print "Extended:", evt.Extended   
    print "Injected:", evt.Injected   
    print "Alt", evt.Alt   
    print "Transition", evt.Transition   
    print "---"
    
    return True

def main():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardevt
    hm.HookKeyboard()

    pythoncom.PumpMessages()

    
if __name__ == '__main__':
    main()
