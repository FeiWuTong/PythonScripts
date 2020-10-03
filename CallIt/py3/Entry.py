# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Module:           Entry
# Purpose:          UI
#
# Author:           UuuuuxxxOwO
#
# Created:          8/3/17
#----------------------------------------------------------------------------


import wx
from RecordInfo import RecordInfo
import sys
import os

'''
import pyHook
import pythoncom
'''

class Entry(wx.Frame):

    # Menu Event
    PLATFORM_ID = wx.NewId()
    EXIT_ID = wx.NewId()
    SETTING_ID = wx.NewId()
    TUTORIAL_ID = wx.NewId()
    ABOUT_ID = wx.NewId()

    FRAME_ID = wx.NewId()

    flag = False

    def __init__(self):
        # no Maximize and Resize
        wx.Frame.__init__(self, None, wx.ID_ANY, 'CallIt', size=(400,100), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP)
        self.SetIcon(wx.Icon(name='wx.ico', type=wx.BITMAP_TYPE_ICO))

        panel = wx.Panel(self, wx.ID_ANY)
        menubar = wx.MenuBar()
        menu_operate = wx.Menu()
        menu_setting = wx.Menu()
        menu_other = wx.Menu()

        word_tag = wx.StaticText(panel, -1, 'Word :', size=(-1, -1))
        self.word_write = wx.TextCtrl(panel, -1, '', size=(150,-1), style=wx.TE_PROCESS_ENTER)
        w, h = self.word_write.GetSize()
        self.enter_word = wx.Button(panel, -1, '>>Enter<<', size=(-1, h))
        word_sizer = wx.BoxSizer(wx.HORIZONTAL)
        word_sizer.AddSpacer(40)
        word_sizer.Add(word_tag, 1, wx.ALIGN_CENTER)
        word_sizer.Add(self.word_write, 1, wx.ALIGN_CENTER)
        word_sizer.AddSpacer(20)
        word_sizer.Add(self.enter_word, 1, wx.ALIGN_CENTER)
        word_sizer.AddSpacer(10)
        panel.SetSizer(word_sizer)

        menu_operate.Append(self.PLATFORM_ID, 'App Platform')
        menu_operate.Append(self.EXIT_ID, 'Exit')
        menubar.Append(menu_operate, 'Operate')
        menu_setting.Append(self.SETTING_ID, 'Settings')
        menubar.Append(menu_setting, 'Settings')
        menu_other.Append(self.TUTORIAL_ID, 'Tutorial')
        menu_other.Append(self.ABOUT_ID, 'About')
        menubar.Append(menu_other, 'Other')

        self.taskBarIcon = TaskBarIcon(self)

        '''
        hm = pyHook.HookManager()
        hm.KeyDown = self.showorhide
        hm.HookKeyboard()
        '''

        wx.EVT_MENU(self, self.PLATFORM_ID, self.ProcessEvent)
        wx.EVT_MENU(self, self.EXIT_ID, self.ProcessEvent)
        wx.EVT_MENU(self, self.SETTING_ID, self.ProcessEvent)
        wx.EVT_MENU(self, self.TUTORIAL_ID, self.ProcessEvent)
        wx.EVT_MENU(self, self.ABOUT_ID, self.ProcessEvent)
        self.Bind(wx.EVT_BUTTON, self.enterword, self.enter_word)
        self.Bind(wx.EVT_TEXT_ENTER, self.enterword, self.word_write)
        self.Bind(wx.EVT_CLOSE, self.iconize)

        self.SetMenuBar(menubar)

    def ProcessEvent(self, evt):
        id = evt.GetId()
        if id == self.PLATFORM_ID:
            self.check()
        elif id == self.EXIT_ID:
            self.close(evt)
        elif id == self.SETTING_ID:
            self.settings()
        elif id == self.TUTORIAL_ID:
            self.tutorial()
        elif id == self.ABOUT_ID:
            self.about()
        else:
            return

    def check(self):
        app_platform = AppPlatform()
        app_platform.CenterOnParent()
        app_platform.ShowModal()

    def close(self, evt):
        self.taskBarIcon.Destroy()
        self.Destroy()

    def iconize(self, evt):
        self.Hide()

    def settings(self):
        pass

    def tutorial(self):
        pass

    def about(self):
        pass

    def enterword(self, evt):
        word = self.word_write.GetValue()
        path = RecordInfo.get_info(word)
        if path is None:
            wx.MessageBox('No app relate with this word !', 'Error', wx.OK)
            return
        if not os.path.exists(path):
            wx.MessageBox('App has been remove !', 'Error', wx.OK)
            return
        os.startfile(path)
        self.word_write.Clear()

    ''' Next Version Update Part / Accelerator Table
    def showorhide(self, evt):
        if evt.KeyID in [162, 163]:
            self.flag = True
        else:
            if evt.KeyID == 190 and self.flag:
                print 's'
            self.flag = False
        return True
    '''


