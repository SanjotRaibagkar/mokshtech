# Importing the Keras libraries and packages

import shutil

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import VotingClassifier


from property import *
import property as p
from stockprediction import filterreport as fr
from stockprediction import models as m


class ml_dpmodels(object):
    def __init__(self, predict_days=1, symbol='NIFTY', flag=False):
        self.predict_days = int(predict_days)
        self.report_dict = {}
        self.symbol = symbol
        forcastdays = self.predict_days
        self.flag = flag

    def data_preprocessing(self, train_paneldict, skipdays):

        if self.flag:
            pass
        else:
            # for predict model building, crop the dataset by no of days
            train_paneldict = train_paneldict.iloc[:-self.predict_days,:]
        df_total = train_paneldict.iloc[:, :]
        y = train_paneldict.iloc[self.predict_days:, 0:1]  # Close  # implement method to get label from file
        self.df = df_total.iloc[:-self.predict_days, :]

        # feature scaling
        # Note length of scaling dataframe should be same otherwise need to use separate scaling objects.
        self.sc = MinMaxScaler(feature_range=(0, 1))
        self.sc_y = MinMaxScaler(feature_range=(0, 1))

        df_total_scaled = self.sc.fit_transform(df_total)  # This is total dataset
        # print('df_total_scaled',df_total_scaled[-15:])
        y_scaled = self.sc.fit_transform(y)
        forcast_scaled = df_total_scaled[-self.predict_days:]
        # print('forcast_scaled',forcast_scaled[-10:])
        df_scaled = df_total_scaled[:-self.predict_days]
        # print('df_scaled',df_scaled[-5:])

        ### Split Data set as per test size.
        splitcount = int(df_scaled.shape[0] * test_size)  # +1

        self.y_test_df = y.iloc[-(splitcount + 1):, :]

        # Creating data sctructure for test and training
        X_train, X_test, y_train, y_test = train_test_split(df_scaled, y_scaled, test_size=test_size)
        X_train, y_train = np.array(X_train), np.array(y_train)

        # Reshape xtrain and xtest to fit in lstm model

        # X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        # X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        # forcast_scaled = np.reshape(forcast_scaled, (forcast_scaled.shape[0], forcast_scaled.shape[1], 1))
        print("X_train.shape, X_test.shape, y_train.shape, y_test.shape, df_scaled.shape, y_scaled.shape")
        print(X_train.shape, X_test.shape, y_train.shape, y_test.shape, df_scaled.shape, y_scaled.shape)

        ###Create Header
        # create report header
        header = self.symbol + "_" + str(self.predict_days) + "_" + ("_".join(str(i) for i in self.df.columns.tolist()))
        header = header.replace("Close_Open_Volume_", "")
        print('header', header)

        return X_train, X_test, y_train, y_test, forcast_scaled, header

    def build_predictmodel(self, dataframe, skipdays):
        # Initialising the RNN

        X_train, X_test, y_train, y_test, forcast_scaled, header = self.data_preprocessing(dataframe, skipdays)

        if len(p.models)>1 :

            modeldict={}
            estimators=[]
            models=pd.Series(p.models)
            def ensambeodel(i):
                key='regressor'+str(i)
                modeldict[key]=[m.buildModel(X_train, X_test, y_train,y_test,forcast_scaled,i)]
                estimators.append((str(key),modeldict[key][0]))
            models.apply(ensambeodel)

            #create the ensemble model
            ensemble = VotingClassifier(estimators)
            #ensemble.fit(X_train,y_train)
            #print(np.mean(np.abs((y_test - ensemble.predict(X_test)) / y_test)))
            from sklearn import model_selection
            kfold = model_selection.KFold(n_splits=10, random_state=7)

            results = model_selection.cross_val_score(ensemble, X_test, y_test, cv=kfold)
            print(results.mean())




            exit(1)
        else:
            regressor, score, X_train, X_test, y_train, y_test, forcast_scaled = m.buildModel(X_train, X_test, y_train, y_test, forcast_scaled=forcast_scaled, method=p.models[0])




        # regressorRF = m.buildModel(X_train, X_test, y_train,y_test,forcast_scaled,'RF')
        #
        # (regressor, score, X_train, X_test, y_train, y_test, forcast_scaled)=regressorRF

        # regressor, score, X_train, X_test, y_train, y_test, forcast_scaled = \
        #     m.buildModel(X_train, X_test, y_train, y_test, forcast_scaled=forcast_scaled, method='RF')

        # Result (MSE adn RMSE)
        TM_MSE = score
        TM_RMSE = math.sqrt(score)
        print('TM_MSE : {0} ,TM_RMSE : {1}'.format(TM_MSE, TM_RMSE))
        self.report_dict = fr.create_basic_report(self.report_dict, header)
        self.report_dict = fr.create_report(self.report_dict, header, 'MSE', TM_MSE)
        self.report_dict = fr.create_report(self.report_dict, header, 'RMSE', TM_RMSE)
        return regressor,  X_train, X_test, y_train, y_test, forcast_scaled, header

    def predict_forcast(self, dataframe, skipdays):

        dataframe = dataframe.drop_duplicates()  # Drop duplicate row
        dataframe = dataframe.dropna(how='all')  # Drop row with all columns as NA
        dataframe = dataframe.fillna(dataframe.mean())
        dataframe = dataframe.set_index('Date')
        dataframe = dataframe.iloc[skipdays:, :]
        regressor,X_train, X_test, y_train, y_test, forcast_scaled, header = self.build_predictmodel(dataframe,
                                                                                                      skipdays)


        # Part 3 - Making the predictions and forcasting the results

        # print('post model building X_test, X_train, y_test, y_train, forcast_scaled')
        # print(X_test.shape, X_train.shape, y_test.shape, y_train.shape, forcast_scaled.shape)
        print(X_test.shape)
        predicted_stock_price = regressor.predict(X_test)

        if (len(predicted_stock_price.shape)) < 2:
            predicted_stock_price = np.reshape(predicted_stock_price, (predicted_stock_price.shape[0], 1))
        predicted_stock_price = self.sc.inverse_transform(predicted_stock_price)

        forcast_stock_price = regressor.predict(forcast_scaled)
        if len(forcast_stock_price.shape) < 2:
            forcast_stock_price = np.reshape(forcast_stock_price, (forcast_stock_price.shape[0], 1))

        forcast_stock_price = self.sc.inverse_transform(forcast_stock_price)

        y_test = self.sc.inverse_transform(y_test)

        # Creating Data Frame for visualisation and storage.
        print(self.y_test_df.shape, predicted_stock_price.shape)

        if self.y_test_df.shape[0] > predicted_stock_price.shape[0]:
            print('self.y_test_df.shape greater', self.y_test_df.shape[0], predicted_stock_price.shape[0])
            self.y_test_df = self.y_test_df.iloc[1:, :]
            print('test')

        elif self.y_test_df.shape[0] < predicted_stock_price.shape[0]:
            print('self.y_test_df.shape less', self.y_test_df.shape[0], predicted_stock_price.shape[0])
            predicted_stock_price = predicted_stock_price.iloc[1:, :]

        self.y_test_df['predicted price'] = predicted_stock_price
        df = dataframe.iloc[:, 0:1].copy()

        df = df.rename(columns={'Close': 'Historic  Price'})
        self.y_test_df['y_test'] = y_test
        result = pd.concat([df, self.y_test_df], axis=1)
        result = result.rename(columns={'Close': 'Real test  Price'})

        dates = fr.get_forcasted_dates((self.y_test_df.index[-3:]), self.predict_days)  # Get dates for forcased values
        fs_df = pd.DataFrame(index=dates)
        fs_df.index = pd.to_datetime(fs_df.index)
        fs_df['forcast_stock_price'] = forcast_stock_price
        result = pd.concat([result, fs_df], axis=1)
        # if self.flag==False:
        actual_price = dataframe.iloc[-self.predict_days:, 0:1].rename(columns={'Close': 'ActualPrice'})
        result = pd.concat([result, actual_price], axis=1)
        # print(result.tail(n=(self.predict_days+self.predict_days+self.predict_days)))

        print('predict', predicted_stock_price[-1])
        print('ytest', y_test[-1])
        print('forcast', forcast_stock_price[-1])
        print('actual', actual_price['ActualPrice'][-1])

        try:
            self.report_dict = fr.create_report(self.report_dict, header, 'Dates', fs_df.index.values)
            self.report_dict = fr.create_report(self.report_dict, header, 'Forcasted', forcast_stock_price)
            # if self.flag==False:
            self.report_dict = fr.create_report(self.report_dict, header, 'Actual', actual_price['ActualPrice'].values)
        except Exception as e:
            print('reporterror', e)
        print('forcast_stock_price for {0}-D-{2} is {1} for {3}'.format(self.predict_days, forcast_stock_price, header,
                                                                        fs_df.index.values))
        if self.flag:
            self.report_dict[header].to_csv(final_reportpath, mode='a', header=False, index=False)
        else:
            self.report_dict[header].to_csv(reportpath, mode='a', header=False, index=False)
            shutil.copyfile(reportpath, techreport)

        # Visualising the results
        width = 18
        height = 10

        # try:
        #     result.plot(legend=True, title='Stock Price Prediction ' + header, figsize=(width, height))
        #     plt.grid(color='b', linestyle='--', linewidth=1)
        #     #plt.show()
        #
        #     if self.flag:
        #         imgpath = os.path.join(repobasepath, 'finalimgs')
        #         imgpath = os.path.join(imgpath, +str(date.today()) + header + '_final.png')
        #     else:
        #         imgpath = os.path.join(repobasepath, 'imgs')
        #         imgpath = os.path.join(imgpath,+str(date.today())+header+'.png')
        #     plt.savefig(imgpath)
        # except Exception as e:
        #     print(e)













        ##############
        '''
        #Manual Split
        df_scaled_shape=df_scaled.shape[0]
        X_train=df_scaled[:-splitcount,:]
        X_test=df_scaled[-splitcount:,:]
        #X_test_df=df_total.iloc[-(self.predict_days+splitcount):-self.predict_days,:]
        y_train=y_scaled[:-splitcount,:]
        y_test=y_scaled[-splitcount:,:]
        '''
        ################
