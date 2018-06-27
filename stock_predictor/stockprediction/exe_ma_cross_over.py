from property import *
from stockprediction.technicalanalysis import ta
from stockprediction import ma_crossover as mc
from backtest.ma_cross_reporting_visualisation import max_return_value as m_return


def exe_ma_crossover(symbol):
    b = ta(symbol)
    data = b.get_panel_data()
    def_features = b.def_features
    if b.featuredict:
        skip_days = sorted([(sorted(v).pop()) for k, v in b.featuredict.items()]).pop()
    else:
        skip_days = 0
    def funcseries(x):
        t = mc.ma_crossover(def_features, int(x), symbol)
        d2 = dict((k, t.ma_cross(v, skip_days)) for k, v in data.items())  # v is dataframe
        return d2


    # list(map(funcseries, b.predict_days))
    d2=funcseries(0)
    m_return(list(d2.values())[0])


def run_ma_crossover():
    #fr.create_reportfile(reportpath, reportcol)
    warnings.filterwarnings("ignore")
    try:
        noninddf = pd.Series(nonindlist)
        indlistdf = pd.Series(indlist)
        noninddf.apply(exe_ma_crossover)
        indlistdf.apply(exe_ma_crossover)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_ma_crossover()
