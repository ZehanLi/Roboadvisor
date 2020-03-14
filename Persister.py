import mysql.connector
from time import time
from src.Utils import Utils


class Persister(object):
    aws_db = None
    insert_data_statement = None
    sql_table_suffix = "_time_series_data"

    def __init__(self):
        aws_host = Utils.read_properties().get('DATABASE','aws_host')
        aws_database = Utils.read_properties().get('DATABASE','aws_database')
        aws_user = Utils.read_properties().get('DATABASE','aws_user')
        aws_password = Utils.read_properties().get('DATABASE', 'aws_password')
        self.aws_db = mysql.connector.connect(host=aws_host, user=aws_user, passwd=aws_password, database=aws_database)
        self.insert_data_statement = "INSERT INTO {} (symbol, company_name, trade_date, " \
               "RSI_rsi, MACD_macd_signal, MACD_macd_histogram, MACD_macd," \
               "BB_real_upper_band, BB_real_middle_band, BB_real_lower_band, OBV_obv, open_price, low_price, high_price, close_price, volume) " \
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def insert(self, stmts):
        try:
            db_cursor = self.aws_db.cursor()
            for stmt in stmts:
                db_cursor.execute(stmt)
            self.aws_db.commit()
            self.aws_db.close()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            self.aws_db.rollback()

    def insert_data(self, data, symbol_map, exchange):
        try:
            db_cursor = self.aws_db.cursor()
            for symbol in data:
                market_data = data[symbol]
                insert_data = []
                market_data = market_data.dropna()
                start_time = time()
                print("Persisting data for symbol: " + symbol)
                for index, row in market_data.iterrows():
                    # Extract date from Python timestamp
                    date = index.date()
                    split_factor = float(row['4. close']) / float(row['5. adjusted close'])
                    market_data = (symbol, symbol_map[symbol], date, float(row['RSI']), float(row['MACD_Signal']), float(row['MACD_Hist']),
                                   float(row['MACD']), float(row['Real Lower Band']), float(row['Real Middle Band']),
                                   float(row['Real Lower Band']), float(row['OBV']), round(float(row['1. open']) / split_factor, 4), round(float(row['3. low']) / split_factor, 4), round(float(row['2. high']) / split_factor, 4), float(row['5. adjusted close']), int(row['6. volume']))
                    insert_data.append(market_data)
                db_cursor.executemany(self.insert_data_statement.format(exchange + self.sql_table_suffix), insert_data)
                self.aws_db.commit()
                end_time = time()
                print("Persisted data for symbol: " + symbol + " in ms: " + str(end_time - start_time))
            self.aws_db.close()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            self.aws_db.rollback()