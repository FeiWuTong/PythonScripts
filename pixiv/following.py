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


import requests
from bs4 import BeautifulSoup
import traceback


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
        link = settings.domain_url + i.find('a').get('href')
        picsList.append(link)
    return picsList
