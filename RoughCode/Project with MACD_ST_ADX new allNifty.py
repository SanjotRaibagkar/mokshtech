"""
Project Idea
My project idea is to use couple of technical indicators to identify the
momentum and trade both long and short side of the market.
The technical indicators that I plan to use are Moving Average Convergence
Divergence (MACD) indicator, a trend-following momentum indicator and Super
Trend indictor, a trend following indicator.
MACD
    MACD is calculated using two exponential moving averages (EMA) - short
    term and long term. Additionally an EMA of this MACD is used as a signal
    line to signal the upward or downward momentum.
SuperTrend
    The Super Trend indicator, is a trending indicator that can be used to
    determine whether the price is in an upward or downward trend. If the
    price is above the indicator line then it acts as a point of support, and
    if below the line it acts as a point of resistance

There are two entry points to be considered while using MACD.  One, when the
MACD line crosses the signal line.  The second is when MACD is in the positive
territory - which implies that the smaller MA is above the chosen larger MA. I
plan to use these signals to optimize my strategy.
I intend to optimize the strategy by managing the position size through a
weightage of 1 for MACD and 2 for SuperTrend. The expectation is that the MACD
will provide quick entry and exit positions.  When used with SuperTrend, it
will provide more clarity to run the trend.

Choice of stocks
There is no stock speicific criterion for using this strategy.  But as always
for any strategy to work efficiently, liquid stocks are most preferred. Hence,
I plan to focus the strategy on Nifty 50 stocks and then extend to the F&O
stocks.

Data usage
I propose to back test on daily time frame as I will be working with daily
data downloaded from Yahoo. If Quantinsti can help me get an hourly or 5 min.
data, I would be happy to backtest my strategy with that data too.

I also propose to test my strategy from year 2008 onwards.  Obviously, some of
the stocks I intend to use may not have data from 2008.  That is a known
caveat, with which I will be developing my strategy.

Programming Language
I propose to use Python for implementing my strategy. I intend to use packages
like Numpy, Panda, Matplotlib, TA-Lib.  If my strategy is not supported by any
specific package, I propose to build the indicator.

Strategy Output
As part of my output, I will be presenting the following parameters in the
report:
    o Annualized returns
    o Annualized Standard deviation
    o Annualized Sharpe ratio
    o CAGR
    o Success Ratio of Trades (no of profit trades vs no of loss trades)
    o Average Profit to Average Loss

Motivation for using this strategy
I have been following charts for a few years now. As part of my learning, I
have followed several technical indicators and am fascinated by how technical
analysts use those indicators in predicting the market.  As my strength is
programming, I want to use a strategy, which is not too heavy on concepts.  As
part of assignments, I have used R to implement the pair trading strategy.

Thanks to Abishek for his time and guidance. Following points were discussed
during the call.

1.  The submitted project is good to start.

2.   After achieving the  , Abhishek suggested to optimize the strategy by
introducing ADX indicator.

        a.  Strategy can be initiated only based on a  pre-determined
        threshold on ADX.

        b.  Since this strategy is dependent on Trend, ADX will give an
        indication when there is a trend. After which the strategy can be
        executed.

If I have missed out anything please let me know
"""
#%%
# Prepare the list of stocks (Nifty 50) to start with
# Read each stock and download the data from 2008
# Use TA-LIB to calculate the MACD on a daily basis
# Create SuperTrend indicator using the formula
import numpy as np
import pandas as pd
from pandas_datareader import data as web  # data retrieval
from matplotlib import pyplot as plt
import datetime as dt
import talib as ta
import StringIO as strio
import requests as req
import sys


# method to calculate SuperTrend indicator
# input each record and get upper band, lower band, final upper band,
# final lower band and SuperTrend indicator band
def ST(high, low, close, atr, prevfinaluband, prevfinallband, prevsupertrend,
       prevclose, multiplier=2.0):
    upperbasicband = ((high+low)/2 + (multiplier * atr))
    lowerbasicband = ((high+low)/2 - (multiplier * atr))
    if upperbasicband < prevfinaluband or prevclose > prevfinaluband:
        upperband = upperbasicband
    else:
        upperband = prevfinaluband
    if lowerbasicband > prevfinallband or prevclose < prevfinallband:
        lowerband = lowerbasicband
    else:
        lowerband = prevfinallband

    if prevsupertrend == prevfinaluband:
        if close <= upperband:
            supertrend = upperband
        else:
            supertrend = lowerband
    else:
        if prevsupertrend == prevfinallband:
            if close >= lowerband:
                supertrend = lowerband
            else:
                supertrend = upperband
        else:
            supertrend = 0.0

    return upperbasicband, lowerbasicband, upperband, lowerband, supertrend

