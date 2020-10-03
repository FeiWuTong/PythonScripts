#! python2

import os

driver = 'driver.txt'

if os.path.exists(driver):
    links = []
    with open(driver, 'r') as f:
        for line in f.readlines():
            links.append("magnet:?xt=urn:btih:"+line)
    with open(driver, 'w') as f:
        f.writelines(links)
    os.startfile(driver)

'''
links = ""
while True:
    code = input("Empty Line With 'Enter' Stop:")
    if not code:
        break
    links += "magnet:?xt=urn:btih:" + code + "\n"

print(links)
'''
