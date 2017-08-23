# -*- coding: utf-8 -*-
'''
Created on 2017年8月24日

@author: garfield
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fbprophet import Prophet

df = pd.read_csv('../scrapy/xueqiu-scrapy/JMEI.csv')
df['y'] = np.log(df['Close'])
df['ds'] = df['Date']
df = df.iloc[0:int(0.8*len(df))]
train_index = int(len(df) * 0.9)

train = df.iloc[0:train_index]
test = df.iloc[train_index:len(df)]

m = Prophet()
m.fit(train)
future = m.make_future_dataframe(periods=len(test))
forecast = m.predict(future)
fig,ax = m.plot(forecast);
# m.plot_components(forecast);
ax.plot(df['ds'].values,df['y'],'k.')
plt.show()



