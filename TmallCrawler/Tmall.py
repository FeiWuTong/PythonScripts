#! python3

#----------------------------------------------------------------------------
# Name:             Tmall.py
# Info:             Crawl the infomation in Tmall's shopping page
# Version:          0.1
#
# Author:           LJT
#
# Created:          4/1/20
# End:              3/6/18
# Environment:      Windows
# Python Version:   python 3.7.3
#----------------------------------------------------------------------------

import requests
import re
from bs4 import BeautifulSoup
import json


#############
# Settings
#############
# Base settings parameters
settings_filepath = ''
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Cookie': 'lid=yuiiido; cna=7LhyFSUSB0wCAXOcjlk2nzCo; hng=CN%7Czh-CN%7CCNY%7C156; enc=mCwro7Lv61d7%2FD7%2B9hHWIoc7LPq2AQDu6C%2BEdoTj1%2FnhYoCiBkqO95NEmfyW1SA7PYm496pqR%2F7Oy3MQFxNZdQ%3D%3D; t=05ed2ba74470a53a72f27a1c11cdcebc; tracknick=yuiiido; pnm_cku822=; _m_h5_tk=1cc7414ae932a6ddcda7bbb38b431b65_1587995760026; _m_h5_tk_enc=88dc708f982d7935c506e93f23e586d2; dnk=yuiiido; lgc=yuiiido; cookie2=10a218feef8976d484bd8c2265fa39b3; _tb_token_=ee9357df16eb7; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=UtASsssme%2BBq&pas=0&cookie14=UoTUPcXB8T%2FGbw%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dBxGRyPfpH9X8fcxg%3D&id2=UUpmmW9Ff3hBkQ%3D%3D&nk2=Gh6dZJaDZQ%3D%3D; uc4=nk4=0%40GJJWSE%2BvmkGUNz7lliHR7KNn&id4=0%40U2gsFUqx0IEwQ8OXwHHy6L6Fx7kF; sgcookie=EPbUtO6gEqVQtXdVZCEgZ; csg=ad7ffadb; cq=ccp%3D1; x5sec=7b2273686f7073797374656d3b32223a22343165613437313065616535626365306132396166363237376263383336313843506e756d2f5546454976643576436a674d4b4c67414561444449794e7a55794e6a557a4f5451374d513d3d227d; isg=BCkpBeg_U_4PmGxuJcXNSruMONWD9h0oqjwZncsepZBPkkmkE0Yt-BeEVDakCrVg; l=eBgam4FnqK6XG9K3BOfwPurza77OSIRAguPzaNbMiT5P_ufp5JXcWZjzL6Y9C3GVh6kJR3yAaP04BeYBqImOI_AO7n2ZtXDmn'
    }

# Read settings from file
def read_settings():
    pass

def read_urls():
    pass

#############
# General
#############
# entry
def entry():
    while True:
        choose = input("Enter q to quit, 1 to go on:  ")
        if choose == 'q':
            return
        elif choose == '1':
            pass
        else:
            print("Please enter [q] or [1]")

# Get html content
def html_content(url):
    try:
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        return r.content
    except:
        #traceback.print_exc()
        wrong = url+" disconnected or something wrong. Go on..."
        print(wrong)
        return ""

# For temply saving html content to parse
def html_temp_save(url):
    with open('parse2.txt', 'wb') as f:
        f.write(html_content(url))

#############
# Parse
#############
# Parse catalogue
def parse_catalogue(url):
    content = html_content(url)
    soup = BeautifulSoup(content, 'html.parser')

def temp_file_parse():
    with open('parse2.txt', 'r') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    mainpart = soup.find('div')
    info1 = mainpart.find_all('dd', class_='\\"detail\\"')
    info2 = mainpart.find_all('dd', class_='\\"rates\\"')
    print("name\tprice\tsale\tcomments")
    for i in range(len(info2)):
        single_info1 = info1[i]
        name = single_info1.a.string
        price = single_info1.find('span', class_='\\"c-price\\"').string.strip()
        sale = single_info1.find('span', class_='\\"sale-num\\"').string
        comments = info2[i].span.string[4:]
        print("{}\t{}\t{}\t{}".format(name, price, sale, comments))

# Parse single shopping page
def parse_per_page(url):
    pass

#############
# Save
#############
# Save needed infomation
def save_info():
    pass

if __name__ == '__main__':
    #entry()
    #url = "https://jeanswest.tmall.com/i/asynSearch.htm?_ksTS=1588000607009_116&callback=jsonp117&mid=w-14813202680-0&wid=14813202680&path=/category-1348746281.htm&spm=a1z10.5-b-s.w4011-14813202680.510.312822b3oklsEr&scene=taobao_shop&catId=1348746281&pageNo=1&scid=1348746281"
    temp_file_parse()
    
