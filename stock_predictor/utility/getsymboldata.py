
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


def getsymboldata(flag,symbol,begining=False):
    print(symbol)
    '''This is only for the development purpose. Idea is to fetch data via frontend code and dump in csv.
    till the time that code is ready we will use this. Once frontend gets ready we will retire code'''
    symbfile=os.path.join(stockdata,symbol+'.csv')
    startdate=gs.get_startdate(symbfile,symbol,flag) # date from where we need to download
    print('startdate',startdate)
    datediff = ((date.today()-startdate).seconds)//60
    if datediff == 0: # for days the above statement will give zero so calculate once more
        datediff = ((date.today()-startdate).days)*24*60*60
    if datediff == 0:
        print('updated data present')
    elif 1 < datediff < 1440 :
        pass                # Place holder for 5 mins and 1 min data download code.
    else:
        print('downloading delta data')
        dw.down_data(symbfile,symbol,flag,startdate=startdate,headerflag=False)


def run_getsymboldata(begining=False):
    for d,s,files in os.walk(stockdatadelta):
        for f in files:
            fnme = os.path.join(stockdatadelta,f)
            if not fnme.startswith("symbolList.csv"):
                os.remove(fnme)
    try:
        if begining:
            remnonin = lambda lst: getsymboldata(False, lst,begining)
            list(map(remnonin, remnonind))
        else:
            ind = lambda lst: getsymboldata(True, lst)
            list(map(ind, indlist))
            nonind = lambda lst: getsymboldata(False, lst)
            list(map(nonind, nonindlist))


    except Exception as e:
        print(e)



if __name__ == '__main__':
    run_getsymboldata(begining=True)