# Input parameters for technnical indicators
macdfast = 12
macdslow = 26
macdsignal = 9
adxtimeperiod = 14
sttimeperiod = 10
stmultiplier = 3.0
adxthresh = 30
# get the latest nifty list -
# The caveat with this is that when backtesting is done there is a chance
# that the stock in this list might have not been part of NIFTY or might not
# have been traded in the secondary market
sys.stdout = open("project.txt", "w")
url = "https://www.nseindia.com/content/indices/ind_nifty50list.csv"
csvfromurl = req.get(url).content
# StringIO with utf-8
csvfordf = pd.read_csv(strio.StringIO(csvfromurl.decode('utf-8')))
nifty50df = pd.DataFrame(csvfordf)
histdata = {}
# setting the back test date as today and start date for for backtesting as
# below
adjclose = 0.0
backtestdt = dt.date.today()
startdate = dt.date(2010, 4, 1)
enddate = dt.date(2016, 12, 30)
diffyears = 0.0
diffyears = enddate.year - startdate.year
for eachscrip in nifty50df['Symbol']:
    stock = eachscrip+'.NS'
    try:
        stockdata = web.DataReader(stock, data_source='yahoo',
                                   start=startdate, end=enddate)
# Adj close is skewed when there is a corporate action.  Hence if the daily
# return is too varied say not between .75 and 1.5, then update the Adj close
# with Close data
        tempcolnum = stockdata.columns.get_loc('Adj Close')
        for i in range(1, len(stockdata)):
            adjrtn = (stockdata['Adj Close'][i] / stockdata['Adj Close'][i-1])
            if (adjrtn < 0.75 or adjrtn > 1.5):
                adjclose = stockdata['Close'][i]
            else:
                adjclose = stockdata['Adj Close'][i]
            stockdata.iloc[i, tempcolnum] = adjclose
        tempcolnum = 0
# need for identifying the firsttrade & initialize the variables
        macdfirsttrade = True
        stfirsttrade = True
        macdtraded = " "
        sttraded = " "
        buyqty = 0
        selqty = 0
        macdboughtprice = 0.0
        macdsoldprice = 0.0
        stboughtprice = 0.0
        stsoldprice = 0.0
# use MACD method in talib to get 3 details - MACD, MACDEMA and MACDHIST
# using 'Adj Close' as this is the only OHLC data being passed
        stockdata['macd'], stockdata['macdema'], stockdata['macdhist'] =\
            ta.MACD(np.asarray(stockdata['Adj Close']), fastperiod=macdfast,
                    slowperiod=macdslow, signalperiod=macdsignal)
# using 'Close' as there are other relative OHLC data used
# using Adj close will skew the output
        stockdata['adx'] =\
            ta.ADX(np.asarray(stockdata['High']),
                   np.asarray(stockdata['Low']),
                   np.asarray(stockdata['Close']),
                   timeperiod=adxtimeperiod)
#
# Calculat ATR using TALIB's method, which is needed for calculating SupeTrend
# using 'Close' as there are other OHLC data used
# using Adj close will skew the output
        stockdata['atr'] = ta.ATR(np.asarray(stockdata['High']),
                                  np.asarray(stockdata['Low']),
                                  np.asarray(stockdata['Close']),
                                  timeperiod=sttimeperiod)
