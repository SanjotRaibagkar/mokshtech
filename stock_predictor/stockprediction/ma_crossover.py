from utility import filterframe as ff
from backtest import ma_cross_strategy as btmc
from backtest import ma_cross_reporting_visualisation as mcrv
from datetime import date
import pandas as pd

class ma_crossover(object):
    def __init__(self,def_features=[], predict_days=1, symbol='NIFTY', flag=False):
        self.predict_days = int(predict_days)
        self.symbol = symbol
        forcastdays = self.predict_days
        self.flag = flag
        self.def_fea=def_features



    def ma_cross(self, dataframe, skipdays):
        dataframe = ff.filtered_frame(dataframe,skipdays)  # Get df wihout nan, outliers
        '''dpro_obj=rn.ml_dpmodels(self.predict_days,self.symbol,self.flag) # Create object for preprocess Data

        build_pm=gm.build_predictmodel()                                        # Create object forbuildpredictmodel
        predict_visulaise = pv.pv_visualise(self.predict_days,self.symbol,self.flag) #Create Object for prediction , forcasting and Visualisation


        #Preprocess Data and Get model
        X_train, X_test, y_train, y_test, forcast_ip_scaled, header = dpro_obj.data_preprocessing(dataframe,self.def_fea)
        '''
        '''
        #Build Models
        regressor, X_train, X_test, y_train, y_test, forcast_ip_scaled, header,self.report_dict= \
            build_pm.build_predictmodel(X_train, X_test, y_train, y_test, forcast_ip_scaled, header)

        # Predict Forcast and Visualise Models

        sc,sc_y,y_test_df=dpro_obj.sc,dpro_obj.sc_target,dpro_obj.target_testDF
        predict_visulaise.predict_forcast(dataframe,sc,sc_y,y_test_df,regressor,X_train, X_test, y_train, y_test, forcast_ip_scaled, header,self.report_dict)
        '''
        #("-".join(str(i) for i in DF.columns.tolist()))
        header=dataframe.columns.tolist()#[-1::-1]
        malist = []
        for i in range(len(header)):
            h = header[i]
            if h.startswith('MA'):
                malist.append(int(h[2:]))
        malist = sorted(malist,reverse=True)
        bars = dataframe
        mac = btmc.MovingAverageCrossStrategy(self.symbol, bars, short_window=malist[1], long_window=malist[0])
        signals = mac.generate_signals()
        #signals.to_csv('signals.csv')
        portfolio = btmc.MarketOnClosePortfolio(self.symbol, bars, signals, initial_capital=100000.0) #10 lacs
        returns = portfolio.backtest_portfolio()
        signallist,signaldict=portfolio.signallist,portfolio.signaldict

        reportname = str(date.today())+'_'+'ma_cross'
        repostring = (self.symbol,int(returns['total'][-1]),malist[0],malist[1],len(signallist))
        #        print(repostring)

        #Reporting
        report=mcrv.mac_reporting(repostring,reportname)

        # Plot two charts to assess trades and equity curve
        imgname = reportname+'_'+str(repostring)[1:-1].replace(',','_').replace("\'",'')
        #mcrv.mac_visualise(bars,signals,returns,imgname)

        # print the best result
        return report





