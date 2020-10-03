#! python3

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


import os
import settings
import traceback


# Create dir for painter
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

# Record the last scrawl id of a single painter
def record_last_id(dir_path, last_id, mul=False):
    with open(os.path.join(dir_path, 'lastID'), 'w') as f:
        if not mul:
            f.write(last_id)
        else:
            f.writelines(last_id)

# Read the record id (single one or multi)
def read_last_id(dir_path, mul=False):
    file_path = os.path.join(dir_path, 'lastID')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            if not mul:
                last_id = f.readline().strip()
            else:
                last_id = []
                for line in f.readlines():
                    last_id.append(line.strip())
        return last_id
    return False