# initialize for SuperTrend
        stockdata['uband'] = 0.0
        uband = 0.0
        stockdata['lband'] = 0.0
        lband = 0.04
        stockdata['finaluband'] = 0.0
        finaluband = 0.0
        stockdata['finallband'] = 0.0
        finallband = 0.0
        stockdata['supert'] = 0.0
        supert = 0.0
        multiplier = stmultiplier
        for i in range(1, len(stockdata)):
            if np.isnan(stockdata['atr'][i]):
                continue
            uband, lband, finaluband, finallband, supert =\
                ST(stockdata['High'][i], stockdata['Low'][i],
                   stockdata['Close'][i], stockdata['atr'][i],
                   stockdata['finaluband'][i-1], stockdata['finallband'][i-1],
                    stockdata['supert'][i-1], stockdata['Close'][i-1],
                    multiplier)
            tempcolnum = stockdata.columns.get_loc('uband')
            stockdata.iloc[i, tempcolnum] = uband
            tempcolnum = stockdata.columns.get_loc('lband')
            stockdata.iloc[i, tempcolnum] = lband
            tempcolnum = stockdata.columns.get_loc('finaluband')
            stockdata.iloc[i, tempcolnum] = finaluband
            tempcolnum = stockdata.columns.get_loc('finallband')
            stockdata.iloc[i, tempcolnum] = finallband
            tempcolnum = stockdata.columns.get_loc('supert')
            stockdata.iloc[i, tempcolnum] = supert
        tempcolnum = 0
# Identify Crossover Trading Signals
# Previous 2 Periods Data (avoid backtesting bias)
# look for cross over and then set the MACD Signal flag on
        stockdata['macd(-1)'] = stockdata['macd'].shift(1)
        stockdata['macdema(-1)'] = stockdata['macdema'].shift(1)
        stockdata['macd(-2)'] = stockdata['macd'].shift(2)
        stockdata['macdema(-2)'] = stockdata['macdema'].shift(2)
# SuperTrend Crossover closing price Trading Signals
# Previous Periods Data (avoid backtesting bias)
# look for cross over and then set the SuperTrend Signal flag on
        stockdata['supert(-1)'] = stockdata['supert'].shift(1)
        stockdata['supert(-2)'] = stockdata['supert'].shift(2)
        stockdata['Close(-1)'] = stockdata['Close'].shift(1)
        stockdata['Close(-2)'] = stockdata['Close'].shift(2)
# ADX change over from trending to not trending to be captured
# look for cross over and then set the ADX Signal flag on
        stockdata['adx(-1)'] = stockdata['adx'].shift(1)
# Generate Trading Signals (buy=1 , sell=-1, do nothing=0)
# if 2 days prior MACD is lower than MACDEMA and 1 day prior MACD is higher
# than MACDEMA - then crossover has happeened yesterday, which will provide a
# buy signal.  Vice versa, sell signal. 
# No signal if neither of the conditions are satisfied
# MACD Crossover Trading Strategy
# Generate Trading Strategy (own stock=1 , short stock= -1, not own stock=0)
# If signal is 1, buy. If signal is -1, sell. If already bought, sell and go
# short.  If already sold,buy and go long
        stockdata['macdsig'] = 0
        stockdata['supertsig'] = 0
        stockdata['macdstr'] = 0
        stockdata['supertstr'] = 0
        stockdata['adxsig'] = 0
        tempcolnum1 = stockdata.columns.get_loc('macdsig')
        tempcolnum2 = stockdata.columns.get_loc('supertsig')
        tempcolnum3 = stockdata.columns.get_loc('macdstr')
        tempcolnum4 = stockdata.columns.get_loc('supertstr')
        tempcolnum5 = stockdata.columns.get_loc('adxsig')
        macdsig = 0
        supertsig = 0
        macdstr = 0
        supertstr = 0
        adxsig = 0
        for i, r in enumerate(stockdata.iterrows()):
            # Set the ADX signal if the adx is above threshold
            if r[1]['adx'] >= adxthresh and r[1]['adx(-1)'] < adxthresh:
                adxsig = 1
            elif r[1]['adx'] < adxthresh and r[1]['adx(-1)'] >= adxthresh:
                adxsig = -1
            else:
                adxsig = 0
            stockdata.iloc[i, tempcolnum5] = adxsig
            if r[1]['macd(-2)'] < r[1]['macdema(-2)'] and\
                    r[1]['macd(-1)'] > r[1]['macdema(-1)'] and\
                    r[1]['adx(-1)'] >= adxthresh:
                macdsig = 1
                macdstr = 1
            elif r[1]['macd(-2)'] > r[1]['macdema(-2)'] and\
                    r[1]['macd(-1)'] < r[1]['macdema(-1)'] and\
                    r[1]['adx(-1)'] >= adxthresh:
                macdsig = -1
                macdstr = -1
            else:
                macdsig = 0
                if r[1]['adx(-1)'] >= adxthresh:
                    macdstr = stockdata['macdstr'][i-1]
                else:
                    macdstr = 0
            stockdata.iloc[i, tempcolnum1] = macdsig
            stockdata.iloc[i, tempcolnum3] = macdstr
