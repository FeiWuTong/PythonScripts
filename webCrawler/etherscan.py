import requests
from bs4 import BeautifulSoup
import re
import time


url = 'https://etherscan.io/block/'
path = 'etherscan3.output'
log = 'etherscan.log'
#blocknum = 7257053
blocknum = 7150000
count = 100000
offset = 96667
# regain the lost page
block_list = [7182372]


def html_content(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.content
    except:
        #traceback.print_exc()
        wrong = url+" disconnected or something wrong. Go on..."
        print(wrong)
        return ""

def parse_per_page(url):
    content = html_content(url)
    if not content:
        return None
    soup = BeautifulSoup(content, 'html.parser')
    tab_content = soup.find('div', 'tab-content')
    info = []
    block_height_div = tab_content.find('div', string='Block Height:').parent
    block_height = block_height_div.find('span').string.strip()
    info.append(block_height)
    transactions_div = tab_content.find('div', string='Transactions:').parent
    transactions_2or1 = transactions_div.find_all('a')
    if transactions_2or1:
        transactions = transactions_2or1[0].string
        transactions = re.search('\d+', transactions).group()
        info.append(transactions)
        if len(transactions_2or1) > 1:
            transactions_contract = transactions_2or1[1].string
            transactions_contract = re.search('\d+', transactions_contract).group()
            info.append(transactions_contract)
        else:
            info.append('0')
    else:
        info.append('0')
        info.append('0')
    size_div = tab_content.find('div', string='Size:').find_next_siblings('div')[0]
    size = size_div.string.strip()
    info.append(size)
    return info

def parse_timestamp(url):
    soup = BeautifulSoup(html_content(url), 'html.parser')
    timestamp_div = soup.find('div', string='TimeStamp:').parent
    timestamp_strings = timestamp_div.find('i').parent.stripped_strings
    timestamp = ""
    for string in timestamp_strings:
        timestamp = string
    timestamp = re.search('\((.*?)\)', timestamp).group(1)
    return timestamp

def save_info(info):
    with open(path, 'a') as f:
        f.write(info+'\n')

def column_name():
    return "# Block Height || Transactions || Contract Transactions || Size #"

def GetInfo(url):
    timestampFrom = "From: "+parse_timestamp(url+str(blocknum+offset))+'\n'
    timestampTo = "To: "+parse_timestamp(url+str(blocknum+count))+'\n'
    with open(path, 'w') as f:
        f.write(timestampFrom+timestampTo)
    save_info(column_name())
    indeed_count = count - offset
    for i in range(indeed_count):
        info = parse_per_page(url+str(blocknum+offset+i))
        if not info:
            ok = False
            for j in range(3):
                info = parse_per_page(url+str(blocknum+offset+i))
                if not info:
                    if j == 2:
                        with open(log, 'a') as f:
                            f.write(time.asctime(time.localtime(time.time()))+" ## "+url+str(blocknum+offset+i)+'\n')
                    continue
                else:
                    print("Reconnect to "+url+str(blocknum+offset+i))
                    ok = True
                    break
            if not ok:
                continue
        save_info(" ".join(info))
        if i % 10 == 0:
            print("Percentage: %.2f"%(i*100.0/indeed_count)+"%")
            time.sleep(1)
    print("Finished. Total: "+str(indeed_count))
    #info = parse_per_page("https://etherscan.io/block/7257053", True)
    #print(info)
    #save_info(info)

def GetSingleInfo(url, block_list):
    for block in block_list:
        info = parse_per_page(url+str(block))
        if not info:
            continue
        save_info(" ".join(info))
    print("Finished. Total: "+str(len(block_list)))


if __name__ == '__main__':
    GetInfo(url)
    #GetSingleInfo(url, block_list)
