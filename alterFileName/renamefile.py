# -*- coding: utf-8 -*-
import os
import re

class Rename:
    def __init__(self, paths=None, mode=0):
        if paths is None:
            self._paths = []
        else:
            self._paths = paths
        self._mode = mode
        self._increase = 0
        self._mode1ar = None      # args for different modes
        self._mode2ar = None
        self._mode4ar = None

    def set_paths(self, paths):
        for x in paths:
            if os.path.isfile(x):
                self._paths.append(x)

    def set_mode(self, mode):
        self._mode = mode

    def set_reg(self, reg):
        self._reg = re.compile(reg)

    def set_increase(self, num):
        self._increase = num

    def set_mode1ar(self, left, right):
        self._mode1ar = (left, right)

    def set_mode2ar(self, reg):
        self._mode2ar = reg

    def set_mode4ar(self, prefix, length):
        self._mode4ar = (prefix, length)

    def _rename_file(self, path):
        if self._mode == 0:
            raise ValueError("None mode was chosen")
        
        if not os.path.isfile(path):
            raise ValueError("Wrong path")
        _dir, whole_name = os.path.split(path)
        name, name_ext = whole_name.split('.')

        if self._mode == 1:
            name = self._mode1(name, self._mode1ar[0], self._mode1ar[1])
        elif self._mode == 2:
            name = self._mode2(name, self._mode2ar)
        elif self._mode == 3:
            name = self._mode3(name, self._increase)
            self._increase += 1
        elif self._mode == 4:
            name = self._mode4(name, self._mode4ar[0], self._mode4ar[1],
                               self._increase)
            self._increase += 1
        
        new_path = _dir + '\\' + name + '.' + name_ext
        os.rename(path, new_path)

    def rename_files(self):
        for x in self._paths:
            self._rename_file(x)

    def paths_in_dir(self, dirpath):
        if os.path.isdir(dirpath):
            self.set_paths(map(lambda x: os.path.join(dirpath, x),
                           os.listdir(dirpath)))

    @staticmethod
    def _mode1(name, left, right):  # 1 will be the first, and right is last+1
        name = name[left-1:right]
        return name

    @staticmethod
    def _mode2(name, reg):
        namelist = reg.findall(name)
        if not namelist:
            return             # ignore the unmatch name
        return namelist[0]

    @staticmethod
    def _mode3(name, increase):
        name = str(increase)
        return name

    @staticmethod
    def _mode4(name, prefix, length, increase):   # length is the postfix's length
        if length == 0:
            name = prefix + str(increase)
        elif length < len(str(increase)):
            raise ValueError("mode4's length is shorter than the increase num")
        else:
            name = prefix + '0'*(length-len(str(increase)))\
                   + str(increase)
        return name

if __name__ == '__main__':
    ro = Rename()   # rename object
    # mode1:name[i:j]              mode2:use regex
    # mode3: increase naturally    mode4:common prefix with increase
    ro.paths_in_dir(r'Z:\try')
    ro.set_mode(4)
    ro.set_mode4ar('he', 0)
    ro.set_increase(5)
    ro.rename_files()
