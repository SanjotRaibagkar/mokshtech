
import datetime
import numpy as np
import pandas as pd
import random
import glob
from scipy.signal import find_peaks

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator

import vasu
list_of_files=[]




def read_data(price_file):
    price_data = pd.read_csv(price_file,index_col=0, parse_dates = True,
                             usecols = [u'Date',u'Open', u'High', u'Low', u'Close'],
                             dtype= {u'Open':np.float64,u'High':np.float64,
                                     u'Low':np.float64,u'Close ':np.float64}).sort_index()
    return price_data




for file_name in glob.glob('index_files\*.csv'):
	try:
		price_data = read_data(file_name)
		#price_data = price_data.loc[datetime.date(year=2019, month=1,day=1):datetime.date.today()]
		trend_data = vasu.get_trend_data(price_data)
    
		def split_data(dataframe):
			train_data = dataframe[(dataframe['high_slope'].notnull()) | (dataframe['low_slope'].notnull())].copy()
			test_data = dataframe[~((dataframe['high_slope'].notnull()) | (dataframe['low_slope'].notnull()))].copy()
			return train_data,test_data
    
		train_data,test_data = split_data(trend_data)
    
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
    
		peak_info =  get_latest_peak_info(train_data)
		peak_type = peak_info['peak_type']
		peak_data = peak_info['peak_data']
    
		peak_date = peak_data.index.to_pydatetime()[0]
		trend_before_peak = peak_data['trend'].values[0]
		peak_high_slope = peak_data['high_slope'].values[0]
		peak_low_slope = peak_data['low_slope'].values[0]
		peak_high = peak_data['High'].values[0]
		peak_low = peak_data['Low'].values[0]
 
		#higher high after bullish or sideways trend
		if (peak_type == 'high') and (peak_high_slope > 0.0) and (trend_before_peak != 'bearish'):
			low_mark_price = peak_low
			signal_data = test_data[test_data['Close'] < low_mark_price][1:2].copy()
        
			if len(signal_data) > 0:
				print(file_name)
				print('Sell!')
				print('Benchmark Price is : %.2f' % low_mark_price)
				print('Signal Date is : %s' % signal_data.index.to_pydatetime()[0])
				print('Closing Price on signal is : %.2f' % signal_data['Close'].values)
				list_of_files.append(file_name)  #the stocks which are beaarish
 

			signal_to_end_data = trend_data.loc[peak_date:].copy()
			signal_to_end_data['benchmark price'] = low_mark_price
			benchmark_series = signal_to_end_data['benchmark price']
    
    
			fig, ax = plt.subplots(figsize = (16,7))
			fig.subplots_adjust(bottom=0.2)

			quotes = zip(mdates.date2num(price_data.index.to_pydatetime()),price_data[u'Open'], 
                             price_data[u'High'],price_data[u'Low'], price_data[u'Close'])
			candlestick_ohlc(ax,quotes,width=0.75,colorup='grey',colordown='black' ,alpha=0.5)

			plt.plot(benchmark_series, "-", color='blue', alpha = 0.4)
			plt.plot(signal_data['Close'], "v", color='red',markersize=10,alpha = 0.8)
			plt.plot(peak_data['Close'], "x", color='b',markersize=10, alpha = 0.8)

			ax.xaxis_date()
			ax.legend([file_name],loc='upper right', shadow=True, fancybox=True)
			ax.autoscale_view()
			plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

			plt.rc('axes', grid=True)
			plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
			plt.show()
			print('----------------------------------------------------------------------------')
	
	except ValueError as VE:
		continue

for i in list_of_files:
    print(i)


