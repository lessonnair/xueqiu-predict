# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import re
import hashlib
import requests


class XqSpider(scrapy.Spider):
    name = 'xq'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/']
    index_url = "https://xueqiu.com/"
    login_url = "https://xueqiu.com/snowman/login"
    check_login_url = "https://xueqiu.com/setting/user"
    download_url = "https://query1.finance.yahoo.com/v7/finance/download/JMEI?period1=1500741608&period2=1503420008&interval=1d&events=history&crumb=B5vTl/WUDG4"
    custom_settings = {
        "COOKIES_ENABLED": True
    }

    login_formdata = {
        "remember_me": "true",
        "username": "18500256134",
        "password": "545300ceshi"
    }

    headers = {
        "Host": "xueqiu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
    }
    # 密码的 md5 加密

    def start_requests(self):
        print('start_requests')
        yield Request(self.index_url, headers=self.headers, callback=self.login)

    def login(self, response):
        print('post_login')
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        self.headers["X-Requested-With"] = "XMLHttpRequest"
        self.headers["Referer"] = self.index_url
        return [FormRequest(
                url=self.login_url,
                formdata=self.login_formdata,
                headers=self.headers,
                callback=self.check_login_status,
                )]

    def check_login_status(self, response):
        # '用来检测是否登陆成功'
        print("----__check_login_status----")
        self.headers["X-Requested-With"] = None
        yield Request(self.check_login_url, headers=self.headers, callback=self.parse_user_detail)

    def parse_user_detail(self, response):
        print("----parse_user_detail----")
        with open('response_of_user_detil.html', 'wb') as file:
            file.write(response.body)
        pa = r'"profile":"/(.*?)","screen_name":"(.*?)"'
        res = re.findall(pa, response.text)
        if res == []:
            print("登录失败，请检查你的手机号和密码输入是否正确")
#             return False
        else:
            print('欢迎使用 xchaoinfo 写的模拟登录 \n 你的用户 id 是：%s, 你的用户名是：%s' % (str(res[0][0]),str(res[0][1])))
            yield Request(self.download_url,headers=self.headers, callback=self.parse_history_file,dont_filter=True)
#             return True

    def parse_history_file(self,response):
        print(response.body)
        with open('JMEI.csv','wb') as local_file:
            local_file.write(response.body)
            return True
        return False
    
    
    def parse(self, response):
        print("----parse----")
        pass
