import os
import datetime
from datetime import date
import property as p
from utility import downloaddata as dw

y,m,n=p.y,p.m,p.d
start=date(y,m,n)
stockfoldpath=p.stockdata


def get_startdate(symbfile,symbol='NIFTY',flag=True):
    print('searching file at',symbfile)
    if os.path.isfile(symbfile):
        print(symbfile,' found')
        with open(symbfile) as f:
                a=f.readlines()
                if len(a)<2:
                    print(symbfile, 'file is empty')
                    d=start
                else:
                    y,m,n=(a[-1].strip().split(",")[0]).split("-")
                    d=date(int(y),int(m),int(n)+1)
                    d=d+datetime.timedelta(days=1)

        return(d)
    else:
        print(symbfile,' file does not exist')
        print('creating file and downloading data')
        d = start
        dw.down_data(symbfile,symbol,flag,headerflag=True)
        return(date.today())


