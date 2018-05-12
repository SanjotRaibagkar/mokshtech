import os
import datetime
from datetime import date
import property as p
from utility import downloaddata as dw
from utility import getDataunit as du

y,m,n=p.y,p.m,p.d
start=date(y,m,n)
stockfoldpath=p.stockdata


def get_startdate(symbfile,symbol='NIFTY',flag=True):
    if os.path.isfile(symbfile):
        with open(symbfile) as f:
                a=f.readlines()
                if len(a)<2:
                    print(symbfile, 'file is empty')
                    d=start
                else:
                    y,m,n=(a[-1].strip().split(",")[0]).split("-")
                    d=date(int(y),int(m),int(n))
                    d=d+datetime.timedelta(minutes=du.get_dataunit(symbfile))   # append time diff of two datapointsto get next start date
        return(d)
    else:
        print(symbfile,' file does not exist')
        print('creating file and downloading data')
        d = start
        dw.down_data(symbfile,symbol,flag,headerflag=True)
        return(date.today())


