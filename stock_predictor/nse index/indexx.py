from datetime import date
from nsetools import Nse
from pprint import pprint
import pandas as pd
import os
import nsepy

nse=Nse()
index_codes=nse.get_index_list()

for i in index_codes:
	sbin=nsepy.get_history(symbol=i,start=date(2015,1,1),end=date.today(),index=True)
	pathh=r"G:\python code\modified testing files\index_files\_"
	sbin.to_csv(pathh+i+'.csv')

	
	
print('bearish files:')
os.system('python bullish_to_bearish_index.py')
print()
print('bullish files')
os.system('python bul_files_index.py')
