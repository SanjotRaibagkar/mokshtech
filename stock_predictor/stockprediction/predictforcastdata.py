from stockprediction import data_preprocessing as rn
from stockprediction import data_modeling as gm
from  stockprediction import data_predictioning as pv
from utility import filterframe as ff

class pre_for(object):
    def __init__(self,def_features=[], predict_days=1, symbol='NIFTY', flag=False):
        self.predict_days = int(predict_days)
        self.report_dict = {}
        self.symbol = symbol
        forcastdays = self.predict_days
        self.flag = flag
        self.def_fea=def_features


    def pf(self, dataframe, skipdays):
        dataframe = ff.filtered_frame(dataframe,skipdays)  # Get df wihout nan, outliers


        dpro_obj=rn.ml_dpmodels(self.predict_days,self.symbol,self.flag) # Create object for preprocess Data
        build_pm=gm.build_predictmodel()                                        # Create object forbuildpredictmodel
        predict_visulaise = pv.pv_visualise(self.predict_days,self.symbol,self.flag) #Create Object for prediction , forcasting and Visualisation




        #Preprocess Data and Get model
        X_train, X_test, y_train, y_test, forcast_ip_scaled, header = dpro_obj.data_preprocessing(dataframe,self.def_fea)

        #Build Models
        regressor, X_train, X_test, y_train, y_test, forcast_ip_scaled, header,self.report_dict= \
            build_pm.build_predictmodel(X_train, X_test, y_train, y_test, forcast_ip_scaled, header)

        # Predict Forcast and Visualise Models

        sc,sc_y,y_test_df=dpro_obj.sc,dpro_obj.sc_target,dpro_obj.target_testDF
        predict_visulaise.predict_forcast(dataframe,sc,sc_y,y_test_df,regressor,X_train, X_test, y_train, y_test, forcast_ip_scaled, header,self.report_dict)


