#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 12, 2014

@author: seny
'''
import urllib, urllib2, cookielib
import datetime
import time
import string
import sys
import threading
class LQJX:
    # like browser
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'}
    cookie = None  # cookie obj
    cookiefile = './cookies.dat'  # cookie file

    def __init__(self):
        self.cookie = cookielib.LWPCookieJar()  # save cookies obj
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)

    def login(self, username , password):
        postdata = {
            '__VIEWSTATE':'/wEPDwUKMTg0NDI4MDE5OGRk5fUBYNDgEyCFMqLG67nHjWu4h3Y=',
            'txtUserName':username,
            'txtPassword':password,
            'BtnLogin':'登  录',
            'rcode':''
            }
        postdata = urllib.urlencode(postdata)
        req = urllib2.Request(
                url='http://106.37.230.254:81/login.aspx',
                data=postdata,
                headers=self.header
            )
        result = urllib2.urlopen(req).read()
        result = str(result)

        self.cookie.save(self.cookiefile)
        if 'zhxx.aspx' in result:
            print "Login successful!"
            flag = True
        elif '重复登录' in result:
            print '对不起，您已在其它地方进行登录，不能多次重复登录!'
            flag = False
        else:
            print "Login failed!"
            flag = False
        return flag
    #Logout
    def logout(self):
        req = urllib2.Request(
                url='http://106.37.230.254:81/Login.aspx?LoginOut=true',
                headers=self.header
        )
        urllib2.urlopen(req).read()
        print 'Logout!!!'

    # send order request which data
    def orderCar(self, jlcbh, xnsd):
        base_url = "http://106.37.230.254:81/Tools/km2.aspx?"
        query_param = {
               'jlcbh': jlcbh,  #  教练场编号
                'yyrqbegin': str(datetime.date.today() + datetime.timedelta(13)).replace('-', ''),  #  预约时间
                'xnsd': xnsd,  #  时段 -1  812  15  58
                'trainType': '3',  #  原地1 道路3 实际4
                'type': "km2Car2" ,  #  约车类型 科目二km2Car
                '_':int(time.time())  # 时间戳
                }
        query_param = urllib.urlencode(query_param)
        uid_url = urllib2.Request(
                url=(base_url + query_param),
                headers=self.header
            )
        auth = urllib2.urlopen(uid_url).read()
        result = str(auth)
        return result

    def run(self, jlcbh, xnsd):
        while 1:
            result = self.orderCar(jlcbh, xnsd)
            if '成功' in result:
                print 'OK!!!!!OK!!!!!OK!!!!!OK!!!!!OK!!!!!'
                print datetime.datetime.now()
                break
            elif '该时间' in result :
                print 'Has not started!'
            elif '最多' in result :
                print 'Have an order!'
                break
            elif '请核对' in result :
                print 'Game Over!!!!!!!!'
                break
            else:
                print jlcbh , result
                jlcbh = str(string.atol(jlcbh) + 1)
            time.sleep(2) 
#****************************************************************************
print datetime.datetime.now()
arg = None
if len(sys.argv) > 1:
    arg = sys.argv[1]
elif arg == None:
    arg = raw_input("username,password,jlcbh,xnsd(812,15,58)\n")
inputdata = arg.split(",")
orderdata = {
  'username':inputdata[0],
  'password':inputdata[1],
  'jlcbh':inputdata[2],
  'xnsd':inputdata[3]
  }
login = LQJX()
try:
    flag = login.login(orderdata['username'], orderdata['password'])
    if flag:
        login.run(orderdata['jlcbh'], orderdata['xnsd'])
    login.logout()
except KeyboardInterrupt, e:
    login.logout()

