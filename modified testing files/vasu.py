import datetime

import math
import numpy as np
import pandas as pd
import random

from scipy.signal import find_peaks

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator

def sample_segment(dataframe, seed, sample_length=120):
	random.seed(seed)
	start_ix = random.randint(0,len(dataframe)-sample_length)	
	sample_data = dataframe[start_ix:start_ix+sample_length].copy()
	#print(sample_data)
	return sample_data

def split_data(dataframe):
	train_data = dataframe[(dataframe['high_slope'].notnull()) | (dataframe['low_slope'].notnull())].copy()
	test_data = dataframe[~((dataframe['high_slope'].notnull()) | (dataframe['low_slope'].notnull()))].copy()
	#print(train_data,test_data)
	return train_data,test_data

def get_latest_peak_info(dataframe):
    return_dict = {}
    high_data = dataframe[dataframe['high_slope'].notnull()].tail(1)
    low_data = dataframe[dataframe['low_slope'].notnull()].tail(1)
    latest_high_date = high_data.index.to_pydatetime()[0]
    latest_low_date = low_data.index.to_pydatetime()[0]

    if latest_high_date > latest_low_date:
        return_dict['peak_type'] = 'high'
        return_dict['peak_data'] = high_data
    elif latest_high_date < latest_low_date:
        return_dict['peak_type'] = 'low'
        return_dict['peak_data'] = low_data
    else:
        return_dict['peak_type'] = 'high&low'
        return_dict['peak_data'] = low_data
    
    return return_dict

def plot_candlestic(dataframe, stock_name):
    
    fig, ax = plt.subplots(figsize = (16,7))
    fig.subplots_adjust(bottom=0.2)

    quotes = zip(mdates.date2num(dataframe.index.to_pydatetime()),dataframe[u'Open'], 
                     dataframe[u'High'],dataframe[u'Low'], dataframe[u'Close'])
    candlestick_ohlc(ax,quotes,width=0.75,colorup='g',colordown='red',alpha=0.6)
    ax.xaxis_date()
    ax.legend([stock_name],loc='upper right', shadow=True, fancybox=True)
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    plt.show()

def plot_candlestic_with_extrema(dataframe, peak_indices, trough_indices, stock_name):
    
    fig, ax = plt.subplots(figsize = (16,7))
    fig.subplots_adjust(bottom=0.2)

    quotes = zip(mdates.date2num(dataframe.index.to_pydatetime()),dataframe[u'Open'], 
                     dataframe[u'High'],dataframe[u'Low'], dataframe[u'Close'])
    low_price_seq = dataframe['Low'].values
    high_price_seq = dataframe['High'].values
    
    candlestick_ohlc(ax,quotes,width=0.75,colorup='g',colordown='red',alpha=0.6)
    
    plt.plot(dataframe.index[peak_indices], pd.Series(high_price_seq,index=dataframe.index)[peak_indices], "v", color='black')
    plt.plot(dataframe.index[trough_indices], pd.Series(low_price_seq,index=dataframe.index)[trough_indices], "^", color='blue')
    
    ax.xaxis_date()
    ax.legend([stock_name],loc='upper right', shadow=True, fancybox=True)
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    plt.show()
    
    
def get_trough_indices(dataframe):
    low_price_seq = dataframe['Low'].values
    trough_indices = get_troughs(low_price_seq)
    return trough_indices    

def get_peak_indices(dataframe):
    high_price_seq = dataframe['High'].values
    peak_indices = get_peaks(high_price_seq)
    return peak_indices    

def get_peaks(price_seq):
    threshold_val = np.mean(price_seq)*0.01
    peaks,peaks_properties = find_peaks(price_seq,distance=4,prominence=5)
    return peaks

def get_troughs(price_seq):
    price_seq_inv = price_seq*-1
    threshold_val = np.mean(price_seq)*0.01
    troughs,troughs_properties = find_peaks(price_seq_inv,distance=4,prominence=5)
    return troughs

def get_slope(x,y):
    dy = np.diff(y)
    dx = np.diff(x)
    slope = np.arctan(dy/dx)
    return np.insert(slope,0,0.0)    

def get_high_trend_data(dataframe):
    high_price_series = dataframe['High']
    high_price_seq = high_price_series.values
    peak_indices = get_peaks(high_price_seq)
    peak_prices = high_price_seq[peak_indices]
    
    high_slopes = get_slope(peak_indices,peak_prices)
    high_trend_data = pd.DataFrame(high_slopes,index = dataframe.index[peak_indices],columns=['high_slope'])
    return high_trend_data

def get_low_trend_data(dataframe):
    low_price_series = dataframe['Low']
    low_price_seq = low_price_series.values
    trough_indices = get_troughs(low_price_seq)
    trough_prices = low_price_seq[trough_indices]
    
    low_slopes = get_slope(trough_indices,trough_prices)
    low_trend_data = pd.DataFrame(low_slopes,index = dataframe.index[trough_indices],columns=['low_slope'])
    return low_trend_data

def get_trend_label(high_slope,low_slope):
    if math.isnan(high_slope) or math.isnan(low_slope):
        return 'indeterminate'
    elif high_slope == 0.0 and low_slope == 0:
        return 'indeterminate'
    elif high_slope > 0.0 and low_slope > 0.0:
        return 'bullish'
    elif high_slope < 0.0 and low_slope < 0.0:
        return 'bearish'
    else:
        return 'sideways'    
    
def get_trend_data(dataframe):
    high_trend_data = get_high_trend_data(dataframe)
    low_trend_data = get_low_trend_data(dataframe)
   
    trend_data = dataframe.join(high_trend_data)
    trend_data = trend_data.join(low_trend_data)
    trend_data = trend_data.fillna(method='bfill')
    
    trend_data['trend'] = trend_data.apply(lambda row: get_trend_label(row['high_slope'], row['low_slope']), axis=1)
    return trend_data 

def get_ma_slope(price_series, ma_period = 8, slope_period = 8):
    ma_series = price_series.rolling(ma_period).mean()[-slope_period:]
    y1 = ma_series[0]
    y2 = ma_series[slope_period-1]
    return (((y2-y1)/y1)*100)/slope_period

def get_medium_trend(sample_data):
    medium_term_trend = get_ma_slope(sample_data['Close'],ma_period=20,slope_period=8)
    
    if medium_term_trend < 0.25 and medium_term_trend > -0.25:
        trend = 'sideways'
    elif medium_term_trend <= -0.25:
        trend = 'bearish'
    elif medium_term_trend >= 0.25:
        trend = 'bullish'
    else:
        trend = 'indeterminate' 
    
    return trend