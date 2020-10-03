# -*- coding: utf-8 -*-
import os
import time
import re
def change_name(path):
    global i
    global k
    if not os.path.isdir(path) and not os.path.isfile(path):
        print u'路径错误'
        return False
    if os.path.isfile(path):
        file_path = os.path.split(path)
        lists = file_path[1].split('.')
        file_ext = lists[-1]
        img_ext = 'bmp|jpg|gif|psd|png|jpeg'
        if file_ext in img_ext:
            a = reduce(lambda x,y:x+'.'+y, lists[:-1])
            if a not in map(str,range(1,k+1)):
                while os.path.isfile(file_path[0] + '/'+ str(k) + '.' + file_ext):
                    k += 1
                    if a in map(str,range(1,k+1)):
                        break
                os.rename(path, file_path[0] + '/'+ str(k) + '.' + file_ext)
            i += 1
    elif os.path.isdir(path):
        k = 1
        for x in os.listdir(path):
            change_name(os.path.join(path,x))

print u'输入图片文件夹路径:'
img_dir = raw_input()
img_dir = img_dir.replace('\\','/')
i = 0
k = 1
start = time.time()
change_name(img_dir)
end = time.time() - start
print u'耗时: %0.2f' % end
print u'共 %d 张' % i
raw_input()
