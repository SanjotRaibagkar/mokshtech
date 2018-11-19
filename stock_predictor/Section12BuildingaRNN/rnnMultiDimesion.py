# Recurrent Neural Network

import nsepy
import datetime
from datetime import date

# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
symbole = "BANKNIFTY"

#dataset_train  = pd.DataFrame(nsepy.get_history(symbol=symbole,
#                            start=date(2001,1,1), 
#                            end=date.today(),
#                            index=True))

#dataset_train.to_csv("banknifty_all_csv.csv")
#dataset_test  = pd.DataFrame(nsepy.get_history(symbol=symbole,
#                            start=date(2018,10,1), 
#                            end=date(2018,10,31),
#                            index=True))
#dataset_test.to_csv("banknifty_test_csv.csv")
# Importing the training set
#dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
noofDays =20
noifDaysforYtrain =1
timestep = 120
dataset_train = pd.read_csv('banknifty_all_csv.csv')
training_set = dataset_train.iloc[0:len(dataset_train)-noofDays, :]
training_set = training_set.iloc[:, 4:6]
training_set['Volume'].fillna(training_set['Volume'].mean(),inplace= True )


# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Creating a data structure with  timesteps and noof days output
X_train = []
y_train = []
for i in range(timestep, len(training_set)-noifDaysforYtrain):
    X_train.append(training_set_scaled[i-timestep:i, 0:2])
   # y_train.append(training_set_scaled[i:i+noofDays, 0])
    y_train.append(training_set_scaled[i:i+noifDaysforYtrain, 0])
   
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
#X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))



# Part 2 - Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], X_train.shape[2])))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer

regressor.add(Dense(units = noifDaysforYtrain))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs = 2, batch_size = 32)



# Part 3 - Making the predictions and visualising the results


dataset_test = dataset_train[len(dataset_train)-timestep-noofDays:]


inputs =dataset_test.iloc[:, 4:6]
inputs['Volume'].fillna(inputs['Volume'].mean(),inplace= True )
real_stock_price = inputs.iloc[timestep:].values
inputs = inputs.values

#inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(timestep, len(inputs)):
    X_test.append(inputs[i-timestep:i, 0:2])
X_test = np.array(X_test)
#X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price_all = regressor.predict(X_test)

if X_test.shape[2] >1 and predicted_stock_price_all.shape[1] ==1:
    
    predicted_stock_price_all = np.insert(predicted_stock_price_all,obj=1,values=0, axis =1)

predicted_stock_price = sc.inverse_transform(predicted_stock_price_all)

#predicted_stock_price = sc.inverse_transform(predicted_stock_price_all[:,:2])

#predicted_stcok_price_next_noofDays = predicted_stock_price_all[:1,:]
#predicted_stcok_price_next_noofDays.shape = (noofDays,1)
#predicted_stcok_price_next_noofDays = np.insert(predicted_stcok_price_next_noofDays,obj=1,values=0, axis =1)
#predicted_stcok_price_next_noofDays = sc.inverse_transform(predicted_stcok_price_next_noofDays)
# Visualising the results
plt.plot(real_stock_price[:,0], color = 'red', label = 'Real Bank Nifty Price')
plt.plot(predicted_stock_price[:,0], color = 'blue', label = 'Predicted Bank Nifty Price')
#plt.plot(predicted_stcok_price_next_noofDays[:,0], color = 'green', label = 'Predicted Bank Nifty Price')
plt.title('Bank Nifty  Price Prediction')
plt.xlabel('Time')
plt.ylabel('Bank Nifty Stock Price')
plt.legend()
plt.show()


from keras.models import model_from_json
import os

symbol = 'BANKNIFTYRNNMultiDim_'+noofDays
# serialize model to JSON
model_json = regressor.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
regressor.save_weights(symbol+".h5")
print("Saved model to disk")
#### Reading Model from disk

#json_file = open('model.json', 'r')
#loaded_model_json = json_file.read()
#json_file.close()
#loaded_model = model_from_json(loaded_model_json)
## load weights into new model
#loaded_model.load_weights("model.h5")
#print("Loaded model from disk")
# 
## evaluate loaded model on test data
#loaded_model.compile(optimizer = 'adam', loss = 'mean_squared_error')
#
#score = loaded_model.predict(X_test)
#print(score)
#score = sc.inverse_transform(score)
#print(score)



