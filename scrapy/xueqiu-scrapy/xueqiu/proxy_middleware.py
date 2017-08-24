#!/usr/bin/env python

import base64
from scrapy import log
import proxy_pool

class CustomProxyMiddleware(object):
    
    def __init__(self):
        pass
#     
#     @classmethod
#     def from_crawler(cls,crawler):
#         return cls(crawler.settings)
    
    def process_request(self,request,spider):
#         if 'proxy' in request.meta:
#             return
        proxy_user_pass = ''
        random_proxy = proxy_pool
#         request.meta['proxy'] = random_proxy
#         print random_proxy
#         print repr(request)
#         
#         if proxy_user_pass:
#             basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
#             request.headers['Proxy-Authorization'] = basic_auth
    
    
    def process_exception(self,request,exception,spider):
        proxy = request.meta.get('proxy')
        log.msg('Removing failed proxy <%s>, %d proxies left' % (
                    proxy, len(self.proxies)))
#         try:
#             proxy_pool.proxies.remove(proxy)
#         except ValueError:
#             pass
        
#         return request  
        
if __name__=='__main__':
    proxy = CustomProxyMiddleware()
    proxy.get_proxy()
    print len(proxy.proxies)
    proxy.proxies.remove('http://121.52.229.156:8088')
    print len(proxy.proxies)
        
        