# Generate Trading Signals (buy=1 , sell=-1, do nothing=0)
# if 2 days prior SuperTrend is lower than Closing price and 1 day prior
# SuperTrend is higher than closing price - then crossover has happened
# previous day, which will provide a buy signal.  Vice versa, sell signal. 
# No signal if neither of the conditions are satisfied.
# SuperTrend Crossover Trading Strategy
# Generate Trading Strategy (own stock=1 , short stock= -1, not own stock=0)
# If signal is 1, buy. If signal is -1, sell. If already bought, sell and go
# short.  If already sold,buy and go long
            if r[1]['supert(-2)'] < r[1]['Close(-2)'] and\
                    r[1]['supert(-1)'] > r[1]['Close(-1)'] and\
                    r[1]['adx(-1)'] > adxthresh:
                supertsig = -1
                supertstr = -1
            elif r[1]['supert(-2)'] > r[1]['Close(-2)'] and\
                    r[1]['supert(-1)'] < r[1]['Close(-1)'] and\
                    r[1]['adx(-1)'] > adxthresh:
                supertsig = 1
                supertstr = 1
            else:
                supertsig = 0
                if r[1]['adx(-1)'] >= adxthresh:
                    supertstr = stockdata['supertstr'][i-1]
                else:
                    supertstr = 0
            stockdata.iloc[i, tempcolnum2] = supertsig
            stockdata.iloc[i, tempcolnum4] = supertstr
# Set the last record to 0, to unwind all open positions
        stockdata.iloc[len(stockdata)-1, tempcolnum1] = 0
        stockdata.iloc[len(stockdata)-1, tempcolnum3] = 0
        stockdata.iloc[len(stockdata)-1, tempcolnum2] = 0
        stockdata.iloc[len(stockdata)-1, tempcolnum4] = 0
        tempcolnum1 = 0
        tempcolnum2 = 0
        tempcolnum3 = 0
        tempcolnum4 = 0
        tempcolnum5 = 0
# Fill NAN with Zeroes, so that the graphs are not skewed
        stockdata.fillna(0.0, inplace=True)
        plt.figure(1)
        plt.subplot(411)   # 4 graphs - hence 411
        plt.title('%s Closing Prices & MACD  MACD(12,26,9)' % (stock))
        plt.gca().axes.get_xaxis().set_visible(True)
        plt.plot(stockdata['Adj Close'])
        plt.legend(loc='upper left')
        plt.subplot(412)
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.plot(stockdata['macd'])
        plt.plot(stockdata['macdema'])
        plt.plot(stockdata['macdhist'], linestyle='--')
        plt.legend(loc='upper left')
        plt.subplot(413)
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.plot(stockdata['macdsig'], marker='o', linestyle='')
        plt.legend(loc='upper left')
        plt.subplot(414)
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.plot(stockdata['macdstr'], marker='o', linestyle='')
        plt.legend(loc='upper left')
        plt.show()
##########
        plt.figure(2)
        plt.subplot(311)                      # 3 graphs hence 311
        plt.title('%s Closing Prices & SuperTrend (10,3)' % (stock))
        plt.plot(stockdata['Close'])
        plt.plot(stockdata['supert'])
        plt.legend(loc='upper left')
        plt.gca().axes.get_xaxis().set_visible(True)
        plt.subplot(312)
        plt.plot(stockdata['supertsig'], marker='o', linestyle='')
        plt.legend(loc='upper left')
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.subplot(313)
        plt.plot(stockdata['supertstr'], marker='o', linestyle='')
        plt.legend(loc='upper left')
        plt.show()
##########
# Strategies Daily Returns
# Signal Crossover Strategy Without Trading Commissions
        stockdata['macddailyrtn'] = 0.0
        stockdata['supertdailyrtn'] = 0.0
        tempcolnum1 = stockdata.columns.get_loc('macddailyrtn')
        tempcolnum2 = stockdata.columns.get_loc('supertdailyrtn')
        macdailyrtn = 0
        superdailyrtn = 0
