import pandas as pd
import property as p
import os

header=p.unformat_header
dbpath=p.dbpath
dirpath=os.path.join(dbpath,'stockdata_1')

def format_data():
    for d,s,f in os.walk(dirpath):
        for fold in f:
            name,ext=os.path.splitext(fold)
            if ext == '.txt':
                fold=os.path.join(dirpath,fold)
                fnew=os.path.join(dirpath,name+'.csv')
                os.rename(fold,fnew)
                df=pd.read_csv(fnew)
                df.columns=header
                df['Date']=pd.to_datetime(df['Date'].astype(str)+' '+df['Time'].astype(str))
                df=df.set_index('Date')
                df=df.drop(['Time'],axis=1)
                df=df[~df.index.duplicated(keep='last')]
                df=df.drop_duplicates(keep='last')
                df.to_csv(fnew,mode='w',header=True,index=True)

