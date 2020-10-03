# -*- coding: utf-8 -*-
#! py -2
import sqlite3 as sq
# 未完成

# search it on your pc
dbfile = u'E:\各种应用软件\Thunder\Profiles\TaskDb.dat'

cx=sq.connect(dbfile)
cu=cx.cursor() 
print ">>>>>>>>>>>>>>>>>>>>>>>finish connecting >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
cu.execute("SELECT * FROM AccelerateTaskMap11014832_superspeed_1_1 ")
f=cu.fetchall()
count=0
print f
if f!=[]:
    for i in f:
        count+=1
        print i
        print '*****************************'
else:
    print 'nothing'
    exit()
for n in range(count):
    buff=f[n][3]
    f1=long(f[n][0])
    f2=f[n][1]
    f3=f[n][2]
    print buff
    lis=str(buff).split(',')
    print lis
    if lis[-2]=='"Result":0':
        continue
    else:
        lis[-2]='"Result":0'
        print lis
    st=','
    st=st.join(lis)
    print st
    buff=buffer(st)
    cu.execute("delete from AccelerateTaskMap11014832_superspeed_1_1 where LocalTaskId=?",(f1,))
    cu.execute("insert into AccelerateTaskMap11014832_superspeed_1_1 values(?,?,?,?)",(f1,f2,f3,buff))
cx.commit()
cx.close()
print 'ok\a'
raw_input('Enter to exit')
