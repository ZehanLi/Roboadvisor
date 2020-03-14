import tensorflow as tf
from keras.callbacks import CSVLogger,TensorBoard
from pandas import read_csv
from pandas import read_sql_query
import numpy as np
from sklearn.preprocessing import  MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation,LSTM, Dropout
from keras.optimizers import RMSprop
import time
import matplotlib.pyplot as plt
from src import Constants
import sqlite3
import datetime
import time
from src import TrainingSignals
from src import PersisterSqlite


class LSTMClasifier:
    TRAINING_PERIOD_IN_YEARS = 10


    def getTimeSeries(self, X_train, data_y_train, batch_size, timesteps, no_features, predict_col_index):
        dim_z = X_train.shape[0] - timesteps
        dim_x = timesteps
        dim_y = no_features
        X = np.zeros((dim_z, dim_x, dim_y))
        y = np.zeros((dim_z,))
        if dim_z < batch_size:
            X = np.zeros((batch_size, dim_x, dim_y))
            y = np.zeros((batch_size,))
            for i in range(batch_size):
                X[i] = X_train[0: timesteps]
                y[i] = data_y_train[timesteps-1]
            return X, y
        for i in range(dim_z):
            X[i] = X_train[i: timesteps + i]
            y[i] = data_y_train[timesteps + i]
        return X, y

    def getX_Y_Training_Test_Datasets(self, batch_size, data, no_features, predict_col_index, timesteps):
        data['test_signal'] = data['test_signal'].fillna('HOLD')
        # print (data[5:])
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_train = data.iloc[:, 1:6]
        data_train = data_train.replace({'test_signal': {'BUY': 1, 'SELL': 2, 'HOLD': 3}})
        df_train, df_test = train_test_split(data_train, train_size=0.8, test_size=0.2, shuffle=False)
        data_X_train = df_train.iloc[:, 0:4]
        data_y_train = df_train.loc[:, 'test_signal']
        data_X_test = df_test.iloc[:, 0:4]
        data_y_test = df_test.loc[:, 'test_signal']
        X_train = scaler.fit_transform(data_X_train)
        X_test = scaler.transform(data_X_test)
        X_timeseries, y_timeseries = self.getTimeSeries(X_train, data_y_train, batch_size, timesteps, no_features,
                                                        predict_col_index)
        X_test_timeseries, y_test_timeseries = self.getTimeSeries(X_test, data_y_test.reset_index(drop=True),
                                                                  batch_size, timesteps, no_features, predict_col_index)
        total_rows = X_timeseries.shape[0]
        dicard = total_rows % (batch_size * timesteps)
        data_size = total_rows - dicard
        X_t = X_timeseries[0:data_size]
        y_t = y_timeseries[0:data_size]
        test_total_rows = X_test_timeseries.shape[0]
        dicard = test_total_rows % (batch_size * timesteps )
        test_data_size = test_total_rows - dicard
        X_t_test = X_test_timeseries[0:test_data_size]
        y_t_test = y_test_timeseries[0:test_data_size]
        return X_t, X_t_test, y_t, y_t_test


    def learn(self, symbol_list):
        batch_size = 9
        timesteps = 21
        no_features = 4
        predict_col_index = 5
        for symbol in symbol_list:
            print("Training LSTM model for : " + symbol)
            #board=TensorBoard(log_dir=Constants.LSTM_TB_LOGDIR)
            tensorboard = TensorBoard(log_dir="C:\\temp\\blogs-3000")
            #NAME = "RoboAdvisor-LSTM-32-3*3-{}".format(int(time.time()))
            #tensorboard = TensorBoard(log_dir='./logs/{}'.format(NAME))
            TrainingSignals.retrieve_signals_basic(symbol, self.from_date, self.to_date, hold=True)

            DATA_SQL="select trade_date,close_price,RSI_rsi,MACD_macd_histogram,volume,test_signal from sp500_time_series_data where trade_date > ? and symbol=?"

            data=read_sql_query(sql=DATA_SQL, params=[self.from_date, symbol], con=self.conn)

            X_t, X_t_test, y_t, y_t_test = self.getX_Y_Training_Test_Datasets(batch_size, data, no_features,
                                                                              predict_col_index, timesteps)

            model=Sequential()
            model.add(LSTM(10, batch_input_shape=(batch_size, timesteps, 4), return_sequences=True, stateful=True))
            model.add(Dropout(0.4))
            model.add(LSTM(21, dropout=0.0))
            model.add(Dropout(0.4))
            model.add(Dense(batch_size, activation='sigmoid'))
            model.add(Dense(1, kernel_initializer='random_uniform', activation='linear'))
            model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
            #model.summary()
            class_weights = {1: 1,
                            2: 1,
                            3: 1}
            history = model.fit(X_t, y_t, epochs=10, verbose=2, batch_size=batch_size, class_weight=class_weights,
                                shuffle=False, callbacks=[tensorboard], validation_data=(X_t_test,y_t_test))

            p_pred=model.predict(X_t_test, batch_size=batch_size)
            #print(str(p_pred))
            print("Saving LSTM model for : " + symbol)
            mode_name = Constants.MODEL_DIR + "LSTM_" + symbol + Constants.MODEL_EXTENSION
            model.save(filepath=mode_name)
            #model.save_weights(filepath='./weights', overwrite=True)
            scores=model.evaluate(X_t_test, y_t_test, batch_size=batch_size)
            self.models[symbol]=model
            print("Score for symbol", str(scores))




    def classify(self, symbols):
        to_date = datetime.datetime.now()
        from_date = datetime.datetime.now() - datetime.timedelta(days=32)
        from_date=from_date.date()
        ret =[]
        sqllite = PersisterSqlite.PersisterSqlite()

        for symbol in symbols:
            DATA_SQL = "select trade_date,close_price,RSI_rsi,MACD_macd_histogram,volume,test_signal from sp500_time_series_data where trade_date > ? and symbol=?"

            data = read_sql_query(sql=DATA_SQL, params=[from_date, symbol], con=self.conn)

            data['test_signal'] = data['test_signal'].fillna('HOLD')
            # print (data[5:])
            scaler = MinMaxScaler(feature_range=(0, 1))
            data_train = data.iloc[:, 1:6]
            data_train = data_train.replace({'test_signal': {'BUY': 1, 'SELL': 2, 'HOLD': 3}})


            data_X_train = data_train.iloc[:, 0:4]
            data_y_train = data_train.loc[:, 'test_signal']


            X_train = scaler.fit_transform(data_X_train)

            X_timeseries, y_timeseries = self.getTimeSeries(X_train, data_y_train, 9, 21, 4,5)
            model=self.models[symbol]
            prediction =model.predict(X_timeseries, 9)

            if (prediction[0].round() <1.5):
                ret.append( self.categories[0].value)
                sqllite.insert_recommendation(
                    [symbol, Constants.LearningModel.LSTM_CLASIFICATION.value, self.categories[0].value])
            else:
                 ret.append(self.categories[1].value)
            sqllite.insert_recommendation(
                [symbol, Constants.LearningModel.LSTM_CLASIFICATION.value, self.categories[1].value])
        return ret



    def __init__(self, args):
        self.TRAINING_PERIOD_IN_YEAR=10
        self.conn = sqlite3.connect(Constants.DB_DIR)
        self.to_date = datetime.datetime.now() - datetime.timedelta(days=1)
        self.from_date = self.to_date - datetime.timedelta(days=365 * self.TRAINING_PERIOD_IN_YEARS)
        self.to_date = self.to_date.date()
        self.from_date = self.from_date.date()
        self.models={}
        self.categories = [Constants.Signal.BUY, Constants.Signal.SELL]



