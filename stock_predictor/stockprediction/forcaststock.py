from property import *
from stockprediction import filterreport as fr
from stockprediction.technicalanalysis import ta
import stockprediction.filterreport as fr
from stockprediction.rnnmodel import ml_dpmodels
import utility.getsymboldata as gs



moddict = {}
def get_skip_days(symbol):
    try:
        b=ta(symbol)
        data = b.get_panel_data()
        skip_days = sorted([(sorted(v).pop()) for k, v in b.featuredict.items()]).pop()
        return skip_days
    except Exception as e:
        print('e0',e)

def c_moddict(row):
    '''This will crete a dictionary with all symboldata in mod report to avoid repeatation'''
    try:
        if row['symbol'] not in moddict.keys():
            b=ta(row['symbol'])
            moddict[row['symbol']]=b.get_panel_data()
    except Exception as e:
        print('e1',e)

def funr(row,*predict_days):
    try:

        '''This will return datafame with required symbol for a particular MA combinations'''
        key=str((row['MA1'],row['MA2'],row['MA3']))
        if row['symbol'] not in moddict.keys():
            modictkeys=moddict.keys()

            for i in modictkeys:
                row['symbol']=i
                if key in moddict[i].keys():
                    df_inuse = moddict[row['symbol']][key].copy()
                    t = ml_dpmodels(int(predict_days[0]), row['symbol'], True)
                    skip_days = get_skip_days(row['symbol'])
                    print(df_inuse.shape,skip_days)
                    t.predict_forcast(df_inuse, skip_days)

        elif key in moddict[row['symbol']].keys():
            df_inuse=moddict[row['symbol']][key].copy()
            t = ml_dpmodels(int(row['Days']), row['symbol'],True)
            skip_days=get_skip_days(row['symbol'])
            t.predict_forcast(df_inuse, skip_days)
        else:
            print(key,' does not exist for',row['symbol'])
    except Exception as e:
        print('e2',e)
def final_run(symbol='x',predict_days=1):
     try:
        mod_df=fr.mod_report()
        mod_df.apply(c_moddict, axis=1)
        fr.create_reportfile(final_reportpath, reportcol)
        warnings.filterwarnings("ignore")
        if symbol!='x' :
            moddict.clear()
            b = ta(symbol)
            moddict[symbol] = b.get_panel_data()
            mod_df=mod_df.iloc[:1,:] # keep only one row in mod_df
            for j in range(mod_df.shape[0]):
                funr(mod_df.iloc[j,:],predict_days)
        else:
            mod_df.apply(funr, axis=1)
     except Exception as e:
         print('e3',e)

if __name__ == '__main__':
    final_run()
    #final_run('NIFTY',10)   # To run for a specific symbol