# if there is a change in strategy
#    calculate the returns as difference in today's close and today's open
# else
#    calculate the returns as difference in today's close and yday's close
        for i in range(1, len(stockdata)):
            if (stockdata['macdstr'][i] != stockdata['macdstr'][i-1]):
                # Since there is a buy-sell activity using 'Close' to
                # identify the daily retrn
                macdailyrtn = ((stockdata['Close'][i] /
                                stockdata['Open'][i])-1) *\
                                stockdata['macdstr'][i]
            else:
                # Since there is a no buy-sell using 'Adj Close' to
                # identify the daily retrn
                macdailyrtn = ((stockdata['Adj Close'][i] /
                                stockdata['Adj Close'][i-1])-1) *\
                                stockdata['macdstr'][i]
            stockdata.iloc[i, tempcolnum1] = macdailyrtn
            if (stockdata['supertstr'][i] != stockdata['supertstr'][i-1]):
                # Since there is a buy-sell activity using 'Close' to
                # identify the daily retrn
                supertdailyrtn = ((stockdata['Close'][i] /
                                   stockdata['Open'][i])-1) *\
                                   stockdata['supertstr'][i]
            else:
                # Since there is a no buy-sell using 'Adj Close' to
                # identify the daily retrn
                supertdailyrtn = ((stockdata['Adj Close'][i] /
                                   stockdata['Adj Close'][i-1])-1) *\
                                   stockdata['supertstr'][i]
            stockdata.iloc[i, tempcolnum2] = supertdailyrtn
        tempcolnum1 = 0
        tempcolnum2 = 0
# Price Crossover Strategy With Trading Commissions (1% Per Trade)
# First trade will be 1%.  Subsequent trade will have a counter trade, hence 2%.
        stockdata['macdstr(-1)'] = stockdata['macdstr'].shift(1)
        stockdata['macdtcomm'] = stockdata['macdsig']
        stockdata['supertstr(-1)'] = stockdata['supertstr'].shift(1)
        stockdata['superttcomm'] = stockdata['supertsig']
# identify trades and tradeprice
        stockdata['tradeprice'] = 0.0
        stockdata['buyqty'] = 0
        stockdata['selqty'] = 0
        stockdata['macdpl'] = 0.0
        stockdata['stpl'] = 0.0
        tempcolnum1 = stockdata.columns.get_loc('macdtcomm')
        tempcolnum2 = stockdata.columns.get_loc('superttcomm')
        tempcolnum = stockdata.columns.get_loc('tradeprice')
        tempcolnum3 = stockdata.columns.get_loc('buyqty')
        tempcolnum4 = stockdata.columns.get_loc('selqty')
        tempcolnum5 = stockdata.columns.get_loc('macdpl')
        tempcolnum6 = stockdata.columns.get_loc('stpl')
        macdtcomm = 0.0
        superttcomm = 0.0
        tradeprice = 0.0
        macdprofloss = 0.0
        stprofloss = 0.0
        for i, r in enumerate(stockdata.iterrows()):
            macdtcomm = 0.0
            superttcomm = 0.0
#            if (r[1]['macdsig'] == 1 or r[1]['macdsig'] == -1) and \
#                    r[1]['macdstr'] != r[1]['macdstr(-1)']:
#                if macdfirsttrade:
#                    macdtcomm = 0.01
#                    macdfirsttrade = False
#                else:
#                    macdtcomm = 0.02
#            else:
#                macdtcomm = 0.00
#            stockdata.iloc[i, tempcolnum1] = macdtcomm
#            if (r[1]['supertsig'] == 1 or r[1]['supertsig'] == -1) and \
#                    r[1]['supertstr'] != r[1]['supertstr(-1)']:
#                if stfirsttrade:
#                    superttcomm = 0.01
#                    stfirsttrade = False
#                else:
#                    superttcomm = 0.02
#            else:
#                superttcomm = 0.00
#            stockdata.iloc[i, tempcolnum2] = superttcomm
# if the signal and strategy are same and signal is positive
#     if already sold, cover + buy (2) else only buy
            if (r[1]['macdsig'] == r[1]['macdstr']):
                if (r[1]['macdsig'] == 1):
                    tradeprice = -1 * r[1]['Open']
                    macdboughtprice = r[1]['Open']
                    if (macdtraded == "S"):
                        buyqty = 2
                        macdtcomm = 0.02
                        macdprofloss = macdsoldprice - macdboughtprice
                        macdsoldprice = 0.0
                    else:
                        buyqty = 1
                        macdtcomm = 0.01
                    macdtraded = "B"
