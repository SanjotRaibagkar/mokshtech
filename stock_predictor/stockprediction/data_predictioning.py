
import shutil


#from matplotlib import pyplot as plt
#from seaborn import palplot as plt
from bokeh import plotting as plt
from property import *
from stockprediction import reporting as fr


class pv_visualise(object):
    def __init__(self, predict_days=1, symbol='NIFTY', flag=False):

        self.predict_days = int(predict_days)
        self.symbol = symbol
        forcastdays = self.predict_days
        self.flag = flag

    def predict_forcast(self,DF,sc,sc_y,target_testDF,regressor,  X_train, X_test, y_train, y_test, forcast_ip_scaled, header,report_dict):
        self.report_dict=report_dict

        predicted_stock_price = regressor.predict(X_test)    #This should be from row no 2 to 9
        if (len(predicted_stock_price.shape)) < 2:
            predicted_stock_price = np.reshape(predicted_stock_price, (predicted_stock_price.shape[0], 1))
        predicted_stock_price = sc.inverse_transform(predicted_stock_price).round(2)

        forcast_target_price = regressor.predict(forcast_ip_scaled)     #This should give row no 10 for 9th row input
        if len(forcast_target_price.shape) < 2:
            forcast_target_price = np.reshape(forcast_target_price, (forcast_target_price.shape[0], 1))

        forcast_target_price = sc.inverse_transform(forcast_target_price).round(2)  #This should give row no 10

        y_test = sc.inverse_transform(y_test)

        # Creating Data Frame for visualisation and storage.
        if target_testDF.shape[0] > predicted_stock_price.shape[0]:
            print('target_testDF.shape greater', target_testDF.shape[0], predicted_stock_price.shape[0])
            target_testDF = target_testDF.iloc[1:, :]

        elif target_testDF.shape[0] < predicted_stock_price.shape[0]:
            print('target_testDF.shape less', target_testDF.shape[0], predicted_stock_price.shape[0])
            predicted_stock_price = predicted_stock_price.iloc[1:, :]

        target_testDF['predicted price'] = predicted_stock_price
        df = DF.iloc[:, 0:1].copy()

        df = df.rename(columns={'Close': 'Historic  Price'})
        target_testDF['y_test'] = y_test
        result = pd.concat([df, target_testDF], axis=1)
        result = result.rename(columns={'Close': 'Real test  Price'})
        print(self.flag)
        if not self.flag:
            #Get last n dates
            dates = DF.tail(n=self.predict_days).index
        else:
            # Get future n dates for forcased values
            dates = fr.get_forcasted_dates((target_testDF.index[-3:]), self.predict_days)

        fs_df = pd.DataFrame(index=dates)
        fs_df['forcast_stock_price'] = forcast_target_price.round(2)
        result = pd.concat([df, fs_df], axis=1)
        print('predict', predicted_stock_price[-1])
        print('ytest', y_test[-1])
        print('forcast', fs_df['forcast_stock_price'][0])
        if not self.flag:
            actual_price = DF.iloc[-self.predict_days:, 0:1].rename(columns={'Close': 'ActualPrice'})
            result = pd.concat([result, actual_price], axis=1)
            print('actual', actual_price['ActualPrice'][0])


        try:


            self.report_dict = fr.create_report(self.report_dict, header, 'Dates', fs_df.index.values.astype('datetime64[m]'))
            self.report_dict = fr.create_report(self.report_dict, header, 'Forcasted', fs_df['forcast_stock_price'].tolist())
            if not self.flag:
                self.report_dict = fr.create_report(self.report_dict, header, 'Actual', actual_price['ActualPrice'].values.tolist())
        except Exception as e:
            print('reporterror', e)
        print('forcast_stock_price for {0}-D-{2} is {1} for {3}'.format(self.predict_days, fs_df['forcast_stock_price'].tolist(), header,
                                                                        fs_df.index.values.astype('datetime64[m]')))
        if self.flag:
            self.report_dict[header].to_csv(final_reportpath, mode='a', header=False, index=False)
        else:
            self.report_dict[header].to_csv(reportpath, mode='a', header=False, index=False)
            shutil.copyfile(reportpath, techreport)

        #Visualising the results
        width = 18
        height = 10
        try:
            result.plot(legend=True, title='Stock Price Prediction ' + header, figsize=(width, height))
            plt.grid(color='b', linestyle='--', linewidth=1)
            #plt.show()

            if self.flag:
                imgpath = os.path.join(repobasepath, 'finalimgs')
                imgpath = os.path.join(imgpath,str(date.today()) + header + '_final.png')
            else:
                imgpath = os.path.join(repobasepath, 'imgs')
                imgpath = os.path.join(imgpath,str(date.today())+header+'.png')
            plt.savefig(imgpath)
        except Exception as e:
            print(e)










