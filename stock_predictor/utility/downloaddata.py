import nsepy
import datetime
from datetime import date
import property as p
from property import *
from utility import getstart as gs
from utility.dbutilities.csv2sqlite.csv2sqlite import convert
from utility.dbutilities.dbqueries import db_queries
from utility.dbutilities import dbproperties as dbp


startdate=date(p.y,p.m,p.d)

def save_data(DF,file,tempfile,flag):
    DF.to_csv(tempfile, header=True,index='Date')
    if flag:
        stable = dbp.indtable
    else:
        stable = dbp.nonindtable
    try:
        dbq = db_queries()
        dbpath = dbp.sqlmokshtechdb
        con = dbq.create_connection(db_file=dbpath)
        con = convert(tempfile, dbpath=dbpath, table=stable, conn=con)
        DF.to_csv(file, mode='a',index='Date')
        print('data saved')
    except Exception as e:
        print("downdata 4 ", e)
    finally:
        con.close()



def save_all(indexflag=False,filepath=p.stockdatadelta):
    for a,b,c in os.walk(filepath):
        print(a,b,c)
        for files in c:
            filepath = os.path.join(a,files)
            print(filepath)
            Df = pd.read_csv(filepath,index_col='Date')
            save_data(Df, filepath, filepath, indexflag)


def down_data(symbfile,symbol='NIFTY',flag=True,startdate=startdate,enddate=date.today(),headerflag=False):
    try:
        dataset_train  = pd.DataFrame(nsepy.get_history(symbol=symbol,
                            start=startdate,
                            end=date.today(),
                            index=flag))
        if len(list(dataset_train.index.values)) > 2:

            if flag:  # insert symbol column for index data. bydefault nse do not returns symbol column.
                dataset_train['Symbol'] = symbol
            dataset_train=dataset_train.fillna(dataset_train.mean())
            dataset_train['Volume']=dataset_train['Volume'].astype('int64')
            dataset_train.index = pd.to_datetime(dataset_train.index)
            dataset_train=dataset_train.drop_duplicates()
            dataset_train = dataset_train.dropna(how='all')
            delsymfile = symbol + '.csv'
            delsymfilepath = os.path.join(stockdatadelta, delsymfile)
            print(delsymfilepath)
            save_data(dataset_train,symbfile,delsymfilepath,flag)
            print(symbol,' done')
        else:
            print(symbol,startdate,' not sufficient data')
    except Exception as e:
        print('Error',symbol,e)

def get_historical_data(symbol):
    ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
    symbol = symbol.upper()

    start = date(2017,7,27)
    end = date.today()
    url_string = "http://www.google.com/finance/historical?q={0}".format(symbol)
    url_string += "&startdate={0}&enddate={1}&num={0}&ei=KKltWZHCBNWPuQS9147YBw&output=csv".format(
        start.strftime('%b%d,%Y'), end.strftime('%b%d,%Y'), 4000)

    #col_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    stocks = pd.read_csv(url_string, header=0)
    df = pd.DataFrame(stocks)
    print(df)

if __name__ == '__main__':
    # save_all()
    a=nsepy.get_history(start=date(2018,1,10), end=date(2018,1,13), index=True)
    print(a.head(2))
    a.to_csv('a.csv')