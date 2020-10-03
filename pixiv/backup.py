#! python3

#----------------------------------------------------------------------------
# Name:             pixiv.py
# Purpose:          Crawl the pics from pixiv
# Version:          1.0
#
# Author:           LJT
#
# Created:          7/6/17
# End:              3/6/18
# Environment:      Windows
# Python Version:   python 3.60
#----------------------------------------------------------------------------

import time
import random
import sys
import requests
import re
from bs4 import BeautifulSoup
import pickle
import os
import glob
import traceback
import settings

#######################################################
# Common Rudimentary Part
# *****
# use BeautifulSoup to manipulate
def htmlSoup(url, session, headers, encoding='UTF-8'):
    try:
        html = session.get(url, headers=headers)
        html.raise_for_status()
        html.encoding = encoding
        return BeautifulSoup(html.content, 'html.parser')
    except:
        return ""

#######################################################
# Login Part (Including Login func and Save/Load different id's Cookies)
# *****
# login func
def login_func(url, session, headers):
    # post_data
    login_data = settings.login_data
    # get the random post_key
    r1 = session.get(url, headers=headers) # get partial cookies
    r1.encoding = 'UTF-8'
    postkey = re.search(r'name=\"post_key\" value=\"(.+?)\"', r1.text).group(1)
    login_data['post_key'] = postkey
    # login
    session.post(url, data=login_data, headers = headers)

# *****
# check login status
def check_login(check_url, session, headers):
    # check login in or not
    soup = htmlSoup(check_url, session, headers)
    user_name = soup.find('a', attrs={'class': 'user-name js-click-trackable-later'})
    if user_name:
        print("Congratulate \'{}\', login in successfully".format(user_name.string))
        return True
    else:
        return False

# *****
# get cookie filename of each user
def get_cookie_filename():
    user_file = 'cookie_id'
    if not os.path.exists(user_file):
        return ""
    with open(user_file, 'r') as f:
        cookie_file = re.search(r''+settings.login_data['pixiv_id']+' (.*)', f.read())
        if cookie_file:
            return cookie_file.group(1)
        return ""

# *****
# update cookie filename
def update_cookie_filename():
    user_file = 'cookie_id'
    if not os.path.exists(user_file):
        with open(user_file, 'w') as f:
            f.write("{} {}\n".format('id_total', '000'))
    # add 1 user
    user_count = 0
    with open(user_file, 'r+') as f:
        num = f.readline().strip().split()[1]
        user_count = str(int(num) + 1)
        f.seek(9)
        f.write("{:0>3}".format(user_count))
    with open(user_file, 'a') as f:
        f.write("{} {}\n".format(settings.login_data['pixiv_id'],\
                                 "cookies"+str(user_count)))
        return "cookies"+str(user_count)

# ***** *****
# login Process
def loginPixiv(session):
    # Init Part
    url = settings.login_url
    headers = settings.headers
    
    # last cookie or the new one
    cookie_file = get_cookie_filename()
    save_cookie = True

    # read cookies in file
    if os.path.exists(cookie_file):
        with open(cookie_file, 'rb') as f:
            f_read = pickle.load(f)
            if type(f_read) is type(session.cookies):
                session.cookies = f_read
                save_cookie = False
    if save_cookie:
        login_func(url, session, headers)
        
    # check login in or not
    check_url = settings.domain_url
    if not check_login(check_url, session, headers):
        if save_cookie:
            # login_func does not achieve its goal
            print('Fail to login')
            return False
        else:
            # Maybe cookies have expired
            login_func(url, session, headers)
            # login_func does not achieve its goal
            if not check_login(check_url, session, headers):
                print('Fail to login in')
                return False
            save_cookie = True

    # save the cookie by pickle        
    if save_cookie:
        if not cookie_file:
            cookie_file = update_cookie_filename()
        with open(cookie_file, 'wb') as f:
            pickle.dump(session.cookies, f)
    return True
        
#######################################################
# Download Picture Part
# *****
# Get Pic per address (address of the pic)
def get_single_pic_info(url, session, headers, title):
    soup = htmlSoup(url, session, headers)
    temp = soup.find('div', attrs={'class': '_illust_modal _hidden ui-modal-close-box'})
    if not temp:    # indicate that this pic can not be downloaded(may be a flash)
        return (None, None)
    link = temp.find('img').get('data-src')
    whole_name = title + "." + link.split('.')[-1]
    return (whole_name, link)

# *****
# Get Pics per address
def get_mul_pics_info(url, session, headers, num, title):
    url = re.sub('mode=medium', 'mode=manga_big', url)
    urls = []
    for i in range(num):
        urls.append((title+"_p"+str(i), url+"&page="+str(i)))
    return urls

