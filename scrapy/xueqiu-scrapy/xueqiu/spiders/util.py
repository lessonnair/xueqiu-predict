# -*- coding: utf-8 -*-

'''
Created on 2017年8月23日

@author: garfield
'''

import time
import datetime

def datetime2unixtimestamp(date_str,date_format='%Y-%m-%d %H:%M:%S'):
    return int(time.mktime(datetime.datetime.strptime(date_str,date_format).timetuple()))

if __name__=='__main__':
    print datetime2unixtimestamp('2017-08-05 12:23:34')