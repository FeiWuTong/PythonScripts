import re
from bs4 import BeautifulSoup
import os
import requests

url = ''
path = ''

def html_content(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.content
    except:
        traceback.print_exc()
        return ""

def parse_per_page(url):
    soup = BeautifulSoup(html_content(url), 'html.parser')
    info = None
    return info

def save_info(info):
    with open(path, 'w') as f:
        f.write(info)

def GetInfo(url):
    info = parse_per_page(url)
    save_info(info)


if __name__ == '__main__':
    GetInfo(url)
