import datetime
import pandas as pd


path = "C:\\Prgs\\Code\\mokshtech\\stock_predictor\\database\\stockdata\\SYNDIBANK_F1.csv"


def get_dataunit(path,Options):
    df=pd.read_csv(path)
    df['Date']=pd.to_datetime(df['Date'])
    df = df['Date'].unique().to_list()
    # a=df.iloc[1]
    # b = df.iloc[2]
    # c = df.iloc[3]
    if Options and len(df>3):
        return 1440
    else:
        a, b, c = df[1], df[2], df[3]

    if (b-a)<(c-b):
        if b != a:
            diff = b-a
        else:
            diff = c-b
    elif c != b:
        diff = c-b
    else:
        diff = b-a

    widthdays = diff.days*24*60
    widthmin = (diff.seconds)//60

    widthmin += widthdays
    return widthmin




if __name__ == '__main__':
    get_dataunit(path)