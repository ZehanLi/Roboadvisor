import sqlite3
import datetime
import matplotlib
import os
import shutil
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src import TrainingSignals
from src import Constants

def generate_buy_sell_images(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13", window = 20):
    signal_dates = TrainingSignals.retrieve_signals_basic(ticker, start_date, end_date, hold = False)

    # Based on https://arxiv.org/pdf/1907.10046.pdf I do not believe that the BB are included in the training images,
    # but will provide the ability to generate images with BB.
    include_BB_plot = False

    if (len(signal_dates[0]) == 0 and len(signal_dates[1]) == 0):
        print("No buy and sell dates found.")
        return 0

    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    delta = datetime.timedelta(weeks=6)
    adj_start = (start - delta).date()

    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()
    if (include_BB_plot):
        retrieve_stm = 'SELECT trade_date, close_price, BB_real_upper_band, BB_real_lower_band ' \
                       'FROM sp500_time_series_data ' \
                       'WHERE trade_date >= ? AND trade_date <= ? ' \
                       'AND symbol == ?'
    else:
        retrieve_stm = 'SELECT trade_date, close_price ' \
                        'FROM sp500_time_series_data ' \
                        'WHERE trade_date >= ? AND trade_date <= ? ' \
                        'AND symbol == ?'

    db_cursor.execute(retrieve_stm, (adj_start, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    if (len(selected_data) == 0):
        print("No results found. Please check inputs to function 'generate_buy_sell_images'")
        return []

    dirname = Constants.IMAGE_DIR + Constants.Signal.BUY.value + '/' + ticker + "/"
    if os.path.exists(dirname):
        shutil.rmtree(dirname)

    # Buy signals
    for day in signal_dates:
        index = [x[0] for x in selected_data].index(day[0])
        closing_values = []
        if (include_BB_plot):
            bb_upper = []
            bb_lower = []
        if (index >= window - 1):
            for i in range(1, window + 1, 1):
                selected_index = index - window + i
                closing_values.append(selected_data[selected_index][1])
                if (include_BB_plot):
                    bb_upper.append(selected_data[selected_index][2])
                    bb_lower.append(selected_data[selected_index][3])

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            filename = dirname + day[0] + '.png'
            fig = plt.figure(figsize=(6, 6))
            plt.axis('off')
            plt.plot(closing_values, 'b.-', linewidth=1)
            if (include_BB_plot):
                plt.plot(bb_upper, '--', color="black", linewidth=1)
                plt.plot(bb_lower, '--', color="black", linewidth=1)
            plt.savefig(filename, dpi=500, bbox_inches=0, pad_inches=0.0)
            plt.close('all')

    dirname = Constants.IMAGE_DIR + Constants.Signal.SELL.value + '/' + ticker + "/"
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    # Sell signals
    for day in signal_dates:
        index = [x[0] for x in selected_data].index(day[0])
        closing_values = []
        if (include_BB_plot):
            bb_upper = []
            bb_lower = []
        if (index >= window +1):
            for i in range(1, window + 1, 1):
                selected_index = index - window + i
                closing_values.append(selected_data[selected_index][1])
                if (include_BB_plot):
                    bb_upper.append(selected_data[selected_index][2])
                    bb_lower.append(selected_data[selected_index][3])



            if not os.path.exists(dirname):
                os.makedirs(dirname)
            filename = dirname + day[0] + '.png'
            fig = plt.figure(figsize=(6, 6))
            plt.axis('off')
            plt.plot(closing_values, 'b.-', linewidth=1)
            if (include_BB_plot):
                plt.plot(bb_upper, '--', color="black", linewidth=1)
                plt.plot(bb_lower, '--', color="black", linewidth=1)
            plt.savefig(filename, dpi=500, bbox_inches=0, pad_inches=0.0)
            plt.close('all')
    # plt.savefig('../data/buy/filename.png', dpi=5, bbox_inches=0, pad_inches=0.1) # 30 x 30 image
    # Can go higher resolution by setting dpi to a higher value but impacts real time significantly

def generate_buy_sell_hold_images(ticker ="AMZN", start_date ="2014-10-13", end_date ="2014-12-13", window = 20):
    # Based on https://arxiv.org/pdf/1907.10046.pdf I do not believe that the BB are included in the training images,
    # but will provide the ability to generate images with BB.
    include_BB_plot = False

    # Expected format of signal_dates: List of 2 element lists: [[trade_date1, signal1], [trade_date2, signal2], ...]
    signal_dates = TrainingSignals.retrieve_signals_basic(ticker, start_date, end_date, hold = True)

    # Check to make sure a response was returned from retrieve_signals_basic
    if (len(signal_dates[0]) == 0):
        print("No buy, sell, or hold dates found.")
        return 0

    # create adj_start variable to make sure we retrieve data earlier than our first date since we will be plotting 20 days before our first date
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    # Not a rigorous formula. Just going a bit past "window" for holidays and weekends
    delta = datetime.timedelta(days=window*1.5+5)
    adj_start = (start - delta).date()

    # connect to our database
    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()
    if (include_BB_plot):
        retrieve_stm = 'SELECT trade_date, close_price, BB_real_upper_band, BB_real_lower_band ' \
                       'FROM sp500_time_series_data ' \
                       'WHERE trade_date >= ? AND trade_date <= ? ' \
                       'AND symbol == ?'
    else:
        retrieve_stm = 'SELECT trade_date, close_price ' \
                        'FROM sp500_time_series_data ' \
                        'WHERE trade_date >= ? AND trade_date <= ? ' \
                        'AND symbol == ?'

    # retrieve data from database spanning timeframe selected into variable "selected_data"
    db_cursor.execute(retrieve_stm, (adj_start, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    # Sanity check. Make sure some dates are returned.
    if (len(selected_data) == 0):
        print("No results found. Please check inputs to function 'generate_buy_sell_images'")
        return []


    # Generate the three needed directories: buy, sell, hold
    signal_types = [Constants.Signal.BUY.value, Constants.Signal.SELL.value, Constants.Signal.HOLD.value]
    for element in signal_types:
        dirname = Constants.IMAGE_DIR + element + '/' + ticker + "/"
        # If corresponding directory already exists, remove it
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        # If corresponding directory does not exist, create it
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    # Generate an image per day
    for day in signal_dates:
        index = [x[0] for x in selected_data].index(day[0])
        closing_values = []
        if (include_BB_plot):
            bb_upper = []
            bb_lower = []
        if (index >= window - 1):
            for i in range(1, window + 1, 1):
                selected_index = index - window + i
                closing_values.append(selected_data[selected_index][1])
                if (include_BB_plot):
                    bb_upper.append(selected_data[selected_index][2])
                    bb_lower.append(selected_data[selected_index][3])

            # Choose directory based on signal type
            if(day[1] == "buy"):
                dirname = Constants.IMAGE_DIR + Constants.Signal.BUY.value + '/' + ticker + "/"
            elif(day[1] == "sell"):
                dirname = Constants.IMAGE_DIR + Constants.Signal.SELL.value + '/' + ticker + "/"
            else: # hold
                dirname = Constants.IMAGE_DIR + Constants.Signal.HOLD.value + '/' + ticker + "/"

            filename = dirname + day[0] + '.png'
            fig = plt.figure(figsize=(6, 6))
            plt.axis('off')
            plt.plot(closing_values, 'b.-', linewidth=1)
            if (include_BB_plot):
                plt.plot(bb_upper, '--', color="black", linewidth=1)
                plt.plot(bb_lower, '--', color="black", linewidth=1)
            plt.savefig(filename, dpi=500, bbox_inches=0, pad_inches=0.0)
            plt.close('all')

# Able to generate an image with all closing dates from start_date to end_date for each supplied ticker in ticker_list.
def generate_one_image(ticker_list = ["AMZN", "AAPL"], start_date = "2014-10-13", end_date = "2014-12-13"):
    # Based on https://arxiv.org/pdf/1907.10046.pdf I do not believe that the BB are included in the training images,
    # but will provide the ability to generate images with BB.
    include_BB_plot = False

    # connect to our database
    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()
    if (include_BB_plot):
        retrieve_stm = 'SELECT trade_date, close_price, BB_real_upper_band, BB_real_lower_band ' \
                       'FROM sp500_time_series_data ' \
                       'WHERE trade_date >= ? AND trade_date <= ? ' \
                       'AND symbol == ?'
    else:
        retrieve_stm = 'SELECT trade_date, close_price ' \
                        'FROM sp500_time_series_data ' \
                        'WHERE trade_date >= ? AND trade_date <= ? ' \
                        'AND symbol == ?'

    for ticker in ticker_list:
        # retrieve data from database spanning timeframe selected into variable "selected_data"
        db_cursor.execute(retrieve_stm, (start_date, end_date, ticker,))
        selected_data = list(db_cursor.fetchall())

        # Sanity check. Make sure some dates are returned.
        if (len(selected_data) == 0):
            print("No results found. Please check inputs to function 'generate_buy_sell_images'")
            return []

        # Generate the individual directories: buy, sell, hold
        dirname = Constants.IMAGE_DIR + "individual" + '/' + ticker + "/"
        # If corresponding directory already exists, remove it
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        # If corresponding directory does not exist, create it
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Generate the image
        closing_values = []
        if (include_BB_plot):
            bb_upper = []
            bb_lower = []
        for day in selected_data:
            closing_values.append(day[1])
            if (include_BB_plot):
                bb_upper.append(day[2])
                bb_lower.append(day[3])

        filename = dirname + day[0] + '.png'
        fig = plt.figure(figsize=(6, 6))
        plt.axis('off')
        plt.plot(closing_values, 'b.-', linewidth=1)
        if (include_BB_plot):
            plt.plot(bb_upper, '--', color="black", linewidth=1)
            plt.plot(bb_lower, '--', color="black", linewidth=1)
        plt.savefig(filename, dpi=500, bbox_inches=0, pad_inches=0.0)
        plt.close('all')

# Able to generate an image with all closing dates from start_date to end_date for each supplied ticker in ticker_list.
def create_single_image(ticker, start_date="2014-10-13", end_date="2014-12-13"):
    # Based on https://arxiv.org/pdf/1907.10046.pdf I do not believe that the BB are included in the training images,
    # but will provide the ability to generate images with BB.
    include_BB_plot = False

    # connect to our database
    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()
    if (include_BB_plot):
        retrieve_stm = 'SELECT trade_date, close_price, BB_real_upper_band, BB_real_lower_band ' \
                       'FROM sp500_time_series_data ' \
                       'WHERE trade_date >= ? AND trade_date <= ? ' \
                       'AND symbol == ?'
    else:
        retrieve_stm = 'SELECT trade_date, close_price ' \
                       'FROM sp500_time_series_data ' \
                       'WHERE trade_date >= ? AND trade_date <= ? ' \
                       'AND symbol == ?'

    # retrieve data from database spanning timeframe selected into variable "selected_data"
    db_cursor.execute(retrieve_stm, (start_date, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    # Sanity check. Make sure some dates are returned.
    if (len(selected_data) == 0):
        print("No results found. Please check inputs to function 'generate_buy_sell_images'")
        return []

    # Generate the individual directories: buy, sell, hold
    dirname = Constants.IMAGE_DIR + "individual" + '/' + ticker + "/"
    # If corresponding directory already exists, remove it
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    # If corresponding directory does not exist, create it
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # Generate the image
    closing_values = []
    if (include_BB_plot):
        bb_upper = []
        bb_lower = []
    for day in selected_data:
        closing_values.append(day[1])
        if (include_BB_plot):
            bb_upper.append(day[2])
            bb_lower.append(day[3])

    filename = dirname + str(end_date) + '.png'
    fig = plt.figure(figsize=(6, 6))
    plt.axis('off')
    plt.plot(closing_values, 'b.-', linewidth=1)
    if (include_BB_plot):
        plt.plot(bb_upper, '--', color="black", linewidth=1)
        plt.plot(bb_lower, '--', color="black", linewidth=1)
    plt.savefig(filename, dpi=500, bbox_inches=0, pad_inches=0.0)
    plt.close('all')
