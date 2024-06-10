import datetime as dt
import sqlite3 as sql
import pandas as pd
import numpy as np
import os

# get path
home_dir = os.getcwd()

def export_chart_data(close_data_frame,valid,stock_name):
    import json

    chart_data = []

    for d,v in close_data_frame.iterrows():
                dct ={}
                dct["date"] = d.strftime("%Y-%m-%d")
                dct["close"] = v.close
                chart_data.append(dct)

    folder_path = os.path.join(home_dir, "stocks/quotes/static/forecasts/", stock_name)
    file_path = os.path.join(folder_path , "actual_data.json")
    isExist = os.path.exists(folder_path)
    if not isExist:
        os.makedirs(folder_path)
    with open(file_path, "w") as outfile:
                json.dump(chart_data, outfile , indent=2)

    chart_data = []

    for d,v in valid.Predictions.items():
                dct ={}
                dct["date"] = d.strftime("%Y-%m-%d")
                dct["close"] = v
                chart_data.append(dct)

    folder_path = os.path.join(home_dir, "stocks/quotes/static/forecasts/", stock_name)
    file_path = os.path.join(folder_path , "validate_data.json")
    isExist = os.path.exists(folder_path)
    if not isExist:
        os.makedirs(folder_path)
    with open(file_path, "w") as outfile:
                json.dump(chart_data, outfile , indent=2)

def get_stock_data(stock_name):
    """ download the data fromm yahoo fin """
    import yahoo_fin.stock_info as si

    # time interval to forecast
    year = dt.datetime.now().year
    End_Date = dt.datetime.now()
    Start_Date = End_Date.replace(year=End_Date.year-1)
    yf_data = si.get_data(stock_name, start_date= Start_Date, end_date= End_Date, index_as_date = True, interval = "1d")
    return yf_data

def forecast_stock_data(stock_name):
    """
        Forecast Function
    """
    import warnings
    import tensorflow as tf
    from sklearn.preprocessing import MinMaxScaler
    from keras.models import Sequential
    from keras.layers import Dense, LSTM
    from tensorflow import keras

    warnings.filterwarnings("ignore")
    pd.options.mode.chained_assignment = None

    # download the data fromm yahoo fin
    yf_data = get_stock_data(stock_name)

    # Sets the global random seed.
    tf.random.set_seed(0)

    # pre process
    data_frame = pd.DataFrame(data=yf_data)
    data_frame['close'].fillna(method='ffill')

    # get close data
    close_data_frame = data_frame.filter(['close'])
    close_data = close_data_frame.values

    # scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_close_data = scaler.fit_transform(close_data)

    # Get the number of rows to train the model on
    training = int(np.ceil(len(close_data) * .80))

    # Create the training data set
    # Create the scaled training data set
    train_data = scaled_close_data[0:int(training), :]

    # generate the input and output sequences
    n_lookback = 60  # length of input sequences (lookback period)
    n_forecast = 30  # length of output sequences (forecast period)
    n_features = 1   # number of features

    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []

    for i in range(n_lookback, len(train_data),1):
        x_train.append(train_data[i-n_lookback:i])
        y_train.append(train_data[i])

    # Convert the x_train and y_train to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], n_features))

    # Build the LSTM model
    model = Sequential()
    # Adding the First input hidden layer and the LSTM layer
    # return_sequences = True, means the output of every time step to be shared with hidden next layer
    model.add(keras.layers.LSTM(units=30, activation = 'relu', return_sequences=True, input_shape= (x_train.shape[1], 1)))
    # Adding the Second Third hidden layer and the LSTM layer
    model.add(keras.layers.LSTM(units=30, return_sequences=False))
    model.add(keras.layers.Dense(n_forecast))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(x_train, y_train, batch_size=32, epochs=100,verbose=0 )

    # Create the testing data set
    # Create a new array containing scaled values from index 1543 to 2002
    test_data = scaled_close_data[training - n_lookback: , :]
    # Create the data sets x_test and y_test
    x_test = []
    y_test = close_data[training:, :]

    for i in range(n_lookback, len(test_data)):
        x_test.append(test_data[i-n_lookback:i, 0])

    # Convert the data to a numpy array
    x_test = np.array(x_test)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], n_features ))

    # Get the models predicted price values
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # data
    train = close_data_frame[:training]
    valid = close_data_frame[training:]
    valid['Predictions'] = predictions

    return close_data_frame,valid

def sql_connect(db_file):
    con_sql = None
    if os.path.exists(db_file):
        try:
            con_sql = sql.connect(db_file)
            return con_sql
        except sql.Error as db_err:
            print(db_err)

def sql_fetch(con):
    if con_sql:
        stock_list = []
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM quotes_stock')
        rows = cursorObj.fetchall()
        for row in rows:
            stock_list.append(row[1])
        return stock_list

def tr_stock(stock):
    if (len(stock)>= 6 ) and (stock[-3:]==".IS"):
        return True
    else:
        return False

def tr_stock_name(stock):
    if tr_stock(stock):
        return stock[:-3]
    else:
        return stock

# get name of the stock
data_base_file = "/home/csargin/stocks/db.sqlite3"
con_sql = sql_connect(data_base_file)
db_stock_list = sql_fetch(con_sql)
con_sql.close()

for stock_name in db_stock_list:
    close_data_frame,valid = forecast_stock_data(stock_name)
    export_chart_data(close_data_frame,valid,tr_stock_name(stock_name))
