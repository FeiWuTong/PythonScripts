#! python3

#----------------------------------------------------------------------------
# Author:           LJT
#
# Import Name:      Login
# Class Name:       Login
# Purpose:          API
#
# Func Summary:     __init__(self, session=None, headers=None)
#                   set_session(self, session)
#                   set_headers(self, headers)
#                   set_login_data(self, login_data)
#                   loginPixiv(self)
#----------------------------------------------------------------------------


import pickle
import settings
import requests
import re
from bs4 import BeautifulSoup
import os
import traceback

from Basic import htmlSoup


class Login:
    def __init__(self, session=None, headers=None):
        # request need
        self.session = session
        self.headers = headers
        # post_data
        self.login_data = settings.login_data
        # cookie file
        self.user_file = 'cookie_id'
        # login url
        self.url = settings.login_url

    def set_session(self, session):
        self.session = session

    def set_headers(self, headers):
        self.headers = headers

    def set_login_data(self, login_data):
        self.login_data = login_data

    # Use PID and password to login
    def login_func(self, url):
        # get the random post_key
        r1 = self.session.get(url, headers=self.headers)   # get partial cookies
        r1.encoding = 'UTF-8'
        postkey = re.search(r'name=\"post_key\" value=\"(.+?)\"', r1.text).group(1)
        login_data['post_key'] = postkey
        # login
        session.post(url, data=login_data, headers = headers)

    # check login status
    @staticmethod
    def check_login(check_url, session, headers):
        # check login in or not
        soup = htmlSoup(check_url, session, headers)
        user_name = soup.find('a', attrs={'class': 'user-name js-click-trackable-later'})
        if user_name:
            print("Congratulate \'{}\', login in successfully".format(user_name.string))
            return True
        else:
            return False

    # get cookie filename of current user
    def get_cookie_filename(self):
        if not os.path.exists(self.user_file):
            return ""
        with open(self.user_file, 'r') as f:
            cookie_file = re.search(r''+self.login_data['pixiv_id']+' (.*)', f.read())
            if cookie_file:
                return cookie_file.group(1)
            return ""

    # update cookie filename
    def update_cookie_filename(self):
        if not os.path.exists(self.user_file):
            with open(user_file, 'w') as f:
                f.write("{} {}\n".format('id_total', '000'))
        # add 1 user
        user_count = 0
        with open(self.user_file, 'r+') as f:
            num = f.readline().strip().split()[1]
            user_count = str(int(num)+1)
            f.seek(9)
            f.write("{:0>3}".format(user_count))
        with open(self.user_file, 'a') as f:
            f.write("{} {}\n".format(self.login_data['pixiv_id'],\
                                     "cookies"+str(user_count)))
            return "cookies"+str(user_count)

    # login Process
    def loginPixiv(self):
        # Init Part
        url = self.url
        session = self.session
        headers = self.headers
        
        # last cookie or the new one
        cookie_file = self.get_cookie_filename()
        save_cookie = True

        # read cookies in file
        if os.path.exists(cookie_file):
            with open(cookie_file, 'rb') as f:
                f_read = pickle.load(f)
                if isinstance(f_read, session.cookies):
                    session.cookies = f_read
                    save_cookie = False
        if save_cookie:
            self.login_func(url, session, headers)
            
        # check login in or not
        check_url = settings.domain_url
        if not Login.check_login(check_url, session, headers):
            if save_cookie:
                # login_func does not achieve its goal
                print('Fail to login')
                return False
            else:
                # Maybe cookies have expired
                self.login_func(url, session, headers)
                # login_func does not achieve its goal
                if not Login.check_login(check_url, session, headers):
                    print('Fail to login in')
                    return False
                save_cookie = True

        # save the cookie by pickle      
        if save_cookie:
            if not cookie_file:
                cookie_file = self.update_cookie_filename()
            with open(cookie_file, 'wb') as f:
                pickle.dump(session.cookies, f)
        self.session = session
        return True
