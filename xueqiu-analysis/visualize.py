# -*- coding: utf-8 -*-
'''
Created on 2017年8月24日

@author: garfield
'''

import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
import pandas as pd

df = pd.read_csv('../scrapy/xueqiu-scrapy/JMEI.csv')
init_notebook_mode(connected=True)

iplot({
    'data': [
        Scatter(x=df['Date'],
                y=df['Close'],
                mode = 'lines'),
#                 mode = 'lines+markers'),

#         Scatter(x=df['date'],
#                 y=df['close_price'],
#                 mode = 'lines')
        ],
    'layout': Layout(xaxis=XAxis(title='date'), yaxis=YAxis(title='exchange_money', type='log'))
}, show_link=True)