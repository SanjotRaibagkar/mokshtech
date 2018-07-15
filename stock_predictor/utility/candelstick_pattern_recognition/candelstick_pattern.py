import talib
import pandas as pd
from utility import Load_Csv as lcsv
from utility import filterframe
from seaborn import palplot

ld=lcsv.Load_csv()
df=ld.LoadData(filename='BANKNIFTY.csv')

df_new = filterframe.filtered_frame(df,0)

o=df_new["Open"].values
h=df_new["High"].values
l=df_new["Low"].values
c=df_new["Close"].values

df_candle=pd.DataFrame(index=df_new.index)
df_candle["Invertedhammer"]=talib.CDLINVERTEDHAMMER(o,h,l,c)
df_candle["Kicking"]=talib.CDLKICKING(o,h,l,c)
df_candle["Hammer"]=talib.CDLHAMMER(o,h,l,c)
df_candle["shootingstar"]=talib.CDLSHOOTINGSTAR(o,h,l,c)
print(pd.DataFrame(talib.CDLINVERTEDHAMMER(o,h,l,c)))

df_candle.to_csv("candleresult.csv")

