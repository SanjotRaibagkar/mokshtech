#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 23:53:31 2018

@author: sanjotraibagkar
"""

from optionvaluecalculation.optionvalueprop import tb_DerivativeData
import matplotlib as mpl
mpl.use('TkAgg')
from optionvaluecalculation.OptionChain.Implied_Volatility import ImpliedVolatility
from utility import getstart as gs, filterframe
from utility.dbutilities.dbqueries import *
import property as p

import requests as req
from datetime import date, datetime
from calendar import monthrange
import os
import pandas as pd
# import numpy as np
import nsepy
# from bs4 import BeautifulSoup
from io import StringIO, BytesIO


def createCSVFileFromBhavCopy(symbol):
    
    m = range(1,13)
    banknifty = pd.DataFrame()
    for i in m:
        if i>2 : # temp as 2nd month file have some issue
            filename=str("prices_")+str('2018')+"_"+str(i)+".csv"
            fname = os.path.join(p.optiondata,filename)
            fname_day = os.path.join(p.optiondata_day,filename)
            df = pd.read_csv(fname, index_col ='Date')
            df = df.drop(['Unnamed: 15','Unnamed: 0'],1)     
            df = df.loc[df['SYMBOL']== symbol]
            banknifty= banknifty.append(df)
            print("r",fname)
            print(banknifty.head())
            
    
    print(banknifty.shape)
    #os.path.join(p.optiondata,filename)
    banknifty.to_csv(p.optiondata+'/'+symbol+'2018.csv', header=True)

if __name__ == '__main__':
    #createCSVFileFromBhavCopy('BANKNIFTY')