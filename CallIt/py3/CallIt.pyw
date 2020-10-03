# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:             CallIt.py
# Purpose:          Convenient tool about using "word" to "call" out the app
# Version:          C1.0
#
# Author:           UuuuuxxxOwO
#
# Created:          29/05/18
# Environment:      Windows10
# Python Version:   python 3.70
#----------------------------------------------------------------------------

import Entry
import wx

if __name__ == '__main__':
    app = wx.App()
    entry = Entry.Entry()
    entry.Center()
    entry.Hide()
    app.MainLoop()
