# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Module:           RecordInfo
# Purpose:          Provide the interface for saving infomation
#
# Author:           UuuuuxxxOwO
#
# Created:          8/3/17
#----------------------------------------------------------------------------

import os
from ConfigParser import ConfigParser


class RecordInfo:
    
    info_path = os.path.join(os.getcwd(), 'callit.ini')
    config = ConfigParser()
    if not os.path.exists(info_path):
        config.write(open(info_path, 'w'))
    config.read(info_path)

    @classmethod
    def set_info(cls, filepath, word):
        if not cls.config.has_section(str(word)):
            cls.config.add_section(str(word))
        cls.config.set(str(word), 'AppPath', filepath)
        cls.config.write(open(cls.info_path, 'w'))

    @classmethod
    def get_info(cls, word):
        if cls.config.has_section(str(word)):
            return cls.config.get(str(word), 'AppPath')
        return None

    @classmethod
    def del_info(cls, word):
        if cls.config.has_section(str(word)):
            cls.config.remove_section(str(word))
            cls.config.write(open(cls.info_path, 'w'))
            return True
        return False

    @classmethod
    def list_info(cls):
        for section in cls.config.sections():
            yield([section, cls.get_info(section)])

    @classmethod
    def check_info(cls):
        l =[]
        for section in cls.config.sections():
            if not os.path.exists(cls.get_info(section)):
                l.append(section)
        return l
