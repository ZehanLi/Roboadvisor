from src import GenerateImages
from src import GenerateImagesNoHold
from src import Constants
import datetime
import time
import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import  Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard,ModelCheckpoint,EarlyStopping, LearningRateScheduler
from tensorboard.plugins.hparams import api as hp
from sklearn.model_selection import train_test_split
import pickle

from src import PersisterSqlite

class ImageBasedClassifier:
    TRAINING_PERIOD_IN_YEARS = None
    # This seems to be pretty decent image size. We will modify based on the performance
    IMG_SIZE = 50
    from_date = None
    to_date = None
    categories = []
    args = None
    X_train = None
    X_test = None
    y_train = None
    y_test = None
    EPOCHS=50

    loss_object = tf.keras.losses.BinaryCrossentropy()
    optimizer = tf.keras.optimizers.Adam()

    train_loss = tf.keras.metrics.Mean('train_loss', dtype=tf.float32)
    train_accuracy = tf.keras.metrics.BinaryAccuracy('train_accuracy')
    test_loss = tf.keras.metrics.Mean('test_loss', dtype=tf.float32)
    test_accuracy = tf.keras.metrics.BinaryAccuracy('test_accuracy')

    # Hyper parameter tuning
    HP_NUM_UNITS = hp.HParam('num_units', hp.Discrete([16, 32, 64, 128]))
    HP_DROPOUT = hp.HParam('dropout', hp.RealInterval(0.0, 0.6))
    HP_OPTIMIZER = hp.HParam('optimizer', hp.Discrete(['adam', 'sgd', 'rmsprop']))
    HP_ACTIVATION = hp.HParam('activation', hp.Discrete(['relu', 'tanh']))

    hparams = [HP_NUM_UNITS, HP_DROPOUT, HP_OPTIMIZER, HP_ACTIVATION]

    METRIC_ACCURACY = 'accuracy'

    #NAME = "RoboAdvisor-CNN-32-3*3-{}".format(int(time.time()))
    NAME=''
    tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))
    early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=0,
                                   mode='auto', baseline=None, restore_best_weights=0)
    def __init__(self, args):
        self.args = args
        self.TRAINING_PERIOD_IN_YEARS = int(self.args.training_period)
        self.to_date = datetime.datetime.now() - datetime.timedelta(days=20)
        self.from_date = self.to_date - datetime.timedelta(days=365*self.TRAINING_PERIOD_IN_YEARS)
        self.to_date = self.to_date.date()
        self.from_date = self.from_date.date()
        self.categories = [Constants.Signal.BUY, Constants.Signal.SELL]

    def learn(self, symbol_list):
        if self.args.image == "generate":
            for symbol in symbol_list:
                start_time = time.time()
                print("Starting to generate images for: ", symbol)
                GenerateImagesNoHold.generate_buy_sell_images(symbol, str(self.from_date), str(self.to_date))
                end_time = time.time()
                print("Generated images for stocks: ", symbol, " in: ", (end_time - start_time), " seconds")

        training_data = []
        for symbol in symbol_list:
            for category in self.categories:
                path = os.path.join(Constants.IMAGE_DIR, category.value + "/" + symbol)
                class_num = self.categories.index(category)
                for img in os.listdir(path):
                    try:
                        img_arr = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                        resized_arr = cv2.resize(img_arr, (self.IMG_SIZE, self.IMG_SIZE))
                        training_data.append([resized_arr, class_num])
                    except Exception as e:
                        print(e)
            random.shuffle(training_data)
            X = []
            y = []
            for features, labels in training_data:
                X.append(features)
                y.append(labels)

            X = np.array(X).reshape(-1, self.IMG_SIZE, self.IMG_SIZE, 1)
            y = np.array(y)

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=.3)

            self.X_train = self.X_train/255.0

            model = Sequential()
            model.add(Conv2D(128, (3,3), input_shape = X.shape[1:]))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(pool_size=(2,2)))

            model.add(Conv2D(128, (3, 3)))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(pool_size=(2, 2)))

            model.add(Conv2D(128, (3, 3)))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(pool_size=(2, 2)))

            model.add(Flatten())
            model.add(Dense(32))
            model.add(Activation("relu"))

            model.add(Dense(1))
            model.add(Activation('sigmoid'))

            model.compile(loss="binary_crossentropy",
                          optimizer="rmsprop",
                          metrics=['accuracy'],)
            model_save_path = Constants.MODEL_DIR + symbol + Constants.MODEL_EXTENSION
            model_cp = ModelCheckpoint(model_save_path, monitor='val_loss', verbose=0, save_best_only=True,
                                       save_weights_only=False, mode='auto', period=1)

            lr_callback = LearningRateScheduler(self.lr_schedule)
            model.fit(self.X_train, self.y_train, batch_size=16, epochs = self.EPOCHS, validation_split=0.2,
                      callbacks=[self.tensorboard, model_cp, self.early_stopping])

            val_loss, val_acc = model.evaluate(self.X_test, self.y_test)
            print('Accuracy for ',symbol, ": ", val_loss, val_acc)

            model.save(model_save_path)
            accuracy = False
            if accuracy:
                # TENSORBOARD CODE
                train_dataset = tf.data.Dataset.from_tensor_slices((self.X_train, self.y_train/1.0))
                test_dataset = tf.data.Dataset.from_tensor_slices((self.X_test/255.0, self.y_test/1.0))

                train_dataset = train_dataset.shuffle(60000).batch(64)
                test_dataset = test_dataset.batch(64)

                current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                train_summary_writer = tf.summary.create_file_writer('logs/{}'.format(self.NAME) + '/train')
                test_summary_writer = tf.summary.create_file_writer('logs/{}'.format(self.NAME) + '/test')

                for epoch in range(self.EPOCHS):
                    for (x_train, y_train) in train_dataset:
                        self.train_step(model, self.optimizer, x_train, y_train)
                    with train_summary_writer.as_default():
                        tf.summary.scalar('loss', self.train_loss.result(), step=epoch)
                        tf.summary.scalar('accuracy', self.train_accuracy.result(), step=epoch)

                    for (x_test, y_test) in test_dataset:
                        self.test_step(model, x_test, y_test)
                    with test_summary_writer.as_default():
                        tf.summary.scalar('loss', self.test_loss.result(), step=epoch)
                        tf.summary.scalar('accuracy', self.test_accuracy.result(), step=epoch)

                    template = 'Epoch {}, Loss: {}, Accuracy: {}, Test Loss: {}, Test Accuracy: {}'
                    print(template.format(epoch + 1,
                                          self.train_loss.result(),
                                          self.train_accuracy.result() * 100,
                                          self.test_loss.result(),
                                          self.test_accuracy.result() * 100))

                    # Reset metrics every epoch
                    self.train_loss.reset_states()
                    self.test_loss.reset_states()
                    self.train_accuracy.reset_states()
                    self.test_accuracy.reset_states()

            tuning = False
            if tuning:
                with tf.summary.create_file_writer('logs/hparam_tuning').as_default():
                    hp.hparams_config(
                        hparams=[self.HP_NUM_UNITS, self.HP_DROPOUT, self.HP_OPTIMIZER, self.HP_ACTIVATION],
                        metrics=[hp.Metric(self.METRIC_ACCURACY, display_name='Accuracy')],
                    )

                session_num = 0

                for num_units in self.HP_NUM_UNITS.domain.values:
                    for dropout_rate in (self.HP_DROPOUT.domain.min_value, self.HP_DROPOUT.domain.max_value):
                        for optimizer in self.HP_OPTIMIZER.domain.values:
                            for activation in self.HP_ACTIVATION.domain.values:
                                hparams = {
                                    self.HP_NUM_UNITS: num_units,
                                    self.HP_DROPOUT: dropout_rate,
                                    self.HP_OPTIMIZER: optimizer,
                                    self.HP_ACTIVATION:activation
                                }
                                run_name = "run-%d" % session_num
                                print('--- Starting trial: %s' % run_name)
                                print({h.name: hparams[h] for h in hparams})
                                self.run('logs/hparam_tuning/' + run_name, hparams)
                                session_num += 1

    def train_test_model(self, hparams):
        model = Sequential()
        model.add(Conv2D(hparams[self.HP_NUM_UNITS], (3, 3), input_shape=(self.IMG_SIZE, self.IMG_SIZE, 1)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(hparams[self.HP_DROPOUT]))

        model.add(Conv2D(hparams[self.HP_NUM_UNITS], (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(hparams[self.HP_DROPOUT]))

        model.add(Conv2D(hparams[self.HP_NUM_UNITS], (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(hparams[self.HP_DROPOUT]))

        model.add(Flatten())
        model.add(Dense(hparams[self.HP_NUM_UNITS]))
        model.add(Activation("relu"))
        model.add(Dropout(hparams[self.HP_DROPOUT]))

        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        model.compile(
            optimizer=hparams[self.HP_OPTIMIZER],
            loss='binary_crossentropy',
            metrics=['accuracy'],
        )

        model.fit(self.X_train, self.y_train, epochs=self.EPOCHS, validation_split=0.2,
                  callbacks = [ self.early_stopping, hp.KerasCallback('logs/{}'.format(self.NAME), hparams)])  # Run with 1 epoch to speed things up for demo purposes
        _, accuracy = model.evaluate(self.X_test, self.y_test)
        return accuracy

    def train_step(self, model, optimizer, x_train, y_train):
        with tf.GradientTape() as tape:
            predictions = model(x_train, training=True)
            loss = self.loss_object(y_train, predictions)
        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        self.train_loss(loss)
        self.train_accuracy(y_train, predictions)

    def test_step(self, model, x_test, y_test):
        predictions = model(x_test)
        loss = self.loss_object(y_test, predictions)

        self.test_loss(loss)
        self.test_accuracy(y_test, predictions)

    def lr_schedule(self, epoch):
        """
        Returns a custom learning rate that decreases as epochs progress.
        """
        learning_rate = 0.2
        if epoch > 10:
            learning_rate = 0.02
        if epoch > 20:
                learning_rate = 0.01
        if epoch > 30:
            learning_rate = 0.005

        tf.summary.scalar('learning rate', data=learning_rate, step=epoch)
        return learning_rate

    def run(self, run_dir, hparams):
        with tf.summary.create_file_writer(run_dir).as_default():
            hp.hparams(hparams)  # record the values used in this trial
            accuracy = self.train_test_model(hparams)
            tf.summary.scalar(self.METRIC_ACCURACY, accuracy, step=1)

    def classify(self, symbols):
        to_date = datetime.datetime.now()
        from_date = datetime.datetime.now() - datetime.timedelta(days=20)
        for symbol in symbols:
            print('Calculating recommendation for symbol: ', symbol)
            GenerateImages.create_single_image(symbol, from_date.date(), to_date.date())
            path = os.path.join(Constants.IMAGE_DIR, "individual" + '/' + symbol + "/")
            img_arr = cv2.imread(os.path.join(path, str(to_date.date()) + ".png"), cv2.IMREAD_GRAYSCALE)
            img_arr = cv2.resize(img_arr, (self.IMG_SIZE, self.IMG_SIZE))
            img_arr = np.reshape(img_arr, [-1, self.IMG_SIZE, self.IMG_SIZE, 1])
            img_arr = img_arr / 255.0
            model = load_model(Constants.MODEL_DIR + symbol + Constants.MODEL_EXTENSION)
            prediction = model.predict_classes(img_arr)
            signal = self.categories[prediction[0][0]]
            sqllite = PersisterSqlite.PersisterSqlite()
            sqllite.insert_recommendation([symbol, Constants.LearningModel.IMAGE_BASED_CLASSIFICATION.value, signal.value])

