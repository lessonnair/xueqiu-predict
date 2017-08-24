#!/usr/bin/env python

from scrapy import log
from cookie_pool import CookiePool
import re
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class CustomCookieMiddleware(object):
       
    
    def __init__(self):
        self.pool = CookiePool()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        pass

    
    def process_request(self, request, spider):
        
        if re.search('http://weixin.sogou.com/weixin\?.*type\=2.*',request.url):
            cookie_dict = self.pool.get_random_cookie()
            if cookie_dict:
                request.cookies = cookie_dict    
            else:
                cookie_dict = self.pool.get_random_cookie()
                request.cookies = cookie_dict
    
    def process_exception(self,request,exception,spider):
        cookie = request.cookies
        if cookie:
            self.pool.remove_cookie(cookie)
    
    
    def spider_closed(self):
        if self.pool:
            self.pool.spider_closed()
        
#         return request  
        
if __name__=='__main__':
    pass
        
        