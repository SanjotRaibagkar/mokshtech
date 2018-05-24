from property import *
from stockprediction.technicalanalysis import ta
import stockprediction.reporting as fr
from stockprediction.predictforcastdata import pre_for as pf

import sys



moddict = {}
def get_skip_days(symbol):
    try:
        b=ta(symbol)
        data = b.get_panel_data()
        def_features = b.def_features
        if b.featuredict:
            skipdays= sorted([(sorted(v).pop()) for k, v in b.featuredict.items()]).pop()
        else:
            skipdays= 0
        return skipdays,def_features
    except Exception as e:
        print('e0',e)

def c_moddict(row):
    """This will crete a dictionary with all symboldata in mod report to avoid repeatation"""
    try:
        if row['symbol'] not in moddict.keys():
            b=ta(row['symbol'])
            moddict[row['symbol']]=b.get_panel_data()
    except Exception as e:
        print('e1',e)

def funr(row,*predict_days):
    try:
        '''This will return datafame with required symbol for a particular MA combinations'''
        if np.isnan(row['MA1']):
            key=0    #if none of the MA are given in features then default value of key isset as zero.
        else:
            key = [row['MA1'],row['MA2'],row['MA3'],row['MA4']]
        if key:       # If key is zero do not convert it to tuple.
            key=str(tuple(pd.Series(key).dropna().astype('int32').tolist()))

        if row['symbol'] not in moddict.keys():
            modictkeys=moddict.keys()

            for i in modictkeys:
                row['symbol']=i
                if key in moddict[i].keys():
                    df_inuse = moddict[row['symbol']][key].copy()
                    skip_days,def_fea = get_skip_days(row['symbol'])
                    pf_obj = pf(def_features=def_fea, predict_days=int(row['Days']), symbol=row['symbol'], flag=True)
                    pf_obj.pf(df_inuse, skip_days)

        elif key in moddict[row['symbol']].keys():
            df_inuse=moddict[row['symbol']][key].copy()
            skip_days, def_fea = get_skip_days(row['symbol'])
            pf_obj = pf(def_features=def_fea, predict_days=int(row['Days']),symbol= row['symbol'], flag=True)
            pf_obj.pf(df_inuse, skip_days)
        else:
            print(key,' does not exist for',row['symbol'])
    except Exception as e:
        print('e2',sys.exc_info()[0])



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




