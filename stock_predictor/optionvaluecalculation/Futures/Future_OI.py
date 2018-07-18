from datetime import date, datetime
from nsepy import get_history
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
from nsepy.derivatives import get_expiry_date
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def get_expiry(year=2018,sm=1, m=12):
    '''
    :param year: start year for contracts
    :param sm: start month for contract
    :param m:  total month wise contracts
    :return:  list of expiry till current month + 2
    '''
    from nsepy.derivatives import get_expiry_date
    now = datetime.now()
    y_now = now.year
    expiry = []
    try:
        if year < y_now:
            expiry.extend(list(map(lambda x: get_expiry_date(year=year, month=x), range(sm, m + 1))))
            year = year + 1
        while(year < y_now):
            expiry.extend(list(map(lambda x:get_expiry_date(year=year, month=x) ,range(1,m+1))))
            year=year+1
        if year == y_now:
            expiry.extend(list(map(lambda x: get_expiry_date(year=y_now, month=x) if x <= now.month+2 else None, range(1, m + 1))))
    except Exception as e:
        print(e)
    if len(expiry)>0:
        while(expiry[-1] == None):
            expiry.pop(-1)
        return (expiry)
    else:
        print("not sufficient expiry dates",expiry)

def download_stockData(start,end,Flag,expiry,symbol):
    '''
    :param start: start date for data
    :param end:  end Date for data
    :param Flag: True for Index , False for Symbol
    :param expiry: expiry of contracts
    :param symbol: symbol
    :return: expiry date wise list of data
    '''
    symbol_data_list = []
    end = date(2018, 6, 28)
    for i in expiry:
        symbol_data_list.append(get_history(symbol=symbol,
                            start=start,
                            end=end,
                            index=Flag,
                            futures=True,
                            expiry_date=i))
    return symbol_data_list

