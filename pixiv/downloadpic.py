#! python3

#----------------------------------------------------------------------------
# Author:           LJT
#
# Import Name:      downloadpic
# Class Name:       DownloadPic
# Purpose:          API for external
#
# Func Summary:     __init__(self, session, headers)
#                   info_to_save(self, url)
#----------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import os
import re
import settings
from Basic import htmlSoup

class DownloadPic:
    def __init__(self, session, headers):
        # request need
        self.session = session
        self.headers = headers

    # Get Pic per address (address of the pic)
    # title is pic's name on the web
    def get_single_pic_info(self, url, title):
        soup = htmlSoup(url, self.session, self.headers)
        link = soup.find('div', attrs={'class': '_illust_modal _hidden ui-modal-close-box'}).find('img').get('data-src')
        whole_name = title + "." + link.split('.')[-1]
        return (whole_name, link)

    # Get Pics per address
    # url is the pic's exhibition's url
    def get_mul_pics_info(self, url, num, title):
        url = re.sub('mode=medium', 'mode=manga_big', url)
        urls = []
        for i in range(num):
            urls.append((title+"_p"+str(i), url+"&page="+str(i)))
        return urls

    # Judge single or mul and return its title
    def pic_is_mul(self, url):
        soup = htmlSoup(url, self.session, self.headers)
        num = re.search(r'</li><li>.*?\s(\d*?)P</li>', str(soup.find('ul', attrs={'class': 'meta'})))
        title = soup.find('section', attrs={'class': 'work-info'}).find('h1').string
        title = "(pid-{})".format(re.search('id=(\d+)', url).group(1)) + title
        if num:
            return (int(num.group(1)), title)
        return (1, title)

    # Download fuc
    # headers is needed here (headers are changed while downloading pic)
    def download_pic(self, url, headers, filepath):
        try:
            r = self.session.get(url, headers = headers)
            with open(filepath, 'wb') as f:
                f.write(r.content)
            return True
        except:
            traceback.print_exc()
            return False

    # download fuc of a list
    def download_pics(self, url, num, title):
        for t, u in self.get_mul_pics_info(url, num, title):
            alter_headers = self.headers
            alter_headers['Referer'] = u
            soup = htmlSoup(u, self.session, self.headers)
            link = soup.find('img').get('src')
            pic_name = t + "." + link.split('.')[-1]
            ## may change by different dir
            filepath = settings.dir_path + pic_name
            
            if self.download_pic(link, alter_headers, filepath):
                print('Download {} Successfully'.format(pic_name))
            else:
                print('Fail to download ' + pic_name)

    # get the pic from gotten infomation
    def info_to_save(self, url):
        num, title = pic_is_mul(url)
        if num == 1:
            pic_name, link = self.get_single_pic_info(url, title)
            ## may change by different dir
            filepath = settings.dir_path + pic_name
            # Need to add Different Referer / or it will be 403 or 404
            alter_headers = self.headers
            alter_headers['Referer'] = url
            
            if self.download_pic(link, alter_headers, filepath):
                print('Download {} Successfully'.format(pic_name))
            else:
                print('Fail to download ' + pic_name)
        else:
            # download from a list
            self.download_pics(url, num, title)
