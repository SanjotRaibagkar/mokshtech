import stockprediction.reporting as fr
from property import *
from stockprediction.data_preprocessing import ml_dpmodels
from stockprediction.technicalanalysis import ta

moddict = {}


def get_skip_days(symbol):
    try:
        b = ta(symbol)
        data = b.get_panel_data()
        skip_days = sorted([(sorted(v).pop()) for k, v in b.featuredict.items()]).pop()
        return skip_days
    except Exception as e:
        print('e0', e)


def c_moddict(row, symbol=""):
    """This will crete a dictionary with all symboldata in mod report to avoid repeatation"""
    try:
        if symbol != "":
            print("insymbol")
            print(symbol)
            if symbol not in moddict.keys():
                print('not in key')
        if row['symbol'] in moddict.keys():
            pass
        else:
            b = ta(row['symbol'])
            moddict[row['symbol']] = b.get_panel_data()
            print(moddict.keys())

    except Exception as e:
        print('e1', e)


def funr(row):
    try:
        '''This will return datafame with required symbol for a particular MA combinations'''
        key = str((row['MA1'], row['MA2'], row['MA3']))
        if key in moddict[row['symbol']].keys():
            df_inuse = moddict[row['symbol']][key].copy()
            t = ml_dpmodels(int(row['Days']), row['symbol'], True)
            skip_days = get_skip_days(row['symbol'])
            t.predict_forcast(df_inuse, skip_days)
        else:
            print(key, ' does not exist for', row['symbol'])
    except Exception as e:
        print('e2', e)


def final_run(forcastflag=False):
    try:
        mod_df = fr.mod_report()
        mod_df.apply(c_moddict, axis=1)
        fr.create_reportfile(final_reportpath, reportcol)
        warnings.filterwarnings("ignore")
        mod_df.apply(funr, axis=1)
    except Exception as e:
        print('e3', e)


final_run(forcastflag=False)
