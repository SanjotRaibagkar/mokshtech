import property
from property import *
from stockprediction.technicalanalysis import ta
import stockprediction.filterreport as fr
from stockprediction.rnnmodel import ml_dpmodels

def predictstock(symbol):
    b = ta(symbol)
    data = b.get_panel_data()
    skip_days = sorted([(sorted(v).pop()) for k, v in b.featuredict.items()]).pop()
    print(skip_days)

    def funcseries(x):
        t = ml_dpmodels(int(x), symbol)
        d2 = dict((k, t.predict_forcast(v, skip_days)) for k, v in data.items())

    list(map(funcseries, b.predict_days))



fr.create_reportfile(reportpath,reportcol)
warnings.filterwarnings("ignore")
try:
    list(map(predictstock, nonindlist))
    list(map(predictstock, indlist))

except Exception as e:
    print(e)
