

import numpy as np
import talib as ta

close =  np.random.random(100)


output = ta.SMA(close)

from talib import MA_Type

upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)


output = talib.MOM(close, timeperiod=5)


import pandas_datareader.data as web
import datetime
import talib as ta

start = datetime.datetime.strptime('12/1/2015', '%m/%d/%Y')
end = datetime.datetime.strptime('2/20/2016', '%m/%d/%Y')
f = web.DataReader('GOOG', 'yahoo', start, end)
print ('Closing Prices')
print (f['Close'].describe())
print (f.Close)
print (ta.RSI(np.array(f.Close),2))


print (ta.SMA(np.array(f.Close),2))
print (ta.SMA(np.array(f.Volume),4))


