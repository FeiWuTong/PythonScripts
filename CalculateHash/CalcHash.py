# -*- coding: utf-8 -*-
#! python3

#----------------------------------------------------------------------------
# Name:             pixiv.py
# Purpose:          Calculate Hash(MD5) of the file
#
# Author:           LJT
#
# Created:          10/30/2018
# Environment:      Windows
# Python Version:   python 3.60
#----------------------------------------------------------------------------

import os
import hashlib

def obj_hash(obj, filename):
    with open(filename, 'rb') as f:
        while True:
            data = f.read(8096)
            if not data:
                break
            obj.update(data)
    return obj.hexdigest()

def calc_md5(filename):
    md5_obj = hashlib.md5()
    return obj_hash(md5_obj, filename)

def calc_sha1(filename):
    sha1_obj = hashlib.sha1()
    return obj_hash(sha1_obj, filename)

def calc_sha256(filename):
    sha256_obj = hashlib.sha256()
    return obj_hash(sha256_obj, filename)

def compare_hash(hashstr1, hashstr2):
    pass

if __name__ == '__main__':
    print("Enter filepath: ", end="")
    filename = input()
    if os.path.isfile(filename):
        print("Enter hash type: ", end="")
        hash_type = input().lower()
        hash_value = None
        if hash_type == 'md5':
            hash_value = calc_md5(filename)
        elif hash_type == 'sha1':
            hash_value = calc_sha1(filename)
        elif hash_type == 'sha256':
            hash_value = calc_sha256(filename)
        if hash_value:
            print(hash_type, "value:", hash_value)
            print("Compare hash value: ", end="")
            comp_value = input()
            if comp_value == hash_value:
                print("Same.")
            else:
                print("Not the same.")
        else:
            print("hash type is not correct")
    else:
        print("File not exist.")
