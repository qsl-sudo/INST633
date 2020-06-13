#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import http.cookiejar
import re
import urllib.request
from urllib import request
import urllib.parse
import zlib
import pypinyin #pip install pypinyin #lib for translating chinese unicode character to alphabet pinyin 

#config
username = 'your username here'
pwd = 'your password here'
nodefilepath = '/path/to/your/nodes.csv'
edgefilepath = '/path/to/your/edges.csv'

 
def login():
    logpage = 'http://www.renren.com/ajaxLogin/login'
    data = {'email': username, 'password': pwd}
    login_data = urllib.parse.urlencode(data).encode('utf-8')
    cookie = http.cookiejar.CookieJar()   
    handler = urllib.request.HTTPCookieProcessor(cookie)  
    opener = urllib.request.build_opener(handler)  
    request.install_opener(opener)
    res = opener.open(logpage, login_data)
    print("Login now ...")
    html = res.read()
    html = html.decode('utf-8', 'ignore')
    print (html)
    print("Login successfully")


def getfriends():
    global dict1
    dict1 = {}
    url = 'http://friend.renren.com/groupsdata'
    req = urllib.request.Request(url, headers={
        'Host': 'friend.renren.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': 'http://friend.renren.com/managefriends',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'RA-Ver': '3.0.7',
        'RA-Sid': '655102BF-20150723-085431-c809af-3fa054',
    })
    oper = urllib.request.urlopen(req)
    html = oper.read()
    html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
    html = html.decode('utf-8', 'ignore')
    print (html)
    html = html.replace('\n','')
    fid = re.findall(r'"fid":(\d{4,11})', html)
    fname = re.findall(r'"fname":"(.{5,80})","info',html)
    for i in range(0, len(fid)):
        id = fid[i]
        try:
            name = fname[i]
            name = name.encode('utf-8').decode('unicode-escape')
        except:
            print ("friends list completed")
            break
        else:
            print(id, name)
            dict1[id] = name
    with open(nodefilepath, 'wt',encoding='UTF-8') as f:
        f.write('id,name,namepinyin\n')
        for i in dict1:
            f.write(i+','+dict1[i]+','+pypinyin.slug(dict1[i], separator='')+'\n')
            #print(dict1, file=f)
    return dict1

def getmutualfriends(friendid):
    url = 'http://friend.renren.com/shareFriends?p={%22init%22:true,%22uid%22:true,%22uhead%22:false,%22uname%22:false,%22group%22:false,%22net%22:false,%22param%22:{%22guest%22:'+friendid+'}}&requestToken=1464136450&_rtk=2305f15c'
    req = urllib.request.Request(url, headers={
        'Host': 'friend.renren.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': 'http://www.renren.com/'+friendid+'/profile',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'RA-Ver': '3.0.7',
        'RA-Sid': '655102BF-20150723-085431-c809af-3fa054',
    })
    oper = urllib.request.urlopen(req)
    html = oper.read()
    html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
    html = html.decode('utf-8', 'ignore')
    fid = re.findall(r'"id":(\d{4,11})', html)
    with open(edgefilepath, 'a',encoding='UTF-8') as f:
        for i in fid:
            f.write(friendid+','+i+'\n')
    print('shareFriends with '+friendid+':'+str(len(fid)))
    return fid

login()
getfriends()
c = 0
with open(edgefilepath, 'a',encoding='UTF-8') as f:
        f.write('source,target\n')
for friendid in dict1:
    c = c+1
    print(str(c)+' of '+str(len(dict1)))
    getmutualfriends(friendid) 
print('All done.')
      
 







