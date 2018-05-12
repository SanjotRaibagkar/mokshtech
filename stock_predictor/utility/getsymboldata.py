
# coding: utf-8

# '''This is only for the development purpose. Idea is to fetch data via frontend code and dump in csv.
#     till the time that code is ready we will use this. Once frontend gets ready we will retire c
import nsepy
import datetime
from datetime import date
import property
from utility import getstart as gs
from utility import downloaddata as dw
from property import *


def getsymboldata(flag,symbol):
    '''This is only for the development purpose. Idea is to fetch data via frontend code and dump in csv.
    till the time that code is ready we will use this. Once frontend gets ready we will retire code'''
    symbfile=os.path.join(stockdata,symbol+'.csv')
    print(symbfile)
    startdate=gs.get_startdate(symbfile,symbol,flag)
    print('startdate',startdate)
    if date.today()==startdate:
        print('updated data present')
    else:
        print('downloading delta data')
        dw.down_data(symbfile,symbol,flag,startdate=startdate,headerflag=False)


def run_getsymboldata():
    try:
        ind = lambda lst: getsymboldata(True, lst)
        list(map(ind, indlist))
        nonind = lambda lst: getsymboldata(False, lst)
        list(map(nonind, nonindlist))
    except Exception as e:
        print(e)



if __name__ == '__main__':
    run_getsymboldata()