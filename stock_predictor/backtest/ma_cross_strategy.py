import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backtest.strategy import Strategy
from backtest.portfolio import Portfolio
import property as p

class MovingAverageCrossStrategy(Strategy):
    """
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - A DataFrame of bars for the above symbol.
    short_window - Lookback period for short moving average.
    long_window - Lookback period for long moving average."""

    def __init__(self, symbol, bars, short_window=100, long_window=400):
        self.symbol = symbol
        self.bars = bars

        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        """Returns the DataFrame of symbols containing the signals
        to go long, short or hold (1, -1 or 0)."""
        signals = pd.DataFrame(index=self.bars.index)
        signals['signal'] = 0.0

        # Create the set of short and long simple moving averages over the
        # respective periods
        signals['short_mavg'] = pd.rolling_mean(self.bars['Close'], self.short_window, min_periods=1)
        signals['long_mavg'] = pd.rolling_mean(self.bars['Close'], self.long_window, min_periods=1)

        # Create a 'signal' (invested or not invested) when the short moving average crosses the long
        # moving average, but only for the period greater than the shortest moving average window
        signals['signal'][self.short_window:] = np.where(signals['short_mavg'][self.short_window:]
                                                         > signals['long_mavg'][self.short_window:], 1.0, 0.0)

        # Take the difference of the signals in order to generate actual trading orders
        signals['positions'] = signals['signal'].diff()
        return signals


class MarketOnClosePortfolio(Portfolio):
    """Encapsulates the notion of a portfolio of positions based
    on a set of signals as provided by a Strategy.

    Requires:
    symbol - A stock symbol which forms the basis of the portfolio.
    bars - A DataFrame of bars for a symbol set.
    signals - A pandas DataFrame of signals (1, 0, -1) for each symbol.
    initial_capital - The amount in cash at the start of the portfolio."""

    def __init__(self, symbol, bars, signals, initial_capital=1000000.0):
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.initial_capital = float(initial_capital)
        self.positions = self.generate_positions()

    def generate_positions(self):
        positions = pd.DataFrame(index=self.signals.index).fillna(0.0) # This is an empty dataframe.
        positions[self.symbol] = 100 * self.signals['signal']  # This strategy buys 100 shares

        # for i in positions[self.symbol].index:
        #      if int(positions[self.symbol][i]) != 0:
        #         print(i,positions[self.symbol][i])
        #positions[self.symbol].to_csv('abc.csv')
        #exit(1)

        return positions

    def backtest_portfolio(self):
        self.signaldict={}
        self.signallist=[]
        portfolio = self.positions * self.bars['Close']
        pos_diff = self.positions.diff()
        for i in pos_diff[self.symbol].index:
            if pos_diff[self.symbol][i] != 0.0:
                self.signallist.append(i)
                self.signaldict[i]=pos_diff[self.symbol][i]
                #print(i,pos_diff[self.symbol][i])
        #pos_diff[self.symbol].to_csv('abc.csv')

        # exit(1)
        '''
        portfolio['holdings'] = (self.positions * self.bars['Close'])
        This statement is returning zero.
        '''
        portfolio['holdings'] = (self.positions[self.symbol] * self.bars['Close'])
        #portfolio['holdings'].to_csv('holdings.csv')
        # for i in  portfolio.index:
        #     if  portfolio['holdings'][i] != 0.0:
        #         print(i, portfolio[i])
        # pos_diff[self.symbol].to_csv('abc.csv')

        #((pos_diff * self.bars['Close']).sum(axis=1).cumsum()).to_csv('abc.csv')
        portfolio['cash'] = self.initial_capital - (pos_diff[self.symbol] * self.bars['Close']).cumsum()
        #portfolio['cash'].to_csv('cash.csv')

        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        #portfolio['total'].to_csv('total.csv')
        portfolio['returns'] = portfolio['total'].pct_change()
        #portfolio['returns'].to_csv('returns.csv')

        startidex=datetime.datetime.strptime(str(self.signallist[1]),"%Y-%m-%d %H:%M:%S")
        endIndex = datetime.datetime.strptime(str(self.signallist[-1]),"%Y-%m-%d %H:%M:%S")
        #lastIndex =
        #print('Total Money on  {1}, is {0}'.format(portfolio['total'].loc[portfolio.index == startidex].values[0],startidex))
        #print('Total Money on  {1}, is {0}'.format(portfolio['total'].loc[portfolio.index == endIndex].values[0],endIndex))
        return portfolio


