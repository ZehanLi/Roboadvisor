from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from src import Constants
from time import time, sleep
import pandas as pd

class AlphaVantage:
    calls = 0
    calls_allowed = 120

    def call_av(self, tech_indicator_type, tech_indicators, symbol, config):
        self.calls += 1
        if self.calls % self.calls_allowed == 0:
            print("Going to sleep for 1 minute after: " + str(self.calls) + " calls to AV made..")
            self.calls = 0
            sleep(60)
        try:
            if Constants.TechnicalIndicatorType.RSI == tech_indicator_type:
                print("Check RSI for symbol: " + symbol)
                data, meta_data = tech_indicators.get_rsi(symbol, config.get('RSI', 'interval'),
                            config.get('RSI', 'time_period'), config.get('RSI', 'series_type'))
                return data, meta_data
            elif Constants.TechnicalIndicatorType.OBV == tech_indicator_type:
                print("Check OBV for symbol: " + symbol)
                data, meta_data = tech_indicators.get_obv(symbol, config.get('OBV', 'interval'))
                return data, meta_data
            elif Constants.TechnicalIndicatorType.MACD == tech_indicator_type:
                print("Check MACD for symbol: " + symbol)
                data, meta_data = tech_indicators.get_macd(symbol, config.get('MACD', 'interval'),
                                                           config.get('MACD', 'series_type'),
                                                           config.get('MACD', 'fast_period'),
                                                           config.get('MACD', 'slow_period'),
                                                           config.get('MACD', 'signal_period'),)
                return data, meta_data
            elif Constants.TechnicalIndicatorType.BBAND == tech_indicator_type:
                print("Check BBAND for symbol: " + symbol)
                data, meta_data = tech_indicators.get_bbands(symbol, config.get('BBANDS', 'interval'),
                                                             config.get('BBANDS', 'time_period'),
                                                           config.get('BBANDS', 'series_type'),
                                                           config.get('BBANDS', 'nbdevup'),
                                                           config.get('BBANDS', 'nbdevdn'),
                                                           config.get('BBANDS', 'matype'),)
                return data, meta_data
            else:
                print("Invalid Indicator Type")
                return pd.DataFrame(), pd.DataFrame()
        except Exception as e:
            print(str(e) + " while fetching Technical Indicators for symbol: " + symbol)
            return pd.DataFrame(), pd.DataFrame()

    def call_av_time_series(self, ts, symbol, config):
        self.calls += 1
        if self.calls % self.calls_allowed == 0:
            print("Going to sleep for 1 minute after: " + str(self.calls) + " calls to AV made..")
            self.calls = 0
            sleep(60)
        try:
            print("Getting TS data for symbol: " + symbol)
            data, meta_data = ts.get_daily_adjusted(symbol, config.get('TIMESERIES', 'outputsize'))
            return data, meta_data
        except Exception as e:
            print(str(e) + " while fetching TS for symbol: " + symbol)
            return pd.DataFrame(), pd.DataFrame()