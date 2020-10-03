#! python2
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:             CallIt.py
# Purpose:          Convenient tool about using "word" to "call" out the app
# Version:          C1.0
#
# Author:           UuuuuxxxOwO
#
# Created:          8/3/17
# Environment:      Windows
# Python Version:   python 2.70
#----------------------------------------------------------------------------

import Entry
import wx

if __name__ == '__main__':
    app = wx.App()
    entry = Entry.Entry()
    entry.Center()
    entry.Hide()
    app.MainLoop()
