import itertools
import operator

import talib

import utility.getsymboldata as gs
from property import *
from utility import Load_Csv as lcsv


class ta(lcsv.Load_csv):
    # coding: utf-8

    """this class contains functions to predict label with the help of technical indicators"""

    def __init__(self, symbol='NIFTY'):
        self.filename = os.path.join(stockdata, symbol + '.csv')

        try:
            if symbol in indlist:
                fflag = True
            else:
                fflag = False
            gs.getsymboldata(fflag, symbol)  # Download Latest Data for the symbol
        except Exception as e:
            print('getsymbol failed for ', symbol, e)

    def loadcsv(self):

        """load 'Date','Close', 'Volume' data from databse and return dataframe
        """
        self.loadfeatures()  # Load features data
        a = ['Date']
        a.extend(operator.concat(self.label, self.misc))

        seen = set()
        seen_add = seen.add
        a = [x for x in a if not (x in seen or seen_add(x))]

        self.def_features = a
        self.dataset = self.LoadData(self.filename).loc[:, a]
        self.dataset['Date'] = pd.to_datetime(self.dataset['Date'])
        self.dataset = self.dataset.fillna(self.dataset.mean())

        return self.dataset

    def loadfeaturesdata(self, x):
        """load features detailed data from databse
        Row 1 will be index"""
        self.featuresdata = self.LoadfeaData(featuresdata)
        self.featuresdata.index = self.featuresdata[0]
        # self.featuresdata=self.featuresdata.loc[x]
        return list(self.featuresdata.loc[x, 1:])

    def ti_Combinations(self):
        """takes input as list of list and  gives output as comninations """
        self.paneldict = {}

        def comb_r(row):
            comb_dataset = self.dataset.copy()  # deep=True)  #Copy basic dataset to comb_dataset
            for i in row:
                comb_dataset['MA' + str(i)] = self.tdf[
                    'MA' + str(i)]  # add MA rows from tdf to comb_dataset as per the combination .
            # print('c',comb_dataset)    #To print dataset with all combinations of MA

            # print('self.paneldict',self.paneldict)
            row_s = str(row)
            self.paneldict[
                row_s] = comb_dataset.copy()  # deep=True)  # Now xfer dataframe from comb_dataset to panel_dict

        try:
            if 'MA' in self.tidict.keys():
                a = self.tidict['MA']
                # [[10],[50],[60-64]]
                comb_df = pd.Series(list(itertools.product(*a)))  ##get combinatons
                comb_df.apply(comb_r)
                self.combineset = pd.concat([self.dataset, self.tdf],
                                            axis=1)  # This dataset contains all the columns in one frame. not used anywhere. made for future purpose.

                '''
                ### Error: Panel is not working here . 
                On printing panel it is printing merge of all unique columns for each dataframe.
                
                
                #print(item for item in panel_dataset.items])  # to print item name of panel
                #print('(2, 4, 60)',panel_dataset[(2, 4, 60)])
                
                '''
            else:
                self.paneldict[0] = self.dataset.copy()

        except Exception as e:
            print('e2 technicalanalysis', e)

    def loadfeatures(self):
        """load feature label data from databse
        """
        self.featurestilist = []
        self.misc = []
        self.otherindi = []
        self.label = []
        self.tilist = dir(talib)
        self.featuredict = {}
        self.tidict = {}
        self.features = self.LoadfeaData(featurescsv)

        def func(value, args):

            if str(value).find("-") > -1:  # tocheck if range is given
                a, b = value.split("-")
                a = int(a)
                b = int(b)

                self.featuredict[args].extend(list(range(a, b)))  # if range is given then replace it by list
                self.tidict[args].append(list(range(a, b)))

            else:
                try:
                    var = str(args) + '-' + str(int(value))  # togenerate name like MA-1,MA-2
                    args_df = pd.Series(self.loadfeaturesdata(var)).dropna().astype('int64').tolist()
                    self.featuredict[args].extend(args_df)
                    self.tidict[args].append(args_df)
                except Exception as e:
                    pass

        def funr(row):
            ti = row[0]
            rowdf = pd.Series(row[1:])
            rowdf = rowdf.dropna()

            if ti in self.tilist:  # If  first element of each row of features is in tilist then they are technical indicators
                self.featuredict[ti] = []
                self.tidict[ti] = []
                self.featurestilist.append(ti)

                rowdf.apply(func, args=(ti,))  # Vectorize function over each element

            elif ti == 'label':
                self.label.append(row[1])
            elif ti == 'predict_days':
                predict_days = pd.Series(row[1:])
                predict_days = predict_days.dropna()

                self.predict_days = predict_days.values.tolist()
            elif ti == 'others':
                others = pd.Series(row[1:])
                others = others.dropna()
                self.otherindi = others.values.tolist()
            elif ti == 'test':
                pass
            else:
                row = pd.Series(row).dropna().tolist()
                self.misc.extend(row[1:])

                # vectorize approach to speed up process

        self.features.apply(funr, axis=1)

        # return(self.featurestilist,self.label,self.misc)

    def get_MA(self, x):
        malist = self.featuredict['MA']
        for i in malist:
            if ('MA' + str(i)) in self.tdf:
                continue
            else:
                try:
                    self.tdf['MA' + str(i)] = talib.SMA(self.dataset[x], i)
                except Exception as e:
                    pass
        return self.tdf

    def get_RSI(self, x):
        rsilist = self.featuredict['RSI']
        for i in rsilist:
            if ('RSI' + str(i)) in self.tdf:
                continue
            else:
                try:
                    self.dataset['RSI' + str(i)] = talib.RSI(self.dataset[x], i)
                except Exception as e:
                    pass

    def get_BBANDS(self, x):
        tperiod = int(self.featuredict['BBANDS'][0])
        upper, middle, lower = talib.BBANDS(self.dataset[x], timeperiod=tperiod, nbdevup=2, nbdevdn=2)
        self.dataset['BBu_' + str(tperiod)] = upper
        self.dataset['BBl'] = lower
        self.dataset['BBs'] = upper - lower

    def get_technical_indi(self):

        self.tdf = self.LoadData(self.filename).loc[:, [self.get_label()]]
        for i in self.featurestilist:
            if i == 'MA':
                self.get_MA(self.get_label())
            if i == 'RSI':
                self.get_RSI(self.get_label())
            if i == 'BBANDS':
                self.get_BBANDS(self.get_label())

    def get_return(self):
        self.dataset['DailyReturn'] = self.dataset[self.get_label()].pct_change()

    def get_label(self):
        return self.label[0]

    def get_otherindi(self):
        for i in self.otherindi:
            if i == 'dreturn':
                self.get_return()

    def get_panel_data(self):
        self.loadcsv()  # Update and Load Symbol Data
        self.get_technical_indi()  # Get technical indicators for features in features data
        self.get_label()  # Get label
        self.get_otherindi()  # Get other indicators which do not requires no of days parameters
        self.ti_Combinations()  # For indicators which requires combination, create different dataset
        return self.paneldict  # return dictionary of dataframes with key as combination of MA
