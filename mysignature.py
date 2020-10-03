# -*- coding: utf-8 -*-
#! python3

#----------------------------------------------------------------------------
# Name:             pixiv.py
# Purpose:          Crawl the pics from pixiv
# Version:          1.0
#
# Author:           LJT
#
# Created:          7/6/17
# Environment:      Windows
# Python Version:   python 3.60
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Author:           LJT
#
# Import Name:      Login
# Class Name:       Login
# Purpose:          API for external
#
# Func Summary:     __init__(self, session=None, headers=None)
#                   set_session(self, session)
#                   set_headers(self, headers)
#                   set_login_data(self, login_data)
#                   loginPixiv(self)
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Author:           LJT
#
# Import Name:      gengrid
# Class Name:       GenGridForsaken
# Purpose:          API for external 外部调用接口函数
#
# Func Summary:     __init__(self, var_min, var_max, step) 分别为变量最大最小值区间及步长，均为list格式（适应GA）
#                   get_bits_len(self) 获取基因组位数
#                   get_bits_restrict(self) 获取生成位数的高位限制（即致死基因）
#                   data_2_bin(self, data, index)  将对应index变量的数据转换为对应的二进制
#                   check_restrict(self, bits_list) 检查基因组是否符合限制
#                   genome_bits(self) 随机生成非致死的基因组
#                   decode(self, gen) 对基因组进行解码
#
# Properties:       self.var_len        获取每个变量的编码长度
#                   self.bit_start      获取每个变量的起始位
#                   self.restrict_bits  获取每个变量的限制值
#----------------------------------------------------------------------------
