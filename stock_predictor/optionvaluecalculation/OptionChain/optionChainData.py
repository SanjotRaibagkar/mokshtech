
try:
    import requests as req
    from datetime import date, datetime, timedelta
    from calendar import monthrange
    import os
    from utility import getstart as gs, filterframe
    #from utility.dbutilities import dbqueries as dbq
    import property as p
    import numpy as np
    import pandas as pd
    import zipfile
    import nsepy
    from bs4 import BeautifulSoup
    from io import StringIO, BytesIO

except Exception as e:
        print(e)



#PRICE_LIST_URL = 'http://www.nseindia.com/content/historical/EQUITIES/%s/%s/fo%sbhav.csv.zip'
PRICE_LIST_URL = 'http://www.nseindia.com/content/historical/DERIVATIVES/%s/%s/fo%sbhav.csv.zip'

DERIVATIVE_ARCHIVES = 'http://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?instrumentType=OPTIDX&symbol=NIFTY&expiryDate=27-07-2006&optionType=CE&strikePrice=&dateRange=week&fromDate=&toDate=&segmentLink=9&symbolCount='

def __raw_zip_data_to_str(data):
    fp = BytesIO(data)
    print(type(fp))
    import zipfile
    zipfile = zipfile.ZipFile(fp)
    name = zipfile.filelist[0].filename
    return zipfile.read(name)



# raise error, file is truncated

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
    print(url)
    resp = req.get(url=url, proxies=proxies)
    df = pd.read_csv(StringIO(str(__raw_zip_data_to_str(resp.content), 'utf-8')))
    return df

def get_tradingDay(startdate,enddate,tradingFlag=True):
    if type(startdate) == type('str'):
        start = datetime.strptime(startdate,"%d-%b-%Y") # date from where we need to download
    if type(enddate) == type('end'):
        end = datetime.strptime(enddate,"%d-%b-%Y") # date from where we need to download
    else:
        start, end = startdate, enddate
    if tradingFlag:

        print(start,end)
        return pd.Series(pd.DataFrame(nsepy.get_history(symbol='NIFTY',
                start=start,
                end=end,
                index=True)).index)
    else:
        diff_count =  end-start
        return diff_count.days

def get_year_data(year,Flag=False,Start = date(2018,1,1)):
    """
    :param year: year of Data
    :param Flag: if True then append data and skip downloading complete Data
    :param start: if Flag is true, then start date of data
    :return: None. It directly writes data to csv
    """
    now = datetime.now()
    if Flag :
        m = range(Start[2],now.month+1)
        start = date(Start[0], Start[2], Start[1])
    else:
        m = range(1,13)
    for i in m:
        if Flag == False:
            start = date(year, i, 1)
        if year < now.year:
            end = date(year, i, monthrange(year, i)[1])
        elif (year == now.year and i <= now.month):
            end = date(year, i, monthrange(year, i)[1])
        if start == end :
            start += timedelta(days=1)
            continue
        tradingDay=get_tradingDay(start,end)
        print(tradingDay)
        fname=str("prices_")+str(year)+"_"+str(i)+".csv"
        fname = os.path.join(p.optiondata,fname)
        price=[]
        if Flag and os.path.isfile(fname):
            old_prices = pd.read_csv(fname)
            old_prices = filterframe.filtered_frame(old_prices,Options=True)
            price.append(old_prices)
        def concat_Data(x):
            print(x)
            price.append(filterframe.filtered_frame(get_price_list(dt=x),Options=True))
        try:
            tradingDay.apply(concat_Data)
        except Exception as e:
            print(e.with_traceback())
        finally:
            prices = pd.concat(price)
            prices = filterframe.filtered_frame(prices,Options=True)
            prices.to_csv(fname)

years_series=pd.Series([2015])


### code to append data

def appendData():
    now = datetime.now()
    monthFile = get_OptionFile(cuurent=False)
    try:
        startdate = datetime.strptime(gs.get_startdate(monthFile,Options=True),"%d-%b-%y") # date from where we need to download
    except ValueError as e:
        startdate = datetime.strptime(gs.get_startdate(monthFile,Options=True),"%d-%b-%Y"
                                      ) # date from where we need to download
    datediff = ((date.today()-startdate.date()).seconds)//60
    if datediff == 0: # for days the above statement will give zero so calculate once more
        datediff = ((date.today()-startdate.date()).days)*24*60*60
    if datediff == 0:
        print('updated data present')
    elif 1 < datediff < 1440 :
        pass                # Place holder for 5 mins and 1 min data download code.
    else:
        print('downloading delta data')
        startdate = (startdate.year,startdate.day,startdate.month)
        get_year_data(now.year,True,startdate)


def get_OptionFile(cuurent=False):
    """

    :param flag: If Flag is true , it will return current month file name else
    :return: it will return latet available file.
    """
    now = datetime.now()
    name = str("prices_") + str(now.year) + "_" + str(now.month) + ".csv"
    monthFile = os.path.join(p.optiondata, name)
    expected_monthfile = os.path.join(p.optiondata, name)
    filefound = 0
    month = now.month
    while (filefound == 0):
        if os.path.isfile(monthFile):
            filefound = 1
        else:
            month-=1
            name = str("prices_") + str(now.year) + "_" + str(month) + ".csv"
            monthFile = os.path.join(p.optiondata, name)
    return monthFile

if __name__ == '__main__':
    #years_series.apply(get_year_data)
    appendData()


# 18-JUL-2018,NIFTY,26-Jul-2018,10978.6,11000.0,10900.0,32.55462646484375,34.60693359375,35.125732421875,38.543701171875
# import mibian
# CE_H_I = mibian.Me([10986.10, 11000, 7, 0, 8], callPrice=67).impliedVolatility
# print(CE_H_I)
