from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from src import Constants
from src import AlphaV
from src.Persister import Persister
from src.PersisterSqlite import PersisterSqlite
from src.Utils import Utils
from src.Scraper import Scraper
from src.Recommender import Recommender
from time import time
import os
import argparse
import matplotlib
matplotlib.use('Agg')


class PortfolioManager:
    def main(self):
        print("Portfolio Manager started")
        parser = argparse.ArgumentParser()
        parser.add_argument('-database', action='store', dest='database',
                            help='Either of Sqlite/AWS')
        parser.add_argument('-mode', action='store', dest='mode',
                            help='Test Mode[test/real]')
        parser.add_argument('-image', action='store', dest='image',
                            help='Generate Images[generate]')
        parser.add_argument('-model', action='store', dest='model',
                            help='create machine learning model[create]')
        parser.add_argument('-training_period', action='store', dest='training_period',
                            help='Training period in years')
        self.args = parser.parse_args()
        scraper = Scraper()
        config = Utils.read_properties()
        av = AlphaV.AlphaVantage()
        ti = TechIndicators(key=os.environ["ALPHA_VANTAGE_KEY"], output_format='pandas')
        ts = TimeSeries(key=os.environ["ALPHA_VANTAGE_KEY"], output_format='pandas')
        if self.args.mode == 'test':
            symbol_list = scraper.read_symbols()
        else:
            symbol_list = self.get_exchange_symbol_list(Constants.SP500, scraper)
        if self.args.database == 'sqllite':
            self.dump_market_data(symbol_list, Constants.SP500, av, ti, ts, config)
        elif self.args.database == 'AWS':
            for exchange in Constants.Exchanges:
                symbol_list = self.get_exchange_symbol_list(exchange, scraper)
                self.dump_market_data(symbol_list, exchange, av, ti, ts, config)

        if self.args.model == 'create':
            recommender = Recommender(self.args, symbol_list, True)
        else:
            recommender = Recommender(self.args, symbol_list, False)
        #recommender.generate_recommendation(Constants.LearningModel.IMAGE_BASED_CLASSIFICATION, symbol_list)
        #recommender.generate_recommendation(Constants.LearningModel.DECISION_TREE_CLASSIFICATION, symbol_list)
        recommender.generate_recommendation(Constants.LearningModel.LSTM_CLASIFICATION, symbol_list)





    def get_exchange_symbol_list(self, exchange, scraper):
        print("Loading " + exchange + " stocks..")
        symbol_list = {}
        if exchange == Constants.SP500:
            symbol_list = scraper.get_sp500_symbols()
        else:
            symbol_list = scraper.get_exchange_symbols(exchange)
        print("Loaded " + exchange + " stocks..")
        return symbol_list

    def dump_market_data(self, symbol_list, exchange, av, ti, ts, config):
        start_time = time()
        symbol_ts = {}
        for symbol in symbol_list:
            # Fetch Technical indicators data
            rsi_wide_data, rsi_meta_data = av.call_av(Constants.TechnicalIndicatorType.RSI, ti, symbol, config)
            obv_wide_data, obv_meta_data = av.call_av(Constants.TechnicalIndicatorType.OBV, ti, symbol, config)
            bbands_wide_data, bbands_meta_data = av.call_av(Constants.TechnicalIndicatorType.BBAND, ti, symbol, config)
            macd_wide_data, macd_meta_data = av.call_av(Constants.TechnicalIndicatorType.MACD, ti, symbol, config)

            # Fetch TS data
            ts_data, ts_meta_data = av.call_av_time_series(ts, symbol, config)
            if not rsi_wide_data.empty and not obv_wide_data.empty and not bbands_wide_data.empty and not macd_wide_data.empty and not ts_data.empty:
                joinedData = rsi_wide_data.join(obv_wide_data).join(bbands_wide_data).join(macd_wide_data).join(ts_data);
                symbol_ts[symbol] = joinedData

        end_time = time()
        print("Time Elapsed in fetching technical indicators and time series data for exchange [ " + exchange + " ]: " + str(end_time - start_time))
        start_time = time()
        if self.args.database == 'sqllite':
            persister = PersisterSqlite()
            persister.insert_data(symbol_ts, symbol_list)
        else:
            persister = Persister()
            persister.insert_data(symbol_ts, symbol_list, exchange)

        end_time = time()
        print("Time Elapsed in inserting technical indicators and time series data exchange [ " + exchange + " ]: " + str(end_time - start_time))

    def generate_signal(self, symbol_tis):
        for symbol in symbol_tis:
            signal, rsi_value = self.scan_rsi_indicator(symbol_tis[symbol])
            self.print_signal(self, signal, rsi_value, symbol)

    @staticmethod
    def print_signal(self, signal, rsi_value, stock):
        if signal == Constants.Signal.BUY:
            print("BUY Signal generated for: " + stock + ". RSI Value: " + str(rsi_value))
        elif signal == Constants.Signal.SELL:
            print("SELL Signal generated for: " + stock + ". RSI Value: " + str(rsi_value))


if __name__ == "__main__":
    portfolio_manager = PortfolioManager()
    portfolio_manager.main()