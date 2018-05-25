import property as p
import pandas as pd

from sklearn.ensemble import VotingClassifier
import math
from stockprediction import models as m
from stockprediction import reporting as fr
#
# from brew.base import Ensemble, EnsembleClassifier
# from brew.stacking.stacker import EnsembleStack, EnsembleStackClassifier
# from brew.combination.combiner import Combiner
#
# from keras.layers.core import Dense, Dropout
# from keras.layers.recurrent import LSTM
# from keras.models import Sequential
# from sklearn import neighbors
# from sklearn import svm
# from sklearn.ensemble import AdaBoostClassifier
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error

class build_predictmodel(object):
    def __init__(self):
        self.report_dict={}

    def build_predictmodel(self, X_train, X_test, y_train, y_test, forcast_ip_scaled, header):
        # Initialising the RNN

        if len(p.models) > 1:
            modeldict = {}
            estimators = []
            models = pd.Series(p.models)

            def ensambeodel(i):
                key =str(i)
                modeldict[key] = [m.buildModel(X_train, X_test, y_train, y_test, forcast_ip_scaled, i)]
                estimators.append((modeldict[key][0]))

            models.apply(ensambeodel)

            print(estimators)

            # create the ensemble model
            ensemble = VotingClassifier(estimators)
            # ensemble.fit(X_train,y_train)
            # print(np.mean(np.abs((y_test - ensemble.predict(X_test)) / y_test)))
            from sklearn import model_selection
            print('ok')

            kfold = model_selection.KFold(n_splits=10, random_state=7)
            print('ok')




            results = model_selection.cross_val_score(ensemble, X_test, y_test, cv=kfold)
            print(results.mean())

        #     # Initializing Classifiers
        #     clf1 = Sequential(random_state=0)
        #     clf2 = RandomForestRegressor(random_state=0)
        #     clf3 = svm.SVR(random_state=0, probability=True)
        #
        #    # Creating Ensemble
        # ensemble = Ensemble([clf1, clf2, clf3])
        # eclf = EnsembleClassifier(ensemble=ensemble, combiner=Combiner('mean'))
        #
        # # Creating Stacking
        # layer_1 = Ensemble([clf1, clf2, clf3])
        # layer_2 = Ensemble([sklearn.clone(clf1)])




            exit(1)
        else:
            regressor, score, X_train, X_test, y_train, y_test, forcast_ip_scaled = m.buildModel(X_train, X_test,
                                                                                                 y_train, y_test,
                                                                                                 forcast_scaled=forcast_ip_scaled,
                                                                                                 method=p.models[0])

        # Result (MSE adn RMSE)
        TM_MSE = score
        TM_RMSE = math.sqrt(score)
        print('TM_MSE : {0} ,TM_RMSE : {1}'.format(TM_MSE, TM_RMSE))
        self.report_dict = fr.create_basic_report(self.report_dict, header)
        self.report_dict = fr.create_report(self.report_dict, header, 'MSE', TM_MSE)
        self.report_dict = fr.create_report(self.report_dict, header, 'RMSE', TM_RMSE)
        self.report_dict = fr.create_report(self.report_dict, header, 'RMSE', TM_RMSE)
        self.report_dict = fr.create_report(self.report_dict, header, 'model', p.models[0])


        return regressor, X_train, X_test, y_train, y_test, forcast_ip_scaled, header,self.report_dict