# if the signal and strategy are same and signal is negative
#     if already bought, sell + go short (2) else only go short
                elif (r[1]['macdsig'] == -1):
                    tradeprice = r[1]['Open']
                    macdsoldprice = r[1]['Open']
                    if (macdtraded == "B"):
                        selqty = 2
                        macdtcomm = 0.02
                        macdprofloss = macdsoldprice - macdboughtprice
                        macdboughtprice = 0.0
                    else:
                        selqty = 1
                        macdtcomm = 0.01
                    macdtraded = "S"
# if if the signal and strategy are same (0) and signal is NO SIGNAL
# then close the open positions as the ADX signal may not be trending
                else:
                    if (macdtraded == "S"):
                        tradeprice = -1 * r[1]['Open']
                        macdboughtprice = r[1]['Open']
                        buyqty = 1
                        macdtcomm = 0.01
                        macdprofloss = macdsoldprice - macdboughtprice
                        macdsoldprice = 0.0
                    elif (macdtraded == "B"):
                        tradeprice = r[1]['Open']
                        macdsoldprice = r[1]['Open']
                        selqty = 1
                        macdtcomm = 0.01
                        macdprofloss = macdsoldprice - macdboughtprice
                        macdboughtprice = 0.0
                    macdtraded = " "
# if the signal and strategy are same and signal is positive
#     if already sold, cover + buy (4 for SuperTrend) else only buy
            if (r[1]['supertsig'] == r[1]['supertstr']):
                if (r[1]['supertsig'] == 1):
                    tradeprice = -1 * r[1]['Open']
                    stboughtprice = 2 * r[1]['Open']
                    if (sttraded == "S"):
                        buyqty += 4
                        superttcomm = 0.04
                        stprofloss = stsoldprice - stboughtprice
                        stsoldprice = 0.0
                    else:
                        buyqty += 2
                        superttcomm = 0.02
                    sttraded = "B"
# if the signal and strategy are same and signal is negative
#     if already bought, sell + go short (4 for SuperTrend) else only go short
                elif (r[1]['supertsig'] == -1):
                    tradeprice = r[1]['Open']
                    stsoldprice = 2 * r[1]['Open']
                    if (sttraded == "B"):
                        selqty += 4
                        superttcomm = 0.04
                        stprofloss = stsoldprice - stboughtprice
                        stboughtprice = 0.0
                    else:
                        selqty += 2
                        superttcomm = 0.02
                    sttraded = "S"
# if if the signal and strategy are same (0) and signal is NO SIGNAL
# then close the open positions as the ADX signal may not be trending
                else:
                    if (sttraded == "S"):
                        tradeprice = -1 * r[1]['Open']
                        stboughtprice = 2 * r[1]['Open']
                        buyqty = 2
                        superttcomm = 0.02
                        stprofloss = stsoldprice - stboughtprice
                        stsoldprice = 0.0
                    elif (sttraded == "B"):
                        tradeprice = r[1]['Open']
                        stsoldprice = 2 * r[1]['Open']
                        selqty = 2
                        superttcomm = 0.02
                        stprofloss = stsoldprice - stboughtprice
                        stboughtprice = 0.0
                    sttraded = " "
            stockdata.iloc[i, tempcolnum1] = macdtcomm
            stockdata.iloc[i, tempcolnum2] = superttcomm
            stockdata.iloc[i, tempcolnum] = tradeprice
            stockdata.iloc[i, tempcolnum3] = buyqty
            stockdata.iloc[i, tempcolnum4] = selqty
            stockdata.iloc[i, tempcolnum5] = macdprofloss
            stockdata.iloc[i, tempcolnum6] = stprofloss
            buyqty = 0
            selqty = 0
            tradeprice = 0.0
            macdprofloss = 0.0
            stprofloss = 0.0
        tempcolnum = 0
        tempcolnum1 = 0
        tempcolnum2 = 0
        tempcolnum3 = 0
        tempcolnum4 = 0
        tempcolnum5 = 0
        tempcolnum6 = 0
# MACD daily returns after removing the commission
        stockdata['macddailyrtcomm'] = 0.0
        tempcolnum1 = stockdata.columns.get_loc('macddailyrtcomm')
        macddailyrtcomm = 0
