#!/usr/bin/env python
#encoding:utf-8

import random
import urllib
import json
import config

class ProxyPool(object):
    
    def __init__(self,url=config.PROXY_GET_URL,update_url=config.PROXY_UPDATE_URL):
        self.pool = []
        self.proxy_max_counts = 20
        self.url = url
        self.update_url = update_url
        self.get_proxies_by_url()
        print 'proxy init pool size:' + str(len(self.pool))
    

    def get_proxies_by_url(self):
        resp = urllib.urlopen(self.url)
        json_string = resp.read()
        proxy_list = json.loads(json_string) 
        if proxy_list:
            for proxy_json in proxy_list:
                ip = proxy_json['ip']
                port = proxy_json['port']
                self.pool.append('http://'+str(ip)+':'+str(port))
                
    
    def update_proxies_by_url(self):
        urllib.urlopen(self.update_url)
 

    def get_random_proxy(self):
        proxy = ''

        if len(self.pool) < self.proxy_max_counts/2:
            self.get_proxies_by_url()
        
        if len(self.pool) < self.proxy_max_counts/5:
            self.update_proxies_by_url()
        
        if len(self.pool) > 1:
            proxy = random.choice(self.pool)
        
        return proxy



    def remove_proxy(self,proxy):
        if self.pool:
            try:
                self.pool.remove(proxy)
            except:
                pass
        
        
# def check_proxy(ip,port,testurl='http://weixin.sogou.com/weixin?type=2&query=x',checkstr='http://www.sogou.com/complain/antispider',timeout = 30):
#     is_connected = False
#     proxy = ip  + ':' + str(port)
#     proxies = {'http':'http://'+proxy+'/'}
#     import socket
#     socket.setdefaulttimeout(timeout)
#     opener = urllib.FancyURLopener(proxies)
#     opener.addheaders = [
#         ('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
#         ]
#     t1 = time.time()
#     
#     try:
#         f = opener.open(testurl)
#         s = f.read()
# #         print s
#         match = re.findall(checkstr, s)
#     except:
#         match = True
#         pass
#     t2 = time.time()
#     timeused = t2-t1
#     if (timeused < timeout and not match):
#         is_connected = True
#     
#     return is_connected

