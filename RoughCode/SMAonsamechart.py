#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 17:14:08 2018

@author: sanjotraibagkar
"""

import pandas_datareader as web

import datetime
import talib
import numpy

#Download data from yahoo finance
start = datetime.datetime(2010,1,1)
end = datetime.datetime(2014,3,24)
ticker = "AAPL"
f=web.DataReader(ticker,'yahoo',start,end)

f['SMA_20'] = talib.SMA(numpy.asarray(f['Close']), 20)
f['SMA_50'] = talib.SMA(numpy.asarray(f['Close']), 50) 
f['RSI'] =talib.RSI(numpy.asarray(f['Close']), 14)
f.plot(y= ['Close','SMA_20','SMA_50'], title='AAPL Close & Moving Averages')