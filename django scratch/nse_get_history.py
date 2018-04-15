#Need to pip install of these library first

import pandas_datareader as pdr
from nsepy import get_history
from datetime import date
from nsepy import get_history
from datetime import date
import pandas as pd


#...... Add Ticker to stock list to get more......140 stock including Banknifty and Nifty...........
stock = [' BANKNIFTY', ' NIFTY', ' VEDL', ' RELIANCE', ' ICICIBANK', ' TATASTEEL', ' AXISBANK', ' MARUTI', ' INFY',
         ' SUNPHARMA', ' IRB', ' TATAMOTORS', ' TCS', ' SBIN', ' HINDPETRO', ' PNB', ' DLF', ' BPCL', ' HINDALCO',
         ' IOC', ' YESBANK', ' ITC', ' LT', ' JINDALSTEL', ' RELCAPITAL', ' PCJEWELLER', ' JUBLFOOD', ' HDFC', ' ONGC',
         ' BAJFINANCE', ' MGL', ' TITAN', ' BHARTIARTL', ' HINDUNILVR', ' MCDOWELL-N', ' LUPIN', ' AUROPHARMA',
         ' JPASSOCIAT', ' CANBK', ' HDFCBANK', ' ADANIENT', ' JSWSTEEL', ' TECHM', ' HCLTECH', ' FEDERALBNK',
         ' GMRINFRA', ' INDUSINDBK', ' APOLLOTYRE', ' RELINFRA', ' EXIDEIND', ' TATAGLOBAL', ' M&M', ' BANKBARODA',
         ' KOTAKBANK', ' CEATLTD', ' NATIONALUM', ' SAIL', ' ARVIND', ' DRREDDY', ' BALKRISIND', ' IDEA', ' BANKINDIA',
         ' BHEL', ' IBULHSGFIN', ' CIPLA', ' INDIGO', ' VOLTAS', ' COALINDIA', ' HEROMOTOCO', ' LICHSGFIN', ' ASHOKLEY',
         ' HEXAWARE', ' ESCORTS', ' IDFCBANK', ' SRF', ' BAJAJ-AUTO', ' PFC', ' MOTHERSUMI', ' BATAINDIA',
         ' TV18BRDCST', ' EICHERMOT', ' IDBI', ' ADANIPORTS', ' UNIONBANK', ' JUSTDIAL', ' KSCL', ' M&MFIN', ' RECLTD',
         ' BEML', ' BHARATFORG', ' NCC', ' DHFL', ' BIOCON', ' L&TFH', ' MANAPPURAM', ' SUNTV', ' CANFINHOME', ' RCOM',
         ' GRASIM', ' CESC', ' INDIACEM', ' TATAPOWER', ' GAIL', ' TATAMTRDVR', ' UPL', ' NMDC', ' BALRAMCHIN',
         ' ADANIPOWER', ' SREINFRA', ' AMBUJACEM', ' MINDTREE', ' IDFC', ' HINDZINC', ' ASIANPAINT', ' DIVISLAB',
         ' SRTRANSFIN', ' IGL', ' DISHTV', ' KPIT', ' NTPC', ' SOUTHBANK', ' JETAIRWAYS', ' HAVELLS', ' ACC',
         ' CENTURYTEX', ' KTKBANK', ' WIPRO', ' TVSMOTOR', ' RBLBANK', ' JISLJALEQS', ' RPOWER', ' BEL', ' UJJIVAN',
         ' HDIL', ' SYNDIBANK', ' NHPC', ' RAYMOND', ' BHARATFIN', ' IFCI', ' ALBK']

#.........Loop To download derivative ->(Open_interest)..........................
#.........add get_history(to accquire other month looking at last thursday)......

start1=date(2018,1,1)
start2=date(2018,1,26)  #the day after end1

start3=date(2018,2,23)  #the day after end2

end1=date(2018,1,25)
end2=date(2018,2,22)    #end3=date(2018,3,29)

for stock in stock:
    data_fut = get_history(symbol=stock,futures=True,start=start1, end=end1,
                           expiry_date=date(2018,1,25))
    data_fut2 = get_history(symbol=stock,futures=True,start=start2, end=end2,
                            expiry_date=date(2018,2,22))

    
    
    VEDL_total= pd.concat([data_fut, data_fut2]) 
    VEDL_total.to_csv("C:\\NSE_OI\\" +stock+ "_OI.csv", encoding ='utf-8', index =True)
    print(stock)



#.....................Loop To Download Historic Data ->(OHLC)....................
for stock in stock:
    data_his = get_history(symbol=stock, start=date(2018,1,1), end=date(2018,2,22))
    data_his.to_csv("C:\\NSE_hist\\" +stock+ ".csv", encoding ='utf-8', index =True)
    data_his = pd.read_csv("C://NSE_hist//" +stock+ "_hist.csv")
    data_his.set_index('Date',inplace = True)
    print(stock)
