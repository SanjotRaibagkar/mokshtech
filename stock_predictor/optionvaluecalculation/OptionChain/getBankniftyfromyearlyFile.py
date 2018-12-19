#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 23:53:31 2018

@author: sanjotraibagkar
"""


import matplotlib as mpl
mpl.use('TkAgg')

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
import math


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
    
def buildandBackTestFVStatergy(filename):
    fname = os.path.join(p.optiondata,filename)
    symobleDF = pd.read_csv(fname,header=0, index_col = 'Date')
    symobldf.index = pd.to_datetime(symobldf.index)
    symobldf.EXPIRY_DT =pd.to_datetime(symobldf.EXPIRY_DT)
    #symobldf['EXPIRY_DT'][0].date()
    print(symobleDF)
    return symobleDF
    
def getStrikePrice(underlyingprice, ratio):
    strikeprice = math.floor(underlyingprice/ratio)*ratio
    return strikeprice

def function(x):
    print(getStrikePrice(x['CLOSE'][:1],100))
    

if __name__ == '__main__':
    #createCSVFileFromBhavCopy('BANKNIFTY')
    symobldf = buildandBackTestFVStatergy('BANKNIFTY2018.csv')
#    df1 = symobldf.groupby(symobldf.index).filter(
#            lambda x :function(x.loc[x['INSTRUMENT']== 'FUTIDX']))
    
#    df1 = symobldf.groupby([symobldf.index,'INSTRUMENT'])
#    for name ,values in df1.groups:
#        print(items)
#            
            
            
    
#    for name in df1.groups :
#        df2 = df1.get_group(name)
#        df = df2.loc[df2['INSTRUMENT']== 'FUTIDX']
#        print(df['EXPIRY_DT'].min())