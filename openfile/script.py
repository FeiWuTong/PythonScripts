# -*- coding: utf-8 -*-
import win32api
def SetList(l):
    f = open('address.txt', 'r')
    for eachline in f.readlines():
        add = eachline.strip()
        l.append(add)
def Execute(l):
    for x in l:
        win32api.ShellExecute(0, 'open', x, '', '', 1)

if __name__ == '__main__':
    l = []
    SetList(l)
    Execute(l)
    
