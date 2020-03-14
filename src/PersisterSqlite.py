from time import time
from src.Utils import Utils
from src import Constants
import sqlite3
import os


class PersisterSqlite(object):
    conn = None
    insert_data_statement = None
    insert_recommendation_sql = None

    def __init__(self):
        #self.conn = sqlite3.connect(Constants.DB_DIR)
        self.conn = sqlite3.connect(Constants.DB_DIR)
        self.insert_data_statement = "INSERT INTO sp500_time_series_data (symbol, company_name, trade_date, " \
        "RSI_rsi, MACD_macd_signal, MACD_macd_histogram, MACD_macd," \
        "BB_real_upper_band, BB_real_middle_band, BB_real_lower_band, OBV_obv,open_price, low_price, high_price, close_price, volume) " \
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        self.insert_recommendation_sql = "INSERT INTO recommendation(symbol, model_name, recommendation)" \
                                     "VALUES (?,?,?)"

    def insert_recommendation(self, row_values):
        self.insert_row(self.insert_recommendation_sql, row_values)

    def insert_row(self, sql_stmt, row_values):
        try:
            db_cursor = self.conn.cursor()
            db_cursor.execute(sql_stmt, row_values)
            self.conn.commit()
            #self.conn.close()
        except sqlite3.Error as err:
            print("Something went wrong: {}".format(err))
            self.conn.rollback()

    def insert(self, stmts):
        try:
            db_cursor = self.conn.cursor()
            for stmt in stmts:
                db_cursor.execute(stmt)
            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as err:
            print("Something went wrong: {}".format(err))
            self.conn.rollback()

    def insert_data(self, data, symbol_map):
        try:
            db_cursor = self.conn.cursor()
            for symbol in data:
                market_data = data[symbol]
                market_data = market_data.dropna()
                insert_data = []
                start_time = time()
                print("Persisting data for symbol: " + symbol)
                for index, row in market_data.iterrows():
                    date = index.date()
                    split_factor = float(row['4. close']) / float(row['5. adjusted close'])
                    insert_data.append([symbol, symbol_map[symbol], date, float(row['RSI']), float(row['MACD_Signal']), float(row['MACD_Hist']),
                                       float(row['MACD']), float(row['Real Upper Band']), float(row['Real Middle Band']),
                                       float(row['Real Lower Band']), float(row['OBV']), round(float(row['1. open']) / split_factor, 4),
                                       round(float(row['3. low']) / split_factor, 4), round(float(row['2. high']) / split_factor, 4), float(row['5. adjusted close']), int(row['6. volume'])])
                db_cursor.executemany(self.insert_data_statement, insert_data)
                self.conn.commit()
                end_time = time()
                print("Persisted data for symbol: " + symbol + " in ms: " + str(end_time - start_time))
            self.conn.close()
        except sqlite3.Error as err:
            print("Something went wrong: {}".format(err))
            self.conn.rollback()