# SuperTrend daily returns after removing the commission
        stockdata['supertdailyrtcomm'] = 0.0
        tempcolnum2 = stockdata.columns.get_loc('supertdailyrtcomm')
        supertdailyrtcomm = 0
        for i in range(1, len(stockdata)):
            if (stockdata['macdstr'][i] != stockdata['macdstr'][i-1]):
                # Since there is a buy-sell activity using 'Close'
                # to identify the daily retrn
                macddailyrtcomm = (((stockdata['Close'][i] /
                                     stockdata['Open'][i])-1) -
                                   stockdata['macdtcomm'][i]) *\
                                   stockdata['macdstr'][i]
            else:
                # Since there is a no buy-sell using 'Adj Close'
                # to identify the daily retrn
                macddailyrtcomm = (((stockdata['Adj Close'][i] /
                                     stockdata['Adj Close'][i-1])-1) -
                                   stockdata['macdtcomm'][i]) *\
                                   stockdata['macdstr'][i]
            stockdata.iloc[i, tempcolnum1] = macddailyrtcomm
            # Since there is a buy-sell activity using 'Close' to
            # identify the daily retrn
            if (stockdata['supertstr'][i] != stockdata['supertstr'][i-1]):
                supertdailyrtcomm = (((stockdata['Close'][i] /
                                       stockdata['Open'][i])-1) -
                                     stockdata['superttcomm'][i]) *\
                                     stockdata['supertstr'][i]
            else:
                # Since there is a no buy-sell using 'Adj Close'
                # to identify the daily retrn
                supertdailyrtcomm = (((stockdata['Adj Close'][i] /
                                       stockdata['Adj Close'][i-1])-1) -
                                     stockdata['superttcomm'][i]) *\
                                     stockdata['supertstr'][i]
            stockdata.iloc[i, tempcolnum2] = supertdailyrtcomm
        tempcolnum1 = 0
        tempcolnum2 = 0
# MACD Cumulative Returns Calculation before comm and after comm
        stockdata['macdcumrt'] = np.cumprod(stockdata['macddailyrtn']+1)-1
        stockdata['macdcumrtcomm'] =\
            np.cumprod(stockdata['macddailyrtcomm']+1)-1
# SuperTrend Cumulative Returns Calculation before comm and after comm
        stockdata['supertcumrt'] = np.cumprod(stockdata['supertdailyrtn']+1)-1
        stockdata['supertcumrtcomm'] =\
            np.cumprod(stockdata['supertdailyrtcomm']+1)-1
# Annualized Returns from MACD
        tempcolnum = stockdata.columns.get_loc('macdcumrt')
        temprownum = len(stockdata)
        macdyrt = stockdata.iloc[temprownum-1, tempcolnum]
        tempcolnum = stockdata.columns.get_loc('macdcumrtcomm')
        temprownum = len(stockdata)
        macdyrtc = stockdata.iloc[temprownum-1, tempcolnum]
# Annualized Returns from SuperTrend
        tempcolnum = stockdata.columns.get_loc('supertcumrt')
        temprownum = len(stockdata)
        supertyrt = stockdata.iloc[temprownum-1, tempcolnum]
        tempcolnum = stockdata.columns.get_loc('supertcumrtcomm')
        temprownum = len(stockdata)
        supertyrtc = stockdata.iloc[temprownum-1, tempcolnum]
# Annualized Standard Deviation from MACD
        macdstd = np.std(stockdata['macddailyrtn'])*np.sqrt(252)
        macdstdc = np.std(stockdata['macddailyrtcomm'])*np.sqrt(252)
# Annualized Standard Deviation from SuperTrend
        supertstd = np.std(stockdata['supertdailyrtn'])*np.sqrt(252)
        supertstdc = np.std(stockdata['supertdailyrtcomm'])*np.sqrt(252)
# Annualized Sharpe Ratio from MACD
        macdsr = macdyrt/macdstd
        macdsrc = macdyrtc/macdstdc
# Annualized Sharpe Ratio from SuperTrend
        supertsr = supertyrt/supertstd
        supertsrc = supertyrtc/supertstdc
# cumulative returns - combined
        combyrt = macdyrt + supertyrt
        combyrtc = macdyrtc + supertyrtc
# Annualized Standard Deviation of returns - combined
        combstd = np.std(stockdata['macddailyrtn'] +
                         stockdata['supertdailyrtn']) * np.sqrt(252)
        combstdc = np.std(stockdata['macddailyrtcomm'] +
                          stockdata['supertdailyrtcomm']) * np.sqrt(252)