class TaskBarIcon(wx.TaskBarIcon):

    CLOSE_ID = wx.NewId()
    APP_ID = wx.NewId()
    SETTING_ID = wx.NewId()

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='wx.ico', type=wx.BITMAP_TYPE_ICO), 'CallIt')
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftDClick)
        wx.EVT_MENU(self, self.CLOSE_ID, self.ProcessEvent)
        wx.EVT_MENU(self, self.APP_ID, self.ProcessEvent)
        wx.EVT_MENU(self, self.SETTING_ID, self.ProcessEvent)

    def ProcessEvent(self, evt):
        id = evt.GetId()
        if id == self.APP_ID:
            self.frame.check()
        elif id == self.CLOSE_ID:
            self.frame.close(evt)
        elif id == self.SETTING_ID:
            self.frame.settings()
        else:
            return

    def OnTaskBarLeftDClick(self, evt):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.word_write.SetFocus()
        self.frame.Raise()

    # override
    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.APP_ID, 'App Platform')
        menu.Append(self.SETTING_ID, 'Settings')
        menu.AppendSeparator()
        menu.Append(self.CLOSE_ID, 'Exit')
        return menu
        

class AppPlatform(wx.Dialog):

    CHECK_ID = wx.NewId()
    ADD_ID = wx.NewId()
    ALTER_ID = wx.NewId()
    DELETE_ID = wx.NewId()
    ID_LIST = [CHECK_ID, ADD_ID, ALTER_ID, DELETE_ID]

    def __init__(self):
        wx.Dialog.__init__(self, wx.GetApp().GetTopWindow(), -1, 'AppPlatform', size=(430,600))

        col_list = ['Megic Word', 'Ext', 'Application']

        panel = wx.Panel(self)
        self.listctrl = wx.ListCtrl(panel, -1, size=(400,480), style=wx.LC_REPORT)
        for i, label in enumerate(col_list):
            self.listctrl.InsertColumn(i, label, wx.LIST_FORMAT_CENTER)
            if i == 0:
                self.listctrl.SetColumnWidth(i, self.listctrl.GetColumnWidth(i)*1.5)
            elif i == 2:
                self.listctrl.SetColumnWidth(i, self.listctrl.GetColumnWidth(i)*3.5)
        button_add = wx.Button(panel, self.ADD_ID, 'Add')
        button_check = wx.Button(panel, self.CHECK_ID, 'Check')
        button_alter = wx.Button(panel, self.ALTER_ID, 'Alter')
        button_delete = wx.Button(panel, self.DELETE_ID, 'Delete')
        w, h = button_add.GetSize()
        line = wx.StaticLine(panel, size=(2, h), style=wx.LI_VERTICAL)
        list_operate = wx.StaticBox(panel, -1, 'Application List')
        
        list_operate_box = wx.StaticBoxSizer(list_operate, wx.VERTICAL)
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        total_box = wx.BoxSizer(wx.VERTICAL)

        button_box.Add(button_add)
        button_box.AddSpacer(10)
        button_box.Add(button_alter)
        button_box.AddSpacer(10)
        button_box.Add(button_delete)
        button_box.AddSpacer(12)
        button_box.Add(line)
        button_box.AddSpacer(12)
        button_box.Add(button_check)

        list_operate_box.AddSpacer(5)
        list_operate_box.Add(self.listctrl)
        list_operate_box.AddSpacer(10)
        list_operate_box.Add(button_box)

        total_box.AddSpacer(5)
        total_box.Add(list_operate_box, 1, wx.ALL, border=5)
        total_box.AddSpacer(10)
        
        panel.SetSizer(total_box)

        for ID in self.ID_LIST:
            wx.EVT_BUTTON(panel, ID, self.ProcessEvent)

        self.reload_list()

    def ProcessEvent(self, evt):
        ID = evt.GetId()
        if ID == self.ADD_ID:
            self.add_evt()
        elif ID == self.ALTER_ID:
            self.alter_evt()
        elif ID == self.DELETE_ID:
            self.delete_evt()
        elif ID == self.CHECK_ID:
            self.check_evt()
        else:
            pass

    def add_evt(self):
        add_dlg = add_evt_dialog()
        add_dlg.CenterOnParent()
        add_dlg.ShowModal()
        self.reload_list()

    def alter_evt(self):
        index = self.listctrl.GetFirstSelected()
        if index == -1:
            wx.MessageBox('Must choose one row !', 'Error', wx.OK)
            return
        alter_dlg = add_evt_dialog()
        word = self.listctrl.GetItemText(index)
        path = self.listctrl.GetItem(index, 2).GetText()
        alter_dlg.wordin.SetValue(word)
        alter_dlg.selectpath.SetValue(path)
        alter_dlg.CenterOnParent()
        alter_dlg.ShowModal()
        self.reload_list()

    def delete_evt(self):
        index = self.listctrl.GetFirstSelected()
        if index == -1:
            wx.MessageBox('Must choose one row !', 'Error', wx.OK)
            return
        confirm_dlg = wx.MessageDialog(None, "Confirm deletion?", "Delete", wx.YES_NO|wx.ICON_EXCLAMATION)
        if confirm_dlg.ShowModal() == wx.ID_YES:
            RecordInfo.del_info(self.listctrl.GetItemText(index))
            confirm_dlg.Destroy()
            self.reload_list()

    def check_evt(self):
        for word in RecordInfo.check_info():
            RecordInfo.del_info(word)
        self.reload_list()

    def reload_list(self):
        self.listctrl.DeleteAllItems()
        for word, path in RecordInfo.list_info():
            index = self.listctrl.InsertStringItem(sys.maxint, word)
            ext = os.path.splitext(path)[1]
            if ext:
                self.listctrl.SetStringItem(index, 1, ext[1:])
            else:
                self.listctrl.SetStringItem(index, 1, 'dir')
            self.listctrl.SetStringItem(index, 2, path)

