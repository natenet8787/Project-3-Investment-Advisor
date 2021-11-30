import pandas as pd
import numpy as np
from pathlib import Path
import hvplot.pandas
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from pandas.tseries.offsets import DateOffset
from sklearn.metrics import classification_report
import requests 
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import os






btc_df = pd.read_csv(
    Path("Project 3\Resources\BTC-USD.csv"), 
    index_col='Date', 
    infer_datetime_format=True, 
    parse_dates=True
)
signals_df = btc_df.loc[:, ["Close"]]
signals_df["Actual Returns"] = signals_df["Close"].pct_change()
signals_df = signals_df.dropna()


short_window = 14
long_window = 30                 ## Setting the SMAs for the strategy 


signals_df['SMA_Fast'] = signals_df['Close'].rolling(window=short_window).mean()
signals_df['SMA_Slow'] = signals_df['Close'].rolling(window=long_window).mean()

signals_df = signals_df.dropna()

signals_df['Signal'] = 0.0

# When Actual Returns are greater than or equal to 0, generate signal to buy stock long
signals_df.loc[(signals_df['Actual Returns'] >= 0), 'Signal'] = 1

# When Actual Returns are less than 0, generate signal to sell stock short
signals_df.loc[(signals_df['Actual Returns'] < 0), 'Signal'] = -1

signals_df['Signal'].value_counts()

signals_df['Strategy Returns'] = signals_df['Actual Returns'] * signals_df['Signal'].shift()

(1 + signals_df['Strategy Returns']).cumprod().plot() 

X = signals_df[['SMA_Fast', 'SMA_Slow']].shift().dropna()

y = signals_df['Signal']

# Review the value counts
y.value_counts()

training_begin = X.index.min()

training_end = X.index.min() + DateOffset(months=6) 

X_train = X.loc[training_begin:training_end]
y_train = y.loc[training_begin:training_end]

X_test = X.loc[training_end+DateOffset(hours=1):]
y_test = y.loc[training_end+DateOffset(hours=1):]

scaler = StandardScaler()   ## Scaling the data 


X_scaler = scaler.fit(X_train)


X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

svm_model = svm.SVC()
 
# Fit the model to the data using the training data
svm_model = svm_model.fit(X_train_scaled, y_train)
 
# Use the testing data to make the model predictions
svm_pred = svm_model.predict(X_train_scaled)

# Review the model's predicted values
svm_pred[:10]

svm_testing_report = classification_report(y_train, svm_pred)

# Print the classification report
print(svm_testing_report)

# Create a predictions DataFrame 
predictions_df =  pd.DataFrame(index=X_train.index)        ## used the index from X_train as the values were not matching up with X_test and we are just looking to match the index

# Add the SVM model predictions to the DataFrame
predictions_df['Predicted'] = svm_pred

# Add the actual returns to the DataFrame
predictions_df['Actual Returns'] = signals_df['Actual Returns']

# Add the strategy returns to the DataFrame
predictions_df['Strategy Returns'] = signals_df['Strategy Returns']

(1 + predictions_df[["Actual Returns", "Strategy Returns"]]).cumprod().plot()