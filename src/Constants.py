import os
from enum import Enum


class Signal(Enum):
    BUY = 'buy';
    SELL = 'sell';
    HOLD = 'hold';


class TechnicalIndicatorType(Enum):
    RSI = 1;
    OBV = 2;
    BBAND = 3;
    MACD = 4;

class LearningModel(Enum):
    IMAGE_BASED_CLASSIFICATION = 1;
    DECISION_TREE_CLASSIFICATION = 2;
    LSTM_CLASIFICATION = 3;


BB_RealLowerBand = "RealLowerBand"
BB_RealUpperBand = "RealUpperBand"
BB_RealMiddleBand = "RealMiddleBand"
MACD = "MACD"
MACD_Histogram = "MACD_Hist"
MACD_Signal = "MACD_Signal"
RSI = "RSI"

Exchanges = ["sp500", "nyse", "nasdaq"]

SP500 = "sp500"

IMAGE_DIR = os.getcwd() + "/data/images/"
DB_DIR=os.getcwd() + "/data/db/trading.db"
MODEL_DIR=os.getcwd() + "/data/model/"
MODEL_EXTENSION=".h5"

LSTM_TB_LOGDIR = os.getcwd() + "/lstm_logs/"