# *****
# Judge single or mul and return its title
def pic_is_mul(url, session, headers):
    soup = htmlSoup(url, session, headers)
    num = re.search(r'</li><li>.*?\s(\d*?)P</li>', str(soup.find('ul', attrs={'class': 'meta'})))
    title = soup.find('section', attrs={'class': 'work-info'}).find('h1').string
    title = "(pid-{})".format(re.search('id=(\d+)', url).group(1)) + title
    if num:
        return (int(num.group(1)), title)
    return (1, title)

# *****
# download fuc
def download_pic(url, session, headers, filepath):
    try:
        if os.path.exists(filepath):
            return True
        r = session.get(url, headers = headers)
        with open(filepath, 'wb') as f:
            f.write(r.content)
        return True
    except:
        traceback.print_exc()
        return False

# ***** *****
# get the pic from gotten infomation
def info_to_save(url, session, headers, dirpath, pid_dict=None):
    num, title = pic_is_mul(url, session, headers)
    if num == 1:
        pic_name, link = get_single_pic_info(url, session, headers, title)
        if not link or not pic_name:
            return
        ## may change by different dir
        filepath = dirpath + '/' + unlegal_alter(pic_name)
        # Need to add Different Referer
        alter_headers = headers
        alter_headers['Referer'] = url
        
        if download_pic(link, session, alter_headers, filepath):
            try:
                print('Download {} Successfully'.format(pic_name))
            except:
                try:        # some name like pic can't not be type normally
                    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                    pic_name.translate(non_bmp_map)
                    print('Download {} Successfully'.format(pic_name))
                except:
                    print("Download Successfully But Can't not type the name")
        else:
            print('Fail to download ' + pic_name)
    else:
        if pid_dict:
            if pid_dict[re.search('id=(\d+)', url).group(1)] >= num:
                return
        # download from a list
        for ttemp in range(3):
            try:
                download_pics(url, session, headers, num, title, dirpath)
                break
            except:
                if ttemp == 2:
                    print("Error in download_pics. Skip this pic: "+url)
                    continue
                print("Error in download_pics. Try again")
                continue

# *****
# download fuc of a list
def download_pics(url, session, headers, num, title, dirpath):
    for t, u in get_mul_pics_info(url, session, headers, num, title):
        alter_headers = headers
        alter_headers['Referer'] = u
        soup = htmlSoup(u, session, headers)
        link = soup.find('img').get('src')
        pic_name = t + "." + link.split('.')[-1]
        ## may change by different dir
        filepath = dirpath + '/' + unlegal_alter(pic_name)
        
        if download_pic(link, session, alter_headers, filepath):
            try:
                print('Download {} Successfully'.format(pic_name))
            except:
                p_temp = ''.join(re.findall('(pid-\d+).*?(_p\d+)', pic_name)[0])
                print("Download {} Successfully But Can't not type the whole name".format(p_temp))
        else:
            print('Fail to download ' + pic_name)

# *****
# to alter unlegal characters
def unlegal_alter(name):
    for i in settings.unvalid:
        if i in name:
            name = name.replace(i, '_')
    return name

#######################################################
# Directory and Record Part
# *****
# Create dir for painter
def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

# Record the last scrawl id of a single painter
def record_last_id(dir_path, last_id, mul=False):
    with open(dir_path+'/lastID', 'w') as f:
        if not mul:
            f.write(last_id)
        else:
            f.writelines(last_id)

# Read the record id (single one or multi)
def read_last_id(dir_path, mul=False):
    file_path = dir_path + '/lastID'
    if os.path.exists(file_path):
        last_id = None
        with open(file_path, 'r') as f:
            if not mul:
                last_id = f.readline().strip()
            else:
                last_id = []
                for line in f.readlines():
                    last_id.append(line.strip())
        return last_id
    return False

#######################################################
# Following Part
# *****
# get painters info per page
def get_painters_per_page(url, session, headers):
    soup = htmlSoup(url, session, headers)
    painters = soup.find_all('div', attrs={'class': 'userdata'})
    p_list = []
    for i in painters:
        a = i.find('a')
        link = settings.domain_url + a.get('href')
        name = a.get('data-user_name')
        p_list.append((link, name))
    return p_list

# *****
# get all painters info from following
def get_all_painters(session):
    # Init Part
    headers = settings.headers
    url = settings.follow_url
    
    soup = htmlSoup(url, session, headers)
    page_num = 1
    pager = soup.find('div', attrs={'class': '_pager-complex'})
    if pager: # get the last num
        page_num = int(pager.find_all('a')[-2].string)
        while True:
            soup2 = htmlSoup(url+"&p="+str(page_num), session, headers)
            Next = soup2.find('a', attrs={'rel': 'next'})
            if not Next:
                break
            pager = soup2.find('div', attrs={'class': '_pager-complex'})
            page_num = int(pager.find_all('a')[-2].string)
    p_list = []
    for i in range(page_num):
        p_list.extend(get_painters_per_page(url+"&p="+str(i+1), session, headers))
    return p_list


