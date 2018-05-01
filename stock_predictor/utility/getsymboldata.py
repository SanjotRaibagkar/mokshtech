
# coding: utf-8

# '''This is only for the development purpose. Idea is to fetch data via frontend code and dump in csv.
#     till the time that code is ready we will use this. Once frontend gets ready we will retire c
import nsepy
import datetime
from datetime import date
import property
from property import *




def getsymboldata(flag,symbol):
    '''This is only for the development purpose. Idea is to fetch data via frontend code and dump in csv.
    till the time that code is ready we will use this. Once frontend gets ready we will retire code'''
    try:

        dataset_train  = pd.DataFrame(nsepy.get_history(symbol=symbol,
                            start=date(2010,1,1),
                            end=date.today(),
                            index=flag))
        dataset_train=dataset_train.fillna(dataset_train.mean())
        dataset_train['Volume']=dataset_train['Volume'].astype('int64')
        dataset_train.index = pd.to_datetime(dataset_train.index)
        print(symbol,dataset_train.head(n=3))
        dataset_train.to_csv(os.path.join(stockdata,symbol+'.csv'))
        print(symbol,' done')
    except Exception as e:
        print('Error',symbol,e)


def get_historical_data(symbol):
    ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
    symbol = symbol.upper()

    start = date(2015,1,1)
    end = date.today()
    url_string = "http://www.google.com/finance/historical?q={0}".format(symbol)
    url_string += "&startdate={0}&enddate={1}&num={0}&ei=KKltWZHCBNWPuQS9147YBw&output=csv".format(
        start.strftime('%b%d,%Y'), end.strftime('%b%d,%Y'), 4000)

    col_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    stocks = pd.read_csv(url_string, header=0, names=col_names)
    df = pd.DataFrame(stocks)
    print(df)




try:
    ind = lambda lst: getsymboldata(True, lst)
    list(map(ind, indlist))
    nonind = lambda lst: getsymboldata(False, lst)
    list(map(nonind, nonindlist))
    list(map(getsymboldata,False,nonindlist))
except Exception as e:
    print(e)




