import sqlite3
from math import copysign
from src import Constants

# Simply looks for MACD crossover and then checks over the previous week of trading for the day with the:
# highest stock price if selling or
# lowest stock price if buying
# and appends this date to the appropriate list.
# Format of output: [list of buy dates, list of sell dates] in the form [YYYY-MM-DD]
def retrieve_signals_basic(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13"):
    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()

    retrieve_stm = 'SELECT trade_date, close_price, RSI_rsi, MACD_macd_histogram ' \
                   'FROM sp500_time_series_data ' \
                   'WHERE trade_date >= ? AND trade_date <= ? ' \
                   'AND symbol == ?'

    db_cursor.execute(retrieve_stm, (start_date, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    if(len(selected_data) == 0):
        print("No results found. Please check inputs to function 'retrieve_signals_basic'")
        return []

    buy_dates = []
    sell_dates = []
    hist_sign = 0

    for counter, day in enumerate(selected_data):
        temp_sign = copysign(1,day[3])
        if(hist_sign == 1 and temp_sign == -1):
            start_index = max(0, counter - 5)
            temp_date = day
            while start_index <= counter:
                if(selected_data[start_index][1] > temp_date[1]):
                    temp_date = selected_data[start_index]
                start_index = start_index + 1
            if(temp_date[0] != sell_dates[-1:]):
                sell_dates.append(temp_date[0])
        if(hist_sign == -1 and temp_sign == 1):
            start_index = max(0, counter - 5)
            temp_date = day
            while start_index <= counter:
                if(selected_data[start_index][1] < temp_date[1]):
                    temp_date = selected_data[start_index]
                start_index = start_index + 1
            if(temp_date[0] != buy_dates[-1:]):
                buy_dates.append(temp_date[0])
        hist_sign = temp_sign

    output = [buy_dates, sell_dates]
    return output

#similar to basic, but requires particular RSI levels at time of buy or sell date)
# to buy, the RSI of the recommended date needs to be beneath 40
# to sell, the RSI of the recommended date needs to be above 60
def retrieve_signals_mid(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13"):
    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()

    retrieve_stm = 'SELECT trade_date, close_price, RSI_rsi, MACD_macd_histogram ' \
                   'FROM sp500_time_series_data ' \
                   'WHERE trade_date >= ? AND trade_date <= ? ' \
                   'AND symbol == ?'

    db_cursor.execute(retrieve_stm, (start_date, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    if(len(selected_data) == 0):
        print("No results found. Please check inputs to function 'retrieve_signals_mid'")
        return []

    buy_dates = []
    sell_dates = []
    hist_sign = 0

    for counter, day in enumerate(selected_data):
        temp_sign = copysign(1,day[3])
        if(hist_sign == 1 and temp_sign == -1):
            start_index = max(0, counter - 5)
            temp_date = day
            while start_index <= counter:
                if(selected_data[start_index][1] > temp_date[1]):
                    temp_date = selected_data[start_index]
                start_index = start_index + 1
            if(temp_date[0] != sell_dates[-1:] and temp_date[2]>= 60):
                sell_dates.append(temp_date[0])
        if(hist_sign == -1 and temp_sign == 1):
            start_index = max(0, counter - 5)
            temp_date = day
            while start_index <= counter:
                if(selected_data[start_index][1] < temp_date[1]):
                    temp_date = selected_data[start_index]
                start_index = start_index + 1
            if(temp_date[0] != buy_dates[-1:] and temp_date[2] <= 40):
                buy_dates.append(temp_date[0])
        hist_sign = temp_sign

    output = [buy_dates, sell_dates]
    return output

#similar to mid, but requires stricter RSI levels at time of buy or sell date)
# to buy, the RSI of the recommended date needs to be beneath 30
# to sell, the RSI of the recommended date needs to be above 70
def retrieve_signals_strict(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13"):
    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()

    retrieve_stm = 'SELECT trade_date, close_price, RSI_rsi, MACD_macd_histogram ' \
                   'FROM sp500_time_series_data ' \
                   'WHERE trade_date >= ? AND trade_date <= ? ' \
                   'AND symbol == ?'

    db_cursor.execute(retrieve_stm, (start_date, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    if(len(selected_data) == 0):
        print("No results found. Please check inputs to function 'retrieve_signals_strict'")
        return []

    buy_dates = []
    sell_dates = []
    hist_sign = 0

    for counter, day in enumerate(selected_data):
        temp_sign = copysign(1,day[3])
        if(hist_sign == 1 and temp_sign == -1):
            start_index = max(0, counter - 5)
            temp_date = day
            while start_index <= counter:
                if(selected_data[start_index][1] > temp_date[1]):
                    temp_date = selected_data[start_index]
                start_index = start_index + 1
            if(temp_date[0] != sell_dates[-1:] and temp_date[2]>= 70):
                sell_dates.append(temp_date[0])
        if(hist_sign == -1 and temp_sign == 1):
            start_index = max(0, counter - 5)
            temp_date = day
            while start_index <= counter:
                if(selected_data[start_index][1] < temp_date[1]):
                    temp_date = selected_data[start_index]
                start_index = start_index + 1
            if(temp_date[0] != buy_dates[-1:] and temp_date[2] <= 30):
                buy_dates.append(temp_date[0])
        hist_sign = temp_sign

    output = [buy_dates, sell_dates]
    return output

# Returns the buy and sell dates based on the traditional BB crossover method.
# Currently not operational as the BB lower crossing data in the trading.db is incorrect
def retrieve_BBAND_signals(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13"):
    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()

    retrieve_stm = 'SELECT trade_date, close_price, BB_real_upper_band, BB_real_lower_band ' \
                   'FROM sp500_time_series_data ' \
                   'WHERE trade_date >= ? AND trade_date <= ? ' \
                   'AND symbol == ?'

    db_cursor.execute(retrieve_stm, (start_date, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    if(len(selected_data) == 0):
        print("No results found. Please check inputs to function 'retrieve_BBAND_signals'")
        return []

    buy_dates = []
    sell_dates = []

    for counter, day in enumerate(selected_data):
        if(day[1] > day[2]):
            if(day[0] != sell_dates[-1:]):
                sell_dates.append(day[0])
        if (day[1] < day[3]):
            if (day[0] != buy_dates[-1:]):
                buy_dates.append(day[0])

    output = [buy_dates, sell_dates]
    return output
