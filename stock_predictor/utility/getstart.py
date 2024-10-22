import os
import datetime
from datetime import date
import property as p
from utility import downloaddata as dw
from utility import getDataunit as du
import format_data as fd
import pandas as pd

from utility.dbutilities.dbqueries import getlatestDerivative

y,m,n=p.y,p.m,p.d
start=date(y,m,n)
stockfoldpath=p.stockdata


def get_date(symbfile,Options):
    print("in get_Date")
    with open(symbfile) as f:
        a = f.readlines()
        try:
            a = pd.read_csv(symbfile)['Date'].dropna().unique()
            print("in get_Date1",a)
        except Exception as e:
            a = pd.read_csv(symbfile)['TIMESTAMP'].dropna().unique()
        if Options:
            d =  a[-1]
        elif len(a) < 2:
            print(symbfile, 'file is empty')
            d = start
        elif len(a)>2:
             d =  a[-1]
       # elif du.get_dataunit(symbfile,Options) >= 1440:
            #y, m, n = (a[-1].strip().split(",")[0]).split("-")
        #    y, m, n = str(a[-1]).split("-")
         #   d = date(int(y), int(m), int(n))
          #  d = d + datetime.timedelta(
           #     minutes=du.get_dataunit(symbfile,Options))  # append time diff of two datapointsto get next start date
        else:
            print("in get_Date2",start)
            d = start
    return d


def get_startdate(symbfile,symbol='NIFTY',flag=True, Options=False):
    '''

    :param symbfile: File path containing data
    :param symbol: Symbol
    :param flag: Index Flag
    :return: 1. If file exist than return date in the last row
             2. Else date from where we need to download
    '''

    print(not(os.path.isfile(symbfile)))
    if os.path.isfile('temp_symboldates.csv') and Options == False and not(os.path.isfile(symbfile)) :
        try:
            print("in get start date1")
            symboldatelist = pd.read_csv('temp_symboldates.csv')

            sdate = symboldatelist.loc[symboldatelist['SYMBOLS'] == symbol]['Date'].unique()[0]

            if p.dataunit == 1440:
                y, m, n = str(sdate).split("-")
                d = date(int(y), int(m), int(n))
                d = d + datetime.timedelta(minutes=1440)
                return d
        except Exception as e:
            print(e)
    elif os.path.isfile(symbfile):
        print("in get start date")
        return (get_date(symbfile,Options))
    else:
        print("in get start date2")
        fd.format_data()  # if the files extension are not csv convert them to csv
        if os.path.isfile(symbfile):
            d = get_date(symbfile,Options)
            return (d)
        else:

            print(symbfile, ' file does not exist')
            print('creating file and downloading data')
            d = start
            try:
                dw.down_data(symbfile, symbol, flag, headerflag=True)
            except KeyError as key:
                print('KeyError ',symbol,' not found')
            return (date.today())

