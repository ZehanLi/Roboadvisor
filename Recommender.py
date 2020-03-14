from src import Constants
from src.ImageBasedClassifier import ImageBasedClassifier
from src.LSTMClasifier import LSTMClasifier
from src.RandomForestClassifier import Random_Forest_Classifier

import matplotlib
matplotlib.use('Agg')

class Recommender:
    ibc = None
    symbols = []

    def __init__(self, args, symbols, init=True):
        if init:
            #self.ibc = ImageBasedClassifier(args)
            #self.ibc.learn(symbols)
            self.lstm = LSTMClasifier(args)
            self.lstm.learn(symbols)
            #self.rfc = Random_Forest_Classifier(args)
            #self.rfc.learn(symbols)

    def generate_recommendation(self, type, symbols):
        if type == Constants.LearningModel.IMAGE_BASED_CLASSIFICATION:
            return self.image_based_classification(symbols)
        elif type == Constants.LearningModel.DECISION_TREE_CLASSIFICATION:
            return self.random_forest_classification(symbols)
        elif type == Constants.LearningModel.LSTM_CLASIFICATION:
            return self.lstm.classify(symbols);


    def image_based_classification(self, symbols):
        # TODO Add code to return recommended trading signal
        self.ibc.classify(symbols)

    def random_forest_classification(self, symbols):
        # classifies the symbols with the stored classification in a dict: self.classifications
        self.rfc.classify(symbols)
