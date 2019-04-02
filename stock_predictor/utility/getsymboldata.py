# coding: utf-8

# '''This is only for the development purpose. Idea is to fetch data via frontend code and dump in csv.
#     till the time that code is ready we will use this. Once frontend gets ready we will retire c

import nsepy
import datetime
from datetime import date
import property as p
from utility import getstart as gs
from utility import downloaddata as dw
from property import *
from utility.dbutilities.dbqueries import getlatestStockDate
from utility.parrallelize import parallelize
from nsepy.history import get_price_list


def getsymboldata(flag,symbol,begining=False):
    print(symbol)
    '''This is only for the development purpose. Idea is to fetch data via frontend code and dump in csv.
    till the time that code is ready we will use this. Once frontend gets ready we will retire code'''
    symbfile = os.path.join(stockdata,symbol+'.csv')
    startdate = gs.get_startdate(symbfile,symbol,flag) # date from where we need to download

    if begining: startdate = None
    if startdate is None:
        startdate = date(p.y,p.m,p.d)
        print('startdate', startdate)

    datediff = ((date.today()-startdate).seconds)//60

    if datediff == 0: # for days the above statement will give zero so calculate once more
        datediff = ((date.today()-startdate).days)*24*60*60

    if datediff == 0:
        print('updated data present')
    #elif 1 < datediff < 1440 :
     #   pass                # Place holder for 5 mins and 1 min data download code.
    else:
        print('downloading delta data')
        dw.down_data(symbfile,symbol,flag,startdate=startdate,headerflag=True)


def run_getsymboldata(begining=False):
    try:
       # pd.DataFrame(getlatestStockDate(), columns=['SYMBOLS', 'Date']).to_csv('temp_symboldates.csv')

        # ind = lambda lst: getsymboldata(True, lst)
        def ind(x):
            getsymboldata(True,x,begining=begining)
        pd.Series(indlist).apply(ind)
        #list(map(ind, indlist))
        #nonind = lambda lst: getsymboldata(False, lst)
        def nonind(x):
            getsymboldata(False,x,begining=begining)
        nonindlist.apply(nonind)
        #parallelize_dataframe(2, nonindlist, nonind)

    except Exception as e:
        print('run_getsymboldata',e)
        import traceback
        print(traceback.extract_stack())
        
#def getBhavCopyData(dt):
#    print(dt)
#    #dt=date(2015,1,1)
#    prices = get_price_list(dt=dt)
#    prices['Date'] = dt
#    delsymfilepath = os.path.join(stockdatadelta,dt.strftime('%m_%d_%Y'))
#    print(delsymfilepath)
#    prices.to_csv(delsymfilepath+'.csv', header=True,index='Date')
#    
##    if os.path.exists(file):
##        prices.to_csv(file, mode='a',index='Date',header=False)
##    else:
##        prices.to_csv(file, mode='a',index='Date',header=True)
##    print('data saved')



if __name__ == '__main__':
#    daterang = pd.date_range(start='1/1/2011', end='1/04/2019')
#    print(daterang.date)
#    pd.Series(daterang.date).apply(getBhavCopyData)
    run_getsymboldata()