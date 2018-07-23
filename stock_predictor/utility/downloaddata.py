import nsepy
import datetime
from datetime import date
import property as p
from property import *
from utility import getstart as gs


startdate=date(p.y,p.m,p.d)
def down_data(symbfile,symbol='NIFTY',flag=True,startdate=startdate,enddate=date.today(),headerflag=False):
    try:
        print(symbol,' downloading...')
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
            dataset_train.to_csv(symbfile , mode='a', header=headerflag)

            print(symbol,' done')
        else:
            print(symbol,' not sufficient data')
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
