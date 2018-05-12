import datetime
import pandas as pd


path = "C:\\Prgs\\Code\\mokshtech\\stock_predictor\\database\\stockdata\\BALRAMCHIN.csv"


def get_dataunit(path):
    df=pd.read_csv(path)
    df['Date']=pd.to_datetime(df['Date'])
    a=df.iloc[1,0]
    b = df.iloc[2, 0]
    c = df.iloc[3,0]
    diff=(b-a).days*24*60
    diff1=(c-b).days*24*60
    if diff < diff1:     # Return least diff to avoid holiday gap.
        return(diff)
    else:
        return(diff1)
