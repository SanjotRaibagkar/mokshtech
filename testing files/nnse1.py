from datetime import date
from nsepy import *
import pandas as pd
import os
import glob

'''
# To add new csv file in the folder
dataset_symb=input()
sbin=get_history(symbol=dataset_symb,start=date(2015,1,1),end=date.today())
sbin.to_csv(dataset_symb+'.csv')
'''

# Just to update existing files in 1 run
for file_name in glob.glob('*.csv'):
	if file_name=='HITACHIHOM.csv':
		 del(file_name)
	else:
		#print(file_name)
		dataset=pd.read_csv(file_name)
		dataset_symb=dataset['Symbol'].iloc[0]
		sbin=get_history(symbol=dataset_symb,start=date(2015,1,1),end=date.today())
		sbin.to_csv(dataset_symb+'.csv')

print('bearish files:')
os.system('python bullish_to_bearish.py')
print()
print('bullish files')
os.system('python bul_files.py')