# *****
# download all pic of a painter
def get_painter_pics(url, session):
    # Init Part
    headers = settings.headers    
    if re.search(r'member\.php\?', url):
        url = re.sub(r'member', 'member_illust', url, count=1)
        
    soup = htmlSoup(url, session, headers)
    page_num = 1
    pager = soup.find('div', attrs={'class': 'pager-container'})
    if pager:
        page_num = int(pager.find_all('li')[-1].string)
        while True:
            soup2 = htmlSoup(url+"&type=all&p="+str(page_num), session, headers)
            Next = soup2.find('a', attrs={'rel': 'next'})
            if not Next:
                break
            pager = soup2.find('div', attrs={'class': 'pager-container'})
            page_num = int(pager.find_all('li')[-1].string)
    for i in range(page_num):
        # use yield but not p_list because the list may be large
        # and the download of pics is slower
        yield get_painter_pics_per_page(url+"&type=all&p="+str(i+1), session, headers)

# *****
# per page operation
def get_painter_pics_per_page(url, session, headers):
    soup = htmlSoup(url, session, headers)
    pics = soup.find_all('li', attrs={'class': 'image-item'})
    picsList = []
    for i in pics:
        link = settings.domain_url + i.find('a').get('href')[1:]
        picsList.append(link)
    return picsList

# *****
# download part (record the newest one and download new part next time)
def download_painter_pics(url, session, dirpath):
    pics = glob.glob(dirpath+'/'+'*')
    pid = re.findall('pid-(\d+)', str(pics))    # already download pics
    pid_page_dict = {}
    for i in map(lambda x: re.search('pid-(\d+).*?_p\d+', x), pics):
        if i:
            pid_page = i.group(1)
            if pid_page in pid_page_dict.keys():
                pid_page_dict[pid_page] += 1
            else:
                pid_page_dict[pid_page] = 1
    
    pattern = re.compile('id=(\d+)')
    for urls_page in get_painter_pics(url, session):
        #print("==="+"\n".join(urls_page)+"===")
        for each_url in urls_page:
            this_pid = pattern.search(each_url).group(1)
            if this_pid not in pid or this_pid in pid_page_dict.keys():
                for ttemp in range(3):
                    try:
                        time.sleep(random.randint(8,16)/8)
                        if this_pid in pid_page_dict.keys():
                            info_to_save(each_url, session, settings.headers, dirpath, pid_page_dict)
                        else:
                            info_to_save(each_url, session, settings.headers, dirpath)
                        break
                    except:
                        if ttemp == 2:
                            print("Error in info_to_save. Skip this pic: "+each_url)
                            continue
                        print("Error in info_to_save. Try again: "+each_url)
                        continue

#######################################################
# Menu Part
# Menu1 -- Update favourite painters' works
def menu1(session, headers):
    pass

def _get_favourite_ids():
    filepath = settings.favourite
    if not os.path.exists(filepath):
        return False
    else:
        pids = []
        with open(filepath, 'r') as f:
            for i in f.readlines():
                pids.append(i)
        return pids

def _save_favourite_ids(ids):     # ids must be a list and each \n at the end
    filepath = settings.favourite
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            for i in ids:
                f.writeline(i)
    else:
        origin = []
        with open(filepath, 'r') as f:
            for i in f.readlines():
                origin.append(i)
        origin.extend(ids)
        origin = tuple(origin)
        with open(filepath, 'w') as f:
            f.writelines(list(origin))

def _del_favourite_ids(ids):
    pass

#######################################################
# Favourite Following Auto-Downloading Part
# *****
# The followings in private(hide)
# (Only one page, more can be extended by 'get_all_painters')
def get_painters(session):
    soup = htmlSoup(settings.favourite, session, settings.headers)
    p_list = []
    for i in soup.find_all('div', attrs={'class': 'userdata'}):
        a = i.find('a')
        link = settings.domain_url+a.get('href')
        name = a.get('data-user_name')
        p_list.append((link, name))
    return p_list

def update_downloaded_pics(session):
    for url, name in get_painters(session):
        dirpath = settings.dir_path+'/'+unlegal_alter(name)
        create_dir(dirpath)
        download_painter_pics(url, session, dirpath)
    print('Has downloaded all already.(Except the error part)')

#######################################################
# Main Part
if __name__ == '__main__':
    # Init Part (Create a Session)
    session = requests.Session()
    headers = settings.headers

    # Operate Part
    # Login part
    loginPixiv(session)
    
    # Update favourite painters' pics
    update_downloaded_pics(session)

    # Save a single url's pic(s)
    #info_to_save("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=29217384", session, headers)

    # Dowload all pics of a painter
    #download_painter_pics('https://www.pixiv.net/member.php?id=84644', session)

    # Get all painters' url
    #get_all_painters(session)
