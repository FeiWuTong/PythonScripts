#! python3

#----------------------------------------------------------------------------
# Author:           LJT
#
# Import Name:      Basic
# Purpose:          API for external
#
# Func Summary:     htmlSoup(url, session, headers, encoding='UTF-8')
#----------------------------------------------------------------------------


from bs4 import BeautifulSoup
import requests
import traceback


def htmlSoup(url, session, headers, encoding='UTF-8'):
    try:
        html = session.get(url, headers=headers)
        html.raise_for_status()
        html.encoding = encoding
        return BeautifulSoup(html.content, 'html.parser')
    except:
        return ""
