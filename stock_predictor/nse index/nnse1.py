from datetime import date
from nsepy import *
import pandas as pd
import os
import glob
symb=[]

'''
dataset=pd.read_csv('Book1.csv')	
for i in dataset['Symbol'].iloc[:]:
	symb.append(i)

#Just to update existing files in 1 run
sum=0
for symb_name in symb:
	try:
		sbin=get_history(symbol=symb_name,start=date(2015,1,1),end=date.today())
		pathh=r"G:\python code\abacussss\shares\_"
		sbin.to_csv(pathh+symb_name+'.csv')
		sum+=1
		print(sum)
	
	except AttributeError as e:
		pass

print('bearish files:')
os.system('python bullish_to_bearish.py')
print()
print('bullish files')
os.system('python bul_files.py')
'''

os.system('python indexx.py')