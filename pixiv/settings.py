#######################################################
# Pixiv options                                       #
#######################################################
# Alter Infomation Here                               #
#######################################################


# Login infomation
# Alter: id & password
login_data = {
    'pixiv_id': '937821701@qq.com',
    'password': 'fay55555',
    'captcha': '',
    'g_recaptcha_response': '',
    'source': 'pc',
    }
# Requests headers
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'https://www.pixiv.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    }


# Different Part Url
# Domain url
domain_url = 'https://www.pixiv.net/'
# Login url
login_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
# Following url
follow_url = 'https://www.pixiv.net/bookmark.php?type=user&rest=show'
# Painters' prefix url
prefix_url = 'https://www.pixiv.net/member.php?'


# Save Pictures Options
# Root directory
dir_path = 'E:/,Mikasa/,Flore'


# Common part
# Favourite painters
favourite = 'https://www.pixiv.net/bookmark.php?type=user&rest=hide'


# Unvalid Name of the files
unvalid = "\/:*?\"<>|"

