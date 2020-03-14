from src import TrainingSignals
from src import Constants
import sqlite3
import pandas as pd
from datetime import date, timedelta, datetime
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from src import PersisterSqlite

class Random_Forest_Classifier:
    training_weeks = 52*2
    test_weeks = 8
    days_ahead = 1
    percent_change = 0
    delta = timedelta(weeks=training_weeks+test_weeks)
    models = {}
    classifications = {}

    def __init__(self, args):
        self.to_date =  date.today().strftime("%Y-%m-%d")
        self.from_date = (datetime.strptime(self.to_date, "%Y-%m-%d") - self.delta).date()
        self.args = args

    def learn(self, symbol_list):

        if self.args.mode == "test":
            print("Random Forest Training and Testing Accuracies per stock:")


        for symbol in symbol_list:
            signals = TrainingSignals.generate_rf_signals(ticker=symbol, start_date=self.from_date, end_date=self.to_date, days_ahead = self.days_ahead, percent_change = self.percent_change)
            conn = sqlite3.connect(Constants.DB_DIR)

            retrieve_stm = 'SELECT * ' \
                               'FROM sp500_time_series_data ' \
                               'WHERE trade_date >= ? AND trade_date <= ? ' \
                               'AND symbol == ?'

            selected_data = pd.read_sql_query(retrieve_stm, con = conn, params = (self.from_date, self.to_date, symbol,))
            selected_data = selected_data.drop(columns=['symbol', 'company_name', 'test_signal'])
            selected_data.drop(selected_data.tail(self.days_ahead).index,inplace=True)
            df = pd.DataFrame(signals, columns=['trade_date', 'Label'])
            selected_data['Label'] = df['Label']

            testing_cutoff = self.test_weeks*5
            data_train = selected_data[:-testing_cutoff]
            data_test = selected_data[-testing_cutoff:]
            x_train = data_train.drop(columns=['trade_date', 'Label'])
            y_train = data_train['Label']
            x_test = data_test.drop(columns=['trade_date', 'Label'])
            y_test = data_test['Label']

            # x_full_train = selected_data.drop(columns=['trade_date', 'Label'])
            # y_full_train = selected_data['Label']

            classifier_rf = RandomForestClassifier(max_features=7, min_samples_split=2, max_depth=7, criterion='gini')
            rf_parameters = {'n_estimators': [10, 50, 100],
                             'min_samples_leaf': [1, 3]}

            # run randomized search
            grid_search = GridSearchCV(classifier_rf, param_grid=rf_parameters, cv=10, iid=False)

            grid_search.fit(x_train, y_train)
            rf_training_pred = grid_search.predict(x_train)
            rf_training_acc = accuracy_score(y_train, rf_training_pred, normalize=True)

            rf_test_pred = grid_search.predict(x_test)
            rf_testing_acc = accuracy_score(y_test, rf_test_pred, normalize=True)

            if self.args.mode == "test":
                print(symbol)
                print("Training Accuracy: ", rf_training_acc)
                print("Testing Accuracy: ", rf_testing_acc)

                # train_buys = rf_training_pred[y_train[:] == 'buy'] == 'buy'
                # if(len(train_buys)>0):
                #     print("Training Sensitivity: ", 100*sum(train_buys)/len(train_buys), "%")
                #
                # test_buys = rf_test_pred[y_test[:] == 'buy'] == 'buy'
                # if(len(test_buys)>0):
                #     print("Testing Sensitivity: ", 100*sum(test_buys)/len(test_buys), "%")

            self.models[symbol] = grid_search

    def classify(self, symbol_list):

        for symbol in symbol_list:
            conn = sqlite3.connect(Constants.DB_DIR)
            retrieve_stm = 'SELECT * ' \
                           'FROM sp500_time_series_data ' \
                           'WHERE symbol == ?' \
                           'ORDER BY trade_date DESC ' \
                           'LIMIT 1'

            selected_data = pd.read_sql_query(retrieve_stm, con=conn, params=(symbol,))
            selected_data = selected_data.drop(columns=['symbol', 'company_name', 'trade_date', 'test_signal'])

            prediction = self.models[symbol].predict(selected_data)[0]
            if(prediction != "buy"):
                prediction = "no buy"
            sqllite = PersisterSqlite.PersisterSqlite()
            sqllite.insert_recommendation([symbol, Constants.LearningModel.DECISION_TREE_CLASSIFICATION.value, prediction])
