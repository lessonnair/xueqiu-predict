#!/usr/bin/python 
#encoding: utf-8

# from proxy import PROXIES
from agents import AGENTS

import random

class CustomUserAgentMiddleware(object):
    
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent        