# Annualized Sharpe Ratio - combined
        combsr = combyrt/combstd
        combsrc = combyrtc/combstdc
        data = [{'0': stock, '1': 'MACD(12,26,9)', '2': 'SuperTrend(10,3)',
                '3': 'Combined'},
                {'0': 'Annualized Return', '1': format(macdyrt, '.2%'),
                '2': format(supertyrt, '.2%'), '3': format(combyrt, '.2%')},
                {'0': 'Annualized Standard Deviation',
                '1': format(macdstd, '.2%'), '2': format(supertstd, '.2%'),
                 '3': format(combstd, '.2%')},
                {'0': 'Annualized Sharpe Ratio (Rf=0%)',
                '1': format(macdsr, '.2%'), '2': format(supertsr, '.2%'),
                 '3': format(combsr, '.2%')}]
        table = pd.DataFrame(data)
        print(table)
##########
# CAGR
        macdcagr = np.power(np.abs(macdyrt), (1.0/diffyears)) - 1.0
        macdcagrc = np.power(np.abs(macdyrtc), (1.0/diffyears)) - 1.0
        stcagr = np.power(np.abs(supertyrt), (1.0/diffyears)) - 1.0
        stcagrc = np.power(np.abs(supertyrtc), (1.0/diffyears)) - 1.0
        combcagr = np.power(np.abs(combyrt), (1.0/diffyears)) - 1.0
        combcagrc = np.power(np.abs(combyrtc), (1.0/diffyears)) - 1.0
# Success Ratio of Trades (no of profit trades vs no of loss trades)
        macdpostrade = stockdata['macdpl'].gt(0).sum().sum()
        macdnegtrade = stockdata['macdpl'].lt(0).sum().sum()
        stpostrade = stockdata['stpl'].gt(0).sum().sum()
        stnegtrade = stockdata['stpl'].lt(0).sum().sum()
        macdsuccratio = (macdpostrade / float(macdpostrade+macdnegtrade))
        stsuccratio = (stpostrade / float(stpostrade+stnegtrade))
        combsuccratio = float(macdpostrade + stpostrade) /\
            float(macdpostrade + stpostrade + macdnegtrade + stnegtrade)
# Average Profit to Average Loss
        macdtotalgain = stockdata['macdpl'][stockdata.macdpl > 0].sum()
        macdwintrad = stockdata['macdpl'][stockdata.macdpl > 0].count()
        macdtotloss = stockdata['macdpl'][stockdata.macdpl < 0].sum()
        macdlosstrad = stockdata['macdpl'][stockdata.macdpl < 0].count()
        macdprofloss = float(macdtotalgain/macdwintrad) /\
            float((np.abs(macdtotloss))/macdlosstrad)
        sttotalgain = stockdata['stpl'][stockdata.stpl > 0].sum()
        stwintrad = stockdata['stpl'][stockdata.stpl > 0].count()
        sttotloss = stockdata['stpl'][stockdata.stpl < 0].sum()
        stlosstrad = stockdata['stpl'][stockdata.stpl < 0].count()
        stprofloss = float(sttotalgain/stwintrad) /\
            float((np.abs(sttotloss))/stlosstrad)
        profloss = (float(macdtotalgain+sttotalgain) /
                    float(macdwintrad+stwintrad)) /\
                   (float(np.abs(macdtotloss+sttotloss)) /
                    float(macdlosstrad+stlosstrad))
        data = [{'0': stock, '1': 'MACD(12,26,9)', '2': 'SuperTrend(10,3)',
                 '3': 'Combined'},
                {'0': 'CAGR', '1': format(macdcagr, '.2%'),
                '2': format(stcagr, '.2%'), '3': format(combcagr, '.2%')},
                {'0': 'Ratio of trades', '1': format(macdsuccratio, '.2%'),
                 '2': format(stsuccratio, '.2%'),
                 '3': format(combsuccratio, '.2%')},
                {'0': 'Profit vs Loss ratio',
                '1': format(macdprofloss, '.2%'),
                 '2': format(stprofloss, '.2%'),
                 '3': format(profloss, '.2%')}]
        table = pd.DataFrame(data)
        print(table)
    except Exception, e:
        print("\n")
        print stock, str(e), startdate, enddate
        print("\n")
        continue
sys.stdout.close
