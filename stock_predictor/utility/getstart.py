import os
import datetime
from datetime import date
import property as p
from utility import downloaddata as dw
from utility import getDataunit as du
import format_data as fd


y,m,n=p.y,p.m,p.d
start=date(y,m,n)
stockfoldpath=p.stockdata

def get_date(symbfile):
    with open(symbfile) as f:
        a = f.readlines()
        if len(a) < 2:
            print(symbfile, 'file is empty')
            d = start
        elif du.get_dataunit(symbfile) >= 1440:
            y, m, n = (a[-1].strip().split(",")[0]).split("-")
            d = date(int(y), int(m), int(n))
            d = d + datetime.timedelta(
                minutes=du.get_dataunit(symbfile))  # append time diff of two datapointsto get next start date
        else:
            d = start
    return d

def get_startdate(symbfile,symbol='NIFTY',flag=True):
    '''

    :param symbfile:
    :param symbol:
    :param flag:
    :return: 1. If file exist than last date in file
             2. Else date from where we need to download
    '''
    if os.path.isfile(symbfile):
        d=get_date(symbfile)
        return(d)
    else:
        fd.format_data()
        if os.path.isfile(symbfile):
            d = get_date(symbfile)
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

