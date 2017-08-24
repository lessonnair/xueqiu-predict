# -*- coding: utf-8 -*-
'''
Created on 2017年8月25日

@author: garfield
'''

from lxml import etree
import urllib2
import pandas as pd
import time

base_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid'

def fetch_data_by_date(stockid,year,jidu):
    url = '%s/%d.phtml?year=%d&jidu=%d' %(base_url,stockid,year,jidu)
    resp = urllib2.urlopen(url)
    content = resp.read()
    html = etree.HTML(content)
    dates = html.xpath('//*[@id="FundHoldSharesTable"]//tr[*]/td[1]/div/a')
    start_prices = html.xpath('//*[@id="FundHoldSharesTable"]//tr[*]/td[2]/div/text()')
    max_prices = html.xpath('//*[@id="FundHoldSharesTable"]//tr[*]/td[3]/div/text()')
    close_prices = html.xpath('//*[@id="FundHoldSharesTable"]//tr[*]/td[4]/div/text()')
    low_prices = html.xpath('//*[@id="FundHoldSharesTable"]//tr[*]/td[5]/div/text()')
    exchange_num = html.xpath('//*[@id="FundHoldSharesTable"]//tr[*]/td[6]/div/text()')
    exchange_money = html.xpath('//*[@id="FundHoldSharesTable"]//tr[*]/td[7]/div/text()')
    dates = [s.text.strip() for s in dates]
    df = pd.DataFrame()
    df['date'] = pd.to_datetime(dates)
    df['close_price'] = pd.to_numeric(close_prices)
    df['exchange_num'] = pd.to_numeric(exchange_num)
    df['exchange_money'] = pd.to_numeric(exchange_money)
    df['stock_id'] = stockid
    return df

def fetch_data(stockid,years,jidus):
    df = pd.DataFrame()
    for y in years:
        for j in jidus:
            print "fetch %d-%d" % (y,j)
            tmp = fetch_data_by_date(stockid, y, j)
            df = pd.concat([df,tmp],axis=0)
            time.sleep(5)
    return df

if __name__=='__main__':
    siweituxin = 002405
    df = fetch_data(siweituxin, range(2010,2018), range(1,5))
    df.to_csv('./siweituxin.csv',index=False)
