#!/usr/bin/env python
#encoding:utf-8

import random
import time
import re
import os
import urllib2
from agents import AGENTS
from proxy_pool import ProxyPool
import socket
import httplib
import json
import threading

pool = []
proxy_pool = []
proxy_pool = ProxyPool()
min_pool_size = 6
thread_num_max = 50

class CookiePool(object):
    
    
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__),'cookies.txt')
        self.file = open(self.path,'rb+')
        self.init_pool()
    
    
    def init_pool(self):
        global pool
        lines = self.file.readlines()
        if lines:
            for line in lines:
                threads = []
                try:
                    line = json.loads(line)
                    t = CookiePool.CookieTestThread('test',cookie=line)
                    t.setDaemon(True)
                    t.start()
                    threads.append(t)
                except Exception:
                    pass
                
                for thread in threads:
                    thread.join(60)
        print 'cookie pool size:' + str(len(pool))
        
    
    def refresh_pool(self):
        global pool,proxy_pool
        threads = []
        for i in range(0,60):
            try:
                ss = proxy_pool.get_random_proxy()
                t = CookiePool.CookieTestThread('get',proxy=ss)
                t.setDaemon(True)
                t.start()
                threads.append(t)
            except:
                pass
        for thread in threads:
            thread.join(60)
        
    @staticmethod
    def remove_cookie(cookie):
        global pool
        try:
            pool.remove(cookie)
        except:
            pass
    

    def get_random_cookie(self):
        
        global pool,min_pool_size
            
        if len(pool) < min_pool_size:
            self.refresh_pool()
        
        if len(pool) > 1:
            cookie = random.choice(pool)
            if CookiePool.test_cookie(cookie):
                return cookie
            
    @staticmethod
    def test_cookie(cookie):       
        global pool
        url = 'http://weixin.sogou.com/weixin?type=2&query=%s' % random.choice('abcdefghijklmnopqrstuvwxyz')
        req = urllib2.Request(url)
        cookie_string = 'SUV='+cookie['SUV']+';'+'SUID='+cookie['SUID']+';'+'SNUID='+cookie['SNUID']+';'+'ABTEST='+cookie['ABTEST']+';'+'black_passportid='+cookie['black_passportid']+';'+'IPLOC='+cookie['IPLOC']+';'
        req.add_header('Cookie', cookie_string)
        try:
            resp = urllib2.urlopen(req,timeout=30)
            content = resp.read()
            if content and content.find('weinxinfilter') > 0 :
                return True
            else:
                CookiePool.remove_cookie(cookie)
        except:
            CookiePool.remove_cookie(cookie)
    
    @staticmethod
    def getSUV():
        return str(int(time.time()*1000000) + random.randint(0, 1000))
    
    @staticmethod
    def find_cookie(pattern,string):
        matcher = re.findall(pattern, string)
        if matcher:
            return matcher[0]
        else:
            return ''
    
    @staticmethod
    def scrab_cookie_by_proxy(proxy = ''):
    
        if proxy:
            opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}))
            opener.addheaders = [
                ('User-agent',random.choice(AGENTS))
            ]
            urllib2.install_opener(opener)
    
        url = 'http://weixin.sogou.com/weixin?type=2&query=%s' % random.choice('abcdefghijklmnopqrstuvwxyz')
        try:
            resp = urllib2.urlopen(url,timeout=30)
        except socket.timeout:
            return None
        except urllib2.HTTPError:
            return None
        except urllib2.URLError:
            return None
        except httplib.BadStatusLine:
            return None
        except socket.error:
            return None
        except Exception:
            return None
        
        if not resp:
            return None
        
        cookies = str(resp.headers['Set-Cookie'])

        suid = CookiePool.find_cookie(r'SUID\=(.+?);',cookies)
        abtest = CookiePool.find_cookie(r'ABTEST\=(.+?);',cookies)
        snuid = CookiePool.find_cookie(r'SNUID\=(.+?);',cookies)
        iploc = CookiePool.find_cookie(r'IPLOC\=(.+?);',cookies)
        black_passportid = CookiePool.find_cookie(r'black_passportid\=(.*?);',cookies)
        suv = CookiePool.getSUV()
#         snuid = 'F8EB86DEA4A6B12E7639BFE0A413AA03'
        cookie_dict =  {'ABTEST':abtest,'SNUID':snuid,'IPLOC':iploc,'SUID':suid,'black_passportid':black_passportid,'SUV':suv}
        if snuid:
            return cookie_dict
        else:
            return None
    
    class CookieTestThread(threading.Thread):
        
        def __init__(self,action,cookie='',proxy=''):
            threading.Thread.__init__(self)
            self.action = action
            self.cookie = cookie
            self.proxy = proxy
    
        def run(self):
            global pool,proxy_pool
            if self.action == 'get':
                cookie = CookiePool.scrab_cookie_by_proxy(self.proxy)
                print 'proxy:cookie -----'+str(self.proxy)+":"+str(cookie)
                if cookie:
                    pool.append(cookie)
                else:
                    proxy_pool.remove_proxy(self.proxy)
                    
            elif self.action == 'test':
                if self.cookie and CookiePool.test_cookie(self.cookie):
                    pool.append(self.cookie)
    
    
    def spider_closed(self):
        global pool
        try:
            self.file.close()
            self.file = open(self.path,'w+')
            self.file.truncate()
            for c in pool:
                try:
                    line = json.dumps(c) + "\n"
                    self.file.write(line)
                except Exception:
                    pass
            self.file.close()
        except Exception:
            pass

if __name__=='__main__':
    
    cookie_pool = CookiePool()
    print cookie_pool.get_random_cookie()
    cookie_pool.spider_closed()
#     for proxy in proxy_pool.pool:
#         print proxy
#     
