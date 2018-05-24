from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from property import *


class ml_dpmodels(object):
    def __init__(self, predict_days=1, symbol='NIFTY', flag=False):
        self.predict_days = int(predict_days)
        self.report_dict = {}
        self.symbol = symbol
        forcastdays = self.predict_days
        self.flag = flag

    def data_preprocessing(self, dataset,*def_fea):   #Total 10 rows in dataset
        """take filtered dataframe and returns
        regressor,X_train, X_test, y_train, y_test, forcast_ip_scaled, header
        """

        if self.flag:                        #If flag true 10 rows under consideration
            DF=dataset.copy()
        else:
            # for predict model building, crop the dataset by no of days
            DF = dataset.iloc[:-self.predict_days,:]    # i.e (10-1) if predict days =1 i.e total 1 to 9 rows

        target = DF.iloc[self.predict_days:, 0:1]  # target will be from 2 to 9 Close  # implement method to get label from file
        input = DF.iloc[:-self.predict_days, :]    # input will be from 1 to 8

        # feature scaling
        # Note length of scaling dataframe should be same otherwise need to use separate scaling objects.
        self.sc = MinMaxScaler(feature_range=(0, 1))
        self.sc_target = MinMaxScaler(feature_range=(0, 1))

        DF_scaled = self.sc.fit_transform(DF)  # This is total dataset rows will be 1 to 9
        input_scaled = DF_scaled[:-self.predict_days]       # Row from 1 to 8
        target_scaled = self.sc.fit_transform(target)
        forcast_ip_scaled = DF_scaled[-self.predict_days:]  #This is row no 9

        ### Split Data set as per test size.
        splitcount = int(input_scaled.shape[0] * test_size)  # +1

        self.target_testDF = target.iloc[-(splitcount + 1):, :]   #8/3 +1 i.e from 7 to 9

        # Creating data sctructure for test and training
        X_train, X_test, y_train, y_test = train_test_split(input_scaled, target_scaled, test_size=test_size)
        X_train, y_train = np.array(X_train), np.array(y_train)

        print("X_train.shape, X_test.shape, y_train.shape, y_test.shape, input_scaled.shape, target_scaled.shape, forcast_ip_scaled.shape,DF.shape")
        print(X_train.shape, X_test.shape, y_train.shape, y_test.shape, input_scaled.shape, target_scaled.shape, forcast_ip_scaled.shape,DF.shape)

        ###Create Header
        # create report header
        header = self.symbol + "-" + str(self.predict_days) + "-" + ("-".join(str(i) for i in DF.columns.tolist()))
        if def_fea[0]:
            for x in def_fea[0]:
                header=header.replace('-'+str(x),'')
        header = header.replace("-DailyReturn","")
        print('header', header)

        return X_train, X_test, y_train, y_test, forcast_ip_scaled, header



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
