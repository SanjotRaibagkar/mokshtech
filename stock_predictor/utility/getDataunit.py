import datetime
import pandas as pd


path = "C:\\Prgs\\Code\\mokshtech\\stock_predictor\\database\\stockdata\\SYNDIBANK_F1.csv"


def get_dataunit(path):
    df=pd.read_csv(path)
    df['Date']=pd.to_datetime(df['Date'])
    df = df['Date']
    a=df.iloc[1]
    b = df.iloc[2]
    c = df.iloc[3]

    diff=((b-a).seconds)//60
    diff1=((c-b).seconds)//60
    if diff < diff1:     # Return least diff to avoid holiday gap.
        return (diff)
    else:
        return (diff1)

if __name__ == '__main__':
    get_dataunit(path)