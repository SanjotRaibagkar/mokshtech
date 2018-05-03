# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

import matplotlib.pyplot as plt
from datetime import date
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from stockprediction import filterreport as fr
from property import *


class ml_dpmodels(object):
    def __init__(self, predict_days=1, symbol='NIFTY'):
        self.predict_days = 10  # int(predict_days)
        self.report_dict = {}
        self.symbol = symbol

    def data_preprocessing(self, train_paneldict, skipdays):

        train_paneldict=train_paneldict.iloc[:-self.predict_days, :]
        df_total = train_paneldict.iloc[:, :]
        y = train_paneldict.iloc[self.predict_days:, 0:1]  # Close  # implement method to get label from file
        self.df = df_total.iloc[:-self.predict_days, :]

        # create report header
        header = self.symbol + "_" + str(self.predict_days) + "_" + ("_".join(str(i) for i in self.df.columns.tolist()))
        header = header.replace("Close_Open_Volume_", "")
        print('header', header)
        self.report_dict[header] = pd.DataFrame(columns=['MSE', 'RMSE'], index=[header])

        # feature scaling
        self.sc = MinMaxScaler(feature_range=(0, 1))
        df_total_scaled = self.sc.fit_transform(df_total)  # This is total dataset
        y_scaled = self.sc.fit_transform(y)
        forcast_scaled = df_total_scaled[-self.predict_days:]
        df_scaled = df_total_scaled[:-self.predict_days]

        ### Split Data set as per test size.
        splitcount = int(df_scaled.shape[0] * test_size)  # +1

        '''
        df_scaled_shape=df_scaled.shape[0]

        X_train=df_scaled[:(df_scaled_shape-splitcount),:]
        X_test=df_scaled[(df_scaled_shape-splitcount):,:]

        #self.X_test_df=df_total.iloc[-(self.predict_days+splitcount):-self.predict_days,:]

        y_train=y_scaled[:(df_scaled_shape-splitcount),:]
        y_test=y_scaled[(df_scaled_shape-splitcount):,:]
        self.y_test_df = y.iloc[-(splitcount):, :]

        #'''
        self.y_test_df = y.iloc[-(splitcount):, :]

        # Creating data sctructure for test and training
        X_train, X_test, y_train, y_test = train_test_split(df_scaled, y_scaled, test_size=test_size)
        X_train, y_train = np.array(X_train), np.array(y_train)

        # Reshape xtrain and xtest to fit in lstm model

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        forcast_scaled = np.reshape(forcast_scaled, (forcast_scaled.shape[0], forcast_scaled.shape[1], 1))

        print(X_train.shape, X_test.shape, y_train.shape, y_test.shape, df_scaled.shape, y_scaled.shape)
        self.X_test, self.X_train, self.y_test, self.y_train, self.forcast_scaled = X_test, X_train, y_test, y_train, forcast_scaled

        return (self.X_test, self.X_train, self.y_test, self.y_train, forcast_scaled, header)

    def build_predictmodel(self, dataframe, skipdays):
        # Initialising the RNN

        X_test, X_train, y_test, y_train, forcast_scaled, header = self.data_preprocessing(dataframe, skipdays)
        regressor = Sequential()

        # Adding the first LSTM layer and some Dropout regularisation
        regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        regressor.add(Dropout(dropoutunit))

        LSTM_units = 50
        LSTM_units = LSTM_units + LSTM_unit_increment

        # Adding a second LSTM layer and some Dropout regularisation
        regressor.add(LSTM(units=LSTM_units, return_sequences=True))
        regressor.add(Dropout(dropoutunit))

        # Adding a third LSTM layer and some Dropout regularisation
        LSTM_units = LSTM_units + LSTM_unit_increment

        regressor.add(LSTM(units=LSTM_units, return_sequences=True))
        regressor.add(Dropout(dropoutunit))

        # Adding a fourth LSTM layer and some Dropout regularisation
        LSTM_units = LSTM_units + LSTM_unit_increment
        regressor.add(LSTM(units=LSTM_units))
        regressor.add(Dropout(dropoutunit))

        # print(X_train.shape,y_train.shape)
        # Adding the output layer
        regressor.add(Dense(units=1))

        # Compiling the RNN
        regressor.compile(optimizer='adam', loss='mean_squared_error')

        # Fitting the RNN to the Training set

        regressor.fit(X_train, y_train, epochs=2, batch_size=50)
        print('rnn model build')

        score = regressor.evaluate(X_test, y_test, batch_size=50, verbose=0)

        # Result (MSE adn RMSE)
        TM_MSE = score
        TM_RMSE = math.sqrt(score)
        rep_header = header.split("_")
        ##Sample header  NIFTY_60_RSI10_BBu-10_BBl_BBs_DailyReturn_MA20_MA50_MA252
        self.report_dict[header] = pd.DataFrame(
            columns=['symbol', 'Days', 'RSI', 'BBANDS', 'MA1', 'MA2', 'MA3', 'MA4', 'MSE', 'RMSE', 'Actual',
                     'Forcasted'])
        self.report_dict[header].set_value(header, 'symbol', rep_header[0])
        self.report_dict[header].set_value(header, 'Days', rep_header[1])
        self.report_dict[header].set_value(header, 'RSI', rep_header[2][3:])
        self.report_dict[header].set_value(header, 'BBANDS', rep_header[3][4:])
        self.report_dict[header].set_value(header, 'MA1', rep_header[6][2:])
        self.report_dict[header].set_value(header, 'MA2', rep_header[7][2:])
        self.report_dict[header].set_value(header, 'MA3', rep_header[8][2:])
        if len(rep_header) > 10:
            self.report_dict[header].set_value(header, 'MA4', rep_header[9][2:])
        else:
            self.report_dict[header].set_value(header, 'MA4', '-')
        self.report_dict[header].set_value(header, 'MSE', TM_MSE)
        self.report_dict[header].set_value(header, 'RMSE', TM_RMSE)

        print('TM_MSE : {0} ,TM_RMSE : {1}'.format(TM_MSE, TM_RMSE))
        return (regressor, X_test, X_train, y_test, y_train, forcast_scaled, header)

    def predict_forcast(self, dataframe, skipdays):

        dataframe = dataframe.fillna(dataframe.mean())
        dataframe = dataframe.set_index('Date')
        dataframe = dataframe.iloc[skipdays:, :]
        regressor, X_test, X_train, y_test, y_train, forcast_scaled, header = self.build_predictmodel(dataframe,
                                                                                                      skipdays)

        # Part 3 - Making the predictions and forcasting the results
        predicted_stock_price = regressor.predict(X_test)
        predicted_stock_price = self.sc.inverse_transform(predicted_stock_price)

        y_test = self.sc.inverse_transform(y_test)
        forcast_stock_price = regressor.predict(forcast_scaled)
        forcast_stock_price = self.sc.inverse_transform(forcast_stock_price)

        print('forcast_stock_price for {0}-D-{2} is {1}'.format(self.predict_days, forcast_stock_price, header))
        self.report_dict[header].to_csv(reportpath, mode='a', header=False, index=False)

        # Creating Data Frame for visualisation and storage.
        self.y_test_df['predicted price'] = predicted_stock_price
        print('1')
        df = dataframe.iloc[:, 0:1].copy()
        print('1')

        df = df.rename(columns={'Close': 'Historic  Price'})
        print('1')

        result = pd.concat([df, self.y_test_df], axis=1)
        print('1')

        result = result.rename(columns={'Close': 'Real test  Price'})
        print('1')

        fs_df = dataframe.tail(n=self.predict_days)
        print('1')

        fs_df['forcast_stock_price'] = forcast_stock_price
        print('1')

        fs_df_modified = fs_df[['forcast_stock_price']]
        print('1')


        actual_price = dataframe.iloc[-self.predict_days:, 0:1]
        print('1')


        result = pd.concat([result, fs_df_modified], axis=1)
        print('1')

        result = pd.concat([result, actual_price], axis=1)
        print('1')

        print('predict', predicted_stock_price[-1])
        print('1')

        print('ytest', y_test[-1])
        print('1')

        print('forcast', forcast_stock_price[-1])
        print('1')

        print('actual', actual_price['Close'][-1])
        print('1')


        try:

            self.report_dict[header].set_value(header, 'Forcasted', forcast_stock_price)
            self.report_dict[header].set_value(header, 'Actual', actual_price.values)
        except Exception as e:
            print('reporterror', e)

        # Visualising the results
        width = 18
        height = 10

        try:
            result.plot(legend=True, title='Stock Price Prediction ' + header, figsize=(width, height))
            plt.grid(color='b', linestyle='--', linewidth=1)
            # plt.show()
            plt.savefig(repopath + str(date.today()) + header + '.png')
        except Exception as e:
            print(e)
