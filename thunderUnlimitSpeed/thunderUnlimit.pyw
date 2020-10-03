#! python2
# -*- coding: utf-8 -*-

import sqlite3 as sql
import wx
import os
import re
import time
import sys

dbpath = 'dbpath'

class Entry(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Unlimit', size=(500,350), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.SetIcon(wx.Icon(name='Thunder.ico', type=wx.BITMAP_TYPE_ICO))
        
        self.dbpath = ''
        self.dblink = None
        self.dbcursor = None
        if os.path.exists(dbpath):
            with open(dbpath, 'r') as f:
                self.dbpath = unicode(f.readline())
            self.dblink = sql.connect(self.dbpath)
            self.dbcursor = self.dblink.cursor()
        col_list = ['TaskID', 'Status']

        panel = wx.Panel(self, wx.ID_ANY)
        self.tasklist = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
        for i, label in enumerate(col_list):
            self.tasklist.InsertColumn(i, label, wx.LIST_FORMAT_CENTER)
            self.tasklist.SetColumnWidth(i, self.tasklist.GetColumnWidth(i)*2)
        btn_file = wx.Button(panel, -1, 'DBFile')
        btn_check = wx.Button(panel, -1, 'Check')
        btn_unlimit = wx.Button(panel, -1, 'Unlimit')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(btn_check, 0, wx.ALL, border=5)
        vbox.Add(btn_unlimit, 0, wx.ALL, border=5)
        vbox.AddSpacer(50)
        vbox.Add(btn_file, 0, wx.ALL, border=5)
        hbox.Add(self.tasklist, 1, wx.ALL|wx.EXPAND, border=5)
        hbox.Add(vbox, 0, wx.ALIGN_CENTER)

        panel.SetSizer(hbox)

        btn_check.Bind(wx.EVT_BUTTON, self.check)
        btn_unlimit.Bind(wx.EVT_BUTTON, self.unlimit)
        btn_file.Bind(wx.EVT_BUTTON, self.set_dbpath)
        self.Bind(wx.EVT_CLOSE, self.close)

        self.reload_list()

    def reload_list(self):
        if self.dbcursor is None:
            return
        self._get_record()

        self.tasklist.DeleteAllItems()
        status = ['Unlimited', 'Limited', 'UnSpeedup']
        for tb_item in self.record_list:
            for item in tb_item[1]:
                localtaskid = long(item[0])
                buff = item[3]
                attribute = eval(str(buff))
                index = self.tasklist.InsertStringItem(sys.maxint, str(localtaskid))
                if attribute.has_key('Result') is False:
                    self.tasklist.SetStringItem(index, 1, status[2])
                else:
                    result = attribute['Result']
                    if result == 0:
                        self.tasklist.SetStringItem(index, 1, status[0])
                    else:
                        self.tasklist.SetStringItem(index, 1, status[1])
        self.tasklist.SortItems(self.status_cmp)

    def _get_record(self):
        self.dbcursor.execute("select name from sqlite_master where type='table';")
        tblist = self.dbcursor.fetchall()
        tblist = map(lambda tp: tp[0], tblist)
        tblist = filter(lambda tb_name: True if re.match('AccelerateTaskMap\d+_superspeed_[\d_]+', tb_name) is not None else False, tblist)
        self.record_list = []
        for tb in tblist:
            self.dbcursor.execute("select * from "+tb+";")
            temp = self.dbcursor.fetchall()
            if temp:
                self.record_list.append((tb, temp))

    def check(self, evt):
        if not self.dbpath:
            wx.MessageBox('Choose dat file at first !', 'Error', wx.OK)
            return
        self.dblink = sql.connect(self.dbpath)
        self.dbcursor = self.dblink.cursor()
        self.reload_list()

    def unlimit(self, evt):
        index = self.tasklist.GetFirstSelected()
        if index == -1:
            wx.MessageBox('Choose task(s) at first !', 'Error', wx.OK)
            return
        self._unlimit(index)
        while True:
            index = self.tasklist.GetNextSelected(index)
            if index == -1:
                break
            self._unlimit(index)
        self.reload_list()
        wx.MessageBox('Unlimit has finished !', 'Infomation', wx.OK)

    def _unlimit(self, index):
        if self.tasklist.GetItem(index, 1).GetText() == 'Unlimited':
            return
        else:
            taskid = long(self.tasklist.GetItemText(index))
            for tb_item in self.record_list:
                for item in tb_item[1]:
                    v1 = long(item[0])
                    v2 = item[1]
                    v3 = item[2]
                    buff = item[3]
                    attribute = str(buff).split(',')
                    if v1 == taskid:
                        attribute[-2] = '"Result":0'
                        buff = buffer(','.join(attribute))
                        self.dbcursor.execute("delete from "+tb_item[0]+" where LocalTaskId=?", (v1,))
                        self.dbcursor.execute("insert into "+tb_item[0]+" values(?,?,?,?)", (v1,v2,v3,buff))
                        self.dblink.commit()
                        return

    def set_dbpath(self, evt):
        dlg = wx.FileDialog(None, 'Choose', '', '', 'Database(*.dat)|*.dat',
                            wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.dbpath = dlg.GetPath()
            with open(dbpath, 'w') as f:
                f.write(self.dbpath)
        dlg.Destroy()

    def close(self, evt):
        if self.dblink is not None:
            self.dblink.close()
        self.Destroy()

    def get_time(self, time_int):
        return time.asctime(time.localtime(time_int))

    def status_cmp(self, item1, item2):
        id_list = [item1, item2]
        id_lv = []
        for i in id_list:
            if self.tasklist.GetItem(i, 1).GetText() == 'Limited':
                id_lv.append(0)
            elif self.tasklist.GetItem(i, 1).GetText() == 'UnSpeedup':
                id_lv.append(1)
            elif self.tasklist.GetItem(i, 1).GetText() == 'Unlimited':
                id_lv.append(2)
        if id_lv[0] < id_lv[1]:
            return -1
        elif id_lv[0] > id_lv[1]:
            return 1
        return 0


if __name__ == '__main__':
    app = wx.App()
    entry = Entry()
    entry.Center()
    entry.Show()
    app.MainLoop()
