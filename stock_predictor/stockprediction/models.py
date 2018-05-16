import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from sklearn import neighbors
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
from sklearn import model_selection
from sklearn.metrics import mean_squared_error

from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential

import property as p

def buildModel(X_train, X_test, y_train, y_test, forcast_scaled, method):
    """
    Build final model for predicting real testing data
    """

    if method == 'RNN':
        regressor, MSE, X_train, X_test, y_train, y_test, forcast_scaled= performRNNlass(X_train, X_test, y_train, y_test, forcast_scaled)
        print(method,MSE)
        return regressor,MSE,X_train, X_test, y_train, y_test,forcast_scaled

    elif method == 'RF':
        regressor, MSE =performRFR(X_train, X_test, y_train, y_test)
        print(method,MSE)
        return regressor,MSE,X_train, X_test, y_train, y_test,forcast_scaled

    elif method == 'SVR':
        regressor, MSE, =performSVR(X_train, X_test, y_train, y_test)
        print(method,MSE)
        return  regressor,MSE,X_train,X_test,y_train , y_test,forcast_scaled

    elif method == 'KNN':
        clf = neighbors.KNeighborsClassifier()
        return

    elif method == 'ADA':
        clf = AdaBoostClassifier()
        return



def performRFR(X_train, X_test, y_train, y_test):
    print('rfr1',X_train.shape,X_test.shape, y_train.shape,y_test.shape)

    seed = p.seed
    num_trees = p.n_estimators
    n_splits=p.n_splits
    njobs=p.n_jobs

    model = RandomForestRegressor(n_estimators=num_trees, n_jobs=njobs)
    model.fit(X_train, y_train)
    MSE = mse_error(y_test,X_test,model)
    return (model,MSE)

def performRNNlass(X_train, X_test, y_train, y_test, forcast_scaled):

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    forcast_scaled = np.reshape(forcast_scaled, (forcast_scaled.shape[0], forcast_scaled.shape[1], 1))

    regressor= Sequential()

    dropoutunit=p.dropoutunit
    LSTM_unit_increment = p.LSTM_unit_increment

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

    # Adding a fifth LSTM layer and some Dropout regularisation
    LSTM_units = LSTM_units + LSTM_unit_increment
    regressor.add(LSTM(units=LSTM_units))
    regressor.add(Dropout(dropoutunit))

    # print(X_train.shape,y_train.shape)
    # Adding the output layer
    regressor.add(Dense(units=1))

    # Compiling the RNN
    regressor.compile(optimizer='adam', loss='mean_squared_error')

    # Fitting the RNN to the Training set
    regressor.fit(X_train, y_train, epochs=p.epochs, batch_size=300)
    print('rnn model build',X_test.shape)


    score = regressor.evaluate(X_test, y_test, batch_size=100, verbose=0)
    return regressor,score,X_train, X_test, y_train, y_test,forcast_scaled

def performSVR(X_train, X_test, y_train, y_test):
        model = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
        model.fit(X_train, y_train)
        MSE = mse_error(y_test,X_test,model)
        return (model, MSE)

def performKNNClass(X_train, y_train, X_test, y_test, parameters):
    """
    KNN binary Classification
    """
    clf = neighbors.KNeighborsClassifier(parameters[0])
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)

    return accuracy

def performAdaBoostClass(X_train, y_train, X_test, y_test, forcast):
    """
    Ada Boosting binary Classification
    """
    # n = parameters[0]
    # l =  parameters[1]
    clf = AdaBoostClassifier()
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)

    return accuracy


def mse_error(ytest,xtest,model):
    return mean_squared_error(ytest, model.predict(xtest))