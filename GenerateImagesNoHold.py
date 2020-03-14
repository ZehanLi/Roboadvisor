import sqlite3
import datetime
import matplotlib
import os
import shutil
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src import TrainingSignalsNoHold
from src import Constants

def generate_buy_sell_images(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13", window = 20):
    signal_dates = TrainingSignalsNoHold.retrieve_signals_basic(ticker, start_date, end_date)

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
    for day in signal_dates[0]:
        index = [x[0] for x in selected_data].index(day)
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

            filename = dirname + day + '.png'
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
    for day in signal_dates[1]:
        index = [x[0] for x in selected_data].index(day)
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
            filename = dirname + day + '.png'
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