class add_evt_dialog(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, wx.GetApp().GetTopWindow(), -1, 'Add', size=(500,130))

        panel = wx.Panel(self)
        self.selectpath = wx.TextCtrl(panel, size=(350, -1), style=wx.TE_READONLY)
        w, h = self.selectpath.GetSize()
        fileBtn = wx.Button(panel, -1, 'File', size=(60,h))
        dirBtn = wx.Button(panel, -1, 'Dir', size=(60,h))
        self.wordin = wx.TextCtrl(panel, -1, '', size=(350,-1), style=wx.TE_PROCESS_ENTER)
        okBtn = wx.Button(panel, -1, 'OK', size=(60,h))
        wordtag = wx.StaticText(panel, -1, 'Word :')

        path_box = wx.BoxSizer(wx.HORIZONTAL)
        dn_box = wx.BoxSizer(wx.HORIZONTAL)
        total_box = wx.BoxSizer(wx.VERTICAL)

        path_box.AddSpacer(10)
        path_box.Add(fileBtn, 0)
        path_box.AddSpacer(10)
        path_box.Add(self.selectpath, 1)
        path_box.AddSpacer(10)
        path_box.Add(dirBtn, 0)
        path_box.AddSpacer(10)

        dn_box.AddSpacer(20)
        dn_box.Add(wordtag, 0)
        dn_box.AddSpacer(20)
        dn_box.Add(self.wordin, 1)
        dn_box.AddSpacer(50)
        dn_box.Add(okBtn, 0)
        dn_box.AddSpacer(10)

        total_box.AddSpacer(10)
        total_box.Add(path_box)
        total_box.AddSpacer(10)
        total_box.Add(dn_box)

        self.Bind(wx.EVT_TEXT_ENTER, self.enterword, self.wordin)
        fileBtn.Bind(wx.EVT_BUTTON, self.filebtn)
        dirBtn.Bind(wx.EVT_BUTTON, self.dirbtn)
        okBtn.Bind(wx.EVT_BUTTON, self.enterword)

        panel.SetSizer(total_box)

    def enterword(self, evt):
        path = self.selectpath.GetValue()
        word = self.wordin.GetValue()
        if not path or not word:
            wx.MessageBox('No Path or No Word !', 'Error', wx.OK)
            return
        if RecordInfo.get_info(word) is not None:
            confirm_dlg = wx.MessageDialog(None, "Word has existed, replaces the original part ?", "Warn", wx.YES_NO|wx.ICON_EXCLAMATION)
            if confirm_dlg.ShowModal() != wx.ID_YES:
                confirm_dlg.Destroy()
                return
            confirm_dlg.Destroy()
        RecordInfo.set_info(path, word)
        self.Destroy()

    def filebtn(self, evt):
        dlg = wx.FileDialog(self, 'Select File', '', '', 'All Files (*.*)|*.*', wx.FD_OPEN|wx.wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.selectpath.SetValue(dlg.GetPath())
        dlg.Destroy()

    def dirbtn(self, evt):
        dlg = wx.DirDialog(self, 'Select Dir', style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.selectpath.SetValue(dlg.GetPath())
        dlg.Destroy()


class Setting(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, wx.GetApp().GetTopWindow(), -1, 'Settings', size=(230,400))

        settings_list = ['Shortcut key', 'X options', 'Start-up']
        X_choose_label = ['Minimize', 'Close']

        panel = wx.Panel(self)
        button_save = wx.Button(panel, -1, 'Save')
        button_cancel = wx.Button(panel, -1, 'Cancel')

        shortcut_key = wx.StaticBox(panel, -1, settings_list[0])
        X_choose = wx.RadioBox(panel, -1, settings_list[1],
                               wx.DefaultPosition, wx.DefaultSize,
                               X_choose_label, 1,
                               wx.RA_SPECIFY_ROWS|wx.NO_BORDER)
        self.start_choose = wx.CheckBox(panel, -1, settings_list[2])

        shortcut_key_box = wx.StaticBoxSizer(shortcut_key, wx.VERTICAL)
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        total_box = wx.BoxSizer(wx.VERTICAL)

        button_box.Add(button_save)
        button_box.AddSpacer(10)
        button_box.Add(button_cancel)
        total_box.AddSpacer(10)
        total_box.Add(shortcut_key_box, 1, wx.ALL|wx.ALIGN_CENTER, border=5)
        total_box.AddSpacer(10)
        total_box.Add(X_choose, 1, wx.ALL|wx.ALIGN_CENTER, border=5)
        total_box.AddSpacer(10)
        total_box.Add(self.start_choose, 1, wx.ALL|wx.ALIGN_CENTER, border=5)
        total_box.AddSpacer(10)
        total_box.Add(button_box, 1, wx.ALL|wx.ALIGN_CENTER, border=5)

        panel.SetSizer(total_box)

        self.Bind(wx.EVT_BUTTON, self.save_evt, button_save)
        self.Bind(wx.EVT_BUTTON, self.cancel_evt, button_cancel)

    def save_evt(self, evt):
        pass

    def cancel_evt(self, evt):
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    dialog = Entry()
    dialog.Center()
    dialog.Show()
    app.MainLoop()
