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








PRICE_LIST_URL = 'http://www.nseindia.com/content/historical/DERIVATIVES/%s/%s/fo%sbhav.csv.zip'

DERIVATIVE_ARCHIVES = 'http://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?instrumentType=OPTIDX&symbol=NIFTY&expiryDate=27-07-2006&optionType=CE&strikePrice=&dateRange=week&fromDate=&toDate=&segmentLink=9&symbolCount='

def __raw_zip_data_to_str(data):
    fp = BytesIO(data)
    import zipfile
    zipfile = zipfile.ZipFile(fp)
    name = zipfile.filelist[0].filename
    return zipfile.read(name)


def date_to_str(d, style='dd-mm-yyyy'):
    if style == 'dd-mm-yyyy':
        return str(d.day).zfill(2) + '-' + str(d.month).zfill(2) + '-' + str(d.year).zfill(2)
    elif style == 'ddMMMyyyy':
        import calendar
        lookup = dict((k, v) for k, v in enumerate(calendar.month_abbr))
        return str(d.day).zfill(2) + lookup[d.month] + str(d.year)

def get_price_list(dt, proxies={}):
    dt_str = date_to_str(dt, style='ddMMMyyyy')
    #dt_str = '13Jul2018'
    yy = dt_str[5:9]
    mm = dt_str[2:5].upper()
    url = PRICE_LIST_URL % (yy, mm, dt_str.upper())
    resp = req.get(url=url, proxies=proxies)
    try:
        df = pd.read_csv(StringIO(str(__raw_zip_data_to_str(resp.content), 'utf-8')))
        df = df.rename(columns={"TIMESTAMP": "Date"})
        return df
    except Exception as e:
        print("nseoptions error 1 ",e)

def get_tradingDay(start,end):
    if end < start :
        print('start {0} is greater than end {1}'.format(start,end))
        pass
    else:
        return pd.Series(pd.DataFrame(nsepy.get_history(symbol='NIFTY',
                    start=start,
                    end=end,
                    index=True)).index)

def save_data(dbq,con,DF,table,file,tempfile):
    DF.to_csv(file,mode='a')
    try:
        DF.to_csv(tempfile, header=True)
        con = convert(tempfile, dbpath=dbp.sqlmokshtechdb, table=table, conn=con)
    except Exception as e:
        print("nseoptionachain 5 ", e)
    finally:
        con.commit()
        return con

def get_year_data(year,Flag=False,Start = date(2018,1,1)):
    """
    :param year: year of Data
    :param Flag: if True then append data and skip downloading complete Data
    :param start: if Flag is true, then start date of data
    :return: None. It directly writes data to csv
    """
    now = datetime.now()
    if Flag :
        m = range(now.month,now.month+1)
    else:
        m = range(1,13)
    for i in m:
        if Flag:
            start = str(Start)
            start = date(int(start[0:4]),int(start[5:7]),int(start[8:10]))
        else:
            start = date(year, i, 1)
        if year < now.year:
            end = date(year, i, monthrange(year, i)[1])
        elif (year == now.year and i <= now.month):
            end = date(year, i, monthrange(year, i)[1])
        else:
            break
        print(start,end)
        try:
            tradingDay=get_tradingDay(start,end)
        except Exception as e:
            print("nseoptions error 2 ", e)
        filename=str("prices_")+str(year)+"_"+str(i)+".csv"
        fname = os.path.join(p.optiondata,filename)
        fname_day = os.path.join(p.optiondata_day,filename)
        #price=[]
        # if Flag and os.path.isfile(fname):
        #     old_prices = pd.read_csv(fname)
        #     old_prices.rename(columns={"TIMESTAMP": "Date"})
        #     price.append(old_prices)
        def concat_Data(x,dbq,con):
            print(x)
            price_df = get_price_list(dt=x)
            if not price_df.empty:
                price_df = filterframe.filtered_frame(price_df, Options=True)
                save_data(dbq, con, price_df, tb_DerivativeData, fname, fname_day)
                implobj = ImpliedVolatility(Dframe=price_df, DfFlag=True, dbq=dbq, conn=con)
                implobj.getStrike()
            else:
                print("no data to recieve for ",x)
        try:
            dbq = db_queries()
            con = dbq.create_connection()
            tradingDay.apply(concat_Data,args=(dbq,con,))
        except Exception as e:
            print("nseoptionchain 4 ", e)
        finally:
            dbq.close_conn(conn=con)



### code to append data

def appendData():
    now = datetime.now()
    for d,s,files in os.walk(p.optiondata_day):
        for f in files:
            fnme = os.path.join(p.optiondata_day,f)
            if fnme.startswith("prices_"):
                os.remove(fnme)
    # name = str("prices_") + str(now.year) + "_" + str(now.month) + ".csv"
    # monthFile=os.path.join(p.optiondata,name)
    # filefound = 0
    # while(filefound == 0):
    #     if os.path.isfile(monthFile):
    #         filefound = 1
    #     else:
    #         name = str("prices_") + str(now.year) + "_" + str(now.month-1) + ".csv"
    #         monthFile = os.path.join(p.optiondata, name)
    #         print(monthFile)
    #
    # if filefound:
    #     startdate=datetime.strptime(gs.get_startdate(monthFile,Options=True),"%d-%b-%y") # date from where we need to download
    #     datediff = ((date.today()-startdate.date()).seconds)//60
    #     if datediff == 0: # for days the above statement will give zero so calculate once more
    #         datediff = ((date.today()-startdate.date()).days)*24*60*60
    #     if datediff == 0:
    #         print('updated data present')
    #     elif 1 < datediff < 1440 :
    #         pass                # Place holder for 5 mins and 1 min data download code.
    #     else:
    #         print('downloading delta data')
    #         startdate = (startdate.year,startdate.day,startdate.month)

    latestdate = getlatestDerivative()

    if latestdate !=0 :latestdate=datetime.strptime(latestdate,"%d-%b-%Y")  # date from where we need to download

    get_year_data(now.year,True,latestdate)


years_series=pd.Series([2018])
if __name__ == '__main__':
    #years_series.apply(get_year_data)
    appendData()


