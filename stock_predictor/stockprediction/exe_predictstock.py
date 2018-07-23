from property import *
from stockprediction.technicalanalysis import ta
import stockprediction.reporting as fr
from stockprediction import predictforcastdata as pf


def predictstock(symbol):
    b = ta(symbol)
    data = b.get_panel_data()

    def_features = b.def_features
    if b.featuredict:
        skip_days = sorted([(sorted(v).pop()) for k, v in b.featuredict.items()]).pop()
    else:
        skip_days = 0

    def funcseries(x):
        t = pf.pre_for(def_features, int(x), symbol)
        d2 = dict((k, t.pf(v, skip_days)) for k, v in data.items())  # v is dataframe

    # list(map(funcseries, b.predict_days))


def exe_predictstock():
    fr.create_reportfile(reportpath, reportcol)
    warnings.filterwarnings("ignore")
    try:
        noninddf = pd.Series(nonindlist)
        indlistdf = pd.Series(indlist)
        noninddf.apply(predictstock)
        indlistdf.apply(predictstock)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    exe_predictstock()