def test():
    # def run2():
    #     stock = "SBIN"
    #     start = date(2017, 12, 26)
    #     end = date(2018, 1, 25)
    #     end2 = date(2018, 2, 5)
    #     data_fut = get_history(symbol=stock, futures=True, start=start, end=end,
    #                            expiry_date=date(2018, 1, 25))
    #     data_fut2 = get_history(symbol=stock, futures=True, start=start, end=end2,
    #                             expiry_date=date(2018, 2, 22))
    #
    #     OI_combined = pd.concat([data_fut2['Open Interest'], data_fut['Open Interest']],
    #                             axis=1)
    #     OI_combined['OI_Combined'] = OI_combined.sum(axis=1)
    #
    #     plt.figure(1, figsize=(10, 9))
    #     plt.subplot(211)
    #     plt.title('Open Interest')
    #     plt.plot(OI_combined.OI_Combined, label='OI')
    #     plt.plot(OI_combined.OI_Combined.rolling(5).mean(), label='OI')
    #     plt.legend(['OI', 'OI_mean'])
    #     plt.show()
    #
    #     C_combined = pd.concat([data_fut2['Close'], data_fut['Close']], axis=1)
    #     C_combined['Continous_Close'] = C_combined.iloc[:, 1].fillna(C_combined.iloc[:, 0])
    #
    #
    #
    #     plt.subplot(212)
    #     plt.title('Close')
    #     plt.plot(C_combined.Continous_Close)
    #     plt.plot(C_combined.Continous_Close.rolling(5).mean())
    #     plt.legend(['Close', 'Close_mean'])
    #     plt.show()
    #
    #     data_fut = get_history(symbol=stock, start=start, end=end, option_type='CE',
    #                            strike_price=310, expiry_date=date(2018, 1, 25))
    #     data_fut2 = get_history(symbol=stock, start=start, end=end2, option_type='CE',
    #                             strike_price=310,
    #                             expiry_date=date(2018, 2, 22))
    #     OI_combined = pd.concat([data_fut2['Open Interest'], data_fut['Open Interest']],
    #                             axis=1)
    #     plt.figure(1, figsize=(10, 9))
    #     plt.subplot(211)
    #     plt.title('Open Interest')
    #     plt.plot(OI_combined.sum(axis=1), label='OI')
    #     plt.plot(OI_combined.sum(axis=1).rolling(5).mean())
    #
    #     C_combined = pd.concat([data_fut2['Close'], data_fut['Close']], axis=1)
    #     C_combined['Continous_Close'] = C_combined.iloc[:, 1].fillna(C_combined.iloc[:, 0])
    #
    #
    #     plt.subplot(212)
    #     plt.title('Close')
    #     plt.plot(C_combined.Continous_Close, label='Close')
    #     plt.plot(C_combined.Continous_Close.rolling(5).mean())
    #     plt.show()

    now = datetime.now()
    start = date(2018, 3, 29)
    end = date(now.year, now.month + 3, now.day)
    expiry = get_expiry(year=start.year, sm=start.month)
    # expiry = [date(2017, 6, 29), date(2017, 7, 27), date(2017, 8, 31), date(2017, 9, 28), date(2017, 10, 26), date(2017, 11, 30), date(2017, 12, 28), date(2018, 1, 25), date(2018, 2, 22), date(2018, 4, 26), date(2018, 5, 31)] # , date(2018, 3, 29) skip march empty data
    symbol = "NIFTY"
    Flag = True
    stock_dict={}
    stock_dict[symbol]=download_stockData(start, end, Flag, expiry, symbol)

    symbol_dict=stock_dict[symbol]
    OI_combined = symbol_dict[0]['Open Interest'].copy()
    C_combined =  symbol_dict[0]['Close'].copy()
    for i in range(1,len(symbol_dict)):
        OI_combined =pd.concat([OI_combined,symbol_dict[i]['Open Interest']], axis=1)
        C_combined = pd.concat([C_combined,symbol_dict[i]['Close']], axis=1)

    C_combined['C_Close'] = symbol_dict[0]['Close']
    for i in range(1, len(symbol_dict)):
        C_combined['C_Close'] = C_combined['C_Close'].fillna(C_combined.iloc[:, i])


    OI_combined.to_csv("OI_combined.csv")
    C_combined.to_csv("C_combined.csv")
    sc_OI = MinMaxScaler(feature_range=(0, 1))
    sc_Close = MinMaxScaler(feature_range=(0, 1))

    result=pd.DataFrame(index=OI_combined.index)
    C_com_con = C_combined['C_Close']
    # OI_combined_sum = OI_combined.iloc[:,-1]
    #OI_combined_sum = OI_combined.rolling(2,axis='columns').sum()
    OI_combined_sum = OI_combined.sum(axis=1)
    OI_combined_sum.to_csv("OI_combined_sum.csv")

        #OI_combined.sum(axis=1)

    C_com_con.plot(legend=True, title='Close', figsize=(18, 10))
    plt.show()
    OI_combined_sum.plot(legend=True, title='OI', figsize=(18, 10))
    plt.show()

    C_com_con=np.reshape(np.array(C_com_con),(C_com_con.shape[0],1))
    OI_combined_sum = np.reshape(np.array(OI_combined_sum),(OI_combined_sum.shape[0], 1))


    OI_scaled = sc_OI.fit_transform(OI_combined_sum)
    C_combined_scaled = sc_Close.fit_transform(C_com_con)
    result["F_OI"] = OI_scaled
    result['Close'] = C_combined_scaled
    print(result.tail(3))

    result.to_csv("result.csv")
    result.plot(legend=True, title='Close and F_OI', figsize=(18, 10))

    result = result.apply(lambda x: x / x[0])
    result.head()

    result.plot(legend=True, title='Close and F_OI', figsize=(18, 10))
    plt.grid(color='b', linestyle='--', linewidth=1)
    plt.show()

    #
        #
        # # for i in range(len(symbol_dict)-2):
        # #     j, k = i + 1, i + 2
        # #     OI_combined.append(pd.concat([pd.concat([symbol_dict[i]['Open Interest'], symbol_dict[j]['Open Interest']], axis=1)
        # #                                    , symbol_dict[k]['Open Interest']], axis=1))
        # #
        # #
        # #     C_combined.append(pd.concat([pd.concat([symbol_dict[i]['Close'], symbol_dict[j]['Close']], axis=1)
        # #                       , symbol_dict[k]['Close']], axis=1))
        # #
        # #     #C_combined[i]['Continous_Close'] = C_combined[i].iloc[:, 1].fillna(C_combined[i].iloc[:, 0])
        # #C_combined.to_csv("all_combined.csv")
        # #OI_combined[-1].to_csv("combined_OI.csv")
        # #C_combined[-1].to_csv("combined.csv")
        # result=[]
        # width = 18
        # height = 10
        # for i in range(len(C_combined)):
        #     result.append(pd.DataFrame(index=OI_combined[i].index))
        #     OI_combined[i]['OI_Combined'] = OI_combined[i].sum(axis=1)
        #     C_combined[i]['Continous_Close'] = C_combined[i].iloc[:, 2].fillna(C_combined[i].iloc[:, 0])
        #     result[i]['OI_Combined'] = OI_combined[i]['OI_Combined'].copy()
        #     result[i]['Continous_Close'] = C_combined[i]['Continous_Close']
        #     result[i].plot(legend=True, title='Close and F_OI' + str(i), figsize=(width, height))
        #     plt.grid(color='b', linestyle='--', linewidth=1)
        #





