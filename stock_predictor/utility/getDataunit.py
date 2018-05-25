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

    # diff =((b-a).seconds)//60
    # diff1=((c-b).seconds)//60
    # if diff < diff1:     # Return least diff to avoid holiday gap.
    #     print('diff',diff)
    #     return (diff)
    # else:
    #     print('diff1',diff1)
    #
    #     return (diff1)


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