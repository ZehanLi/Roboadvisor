import sqlite3
from math import copysign
from src import Constants

# Simply looks for MACD crossover and then checks over the previous week of trading for the day with the:
#   highest stock price if selling or lowest stock price if buying
# and appends this date to the appropriate list.

# Output Format: List of 2 element lists: [[trade_date1, signal1], [trade_date2, signal2], ...]
#   trade_date in the form "YYY-MM-DD"
#   signal is one of the following: "buy", "sell", "hold"
def retrieve_signals_basic(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13", hold=True):
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

    output = []
    for day in selected_data:
        if day[0] in buy_dates:
            output.append([day[0], "buy"])
        elif day[0] in sell_dates:
            output.append([day[0], "sell"])
        elif hold:
            output.append([day[0], "hold"])

    training_sql = "UPDATE  sp500_time_series_data set test_signal = ? WHERE trade_date = ? AND symbol = ?"

    for d in buy_dates:
        db_cursor.execute(training_sql, ('BUY', d, ticker))

    for d in sell_dates:
        db_cursor.execute(training_sql, ('SELL', d, ticker))
    conn.commit()
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

    training_sql = "UPDATE  sp500_time_series_data set test_signal = ? WHERE trade_date = ? AND symbol = ?"

    for d in buy_dates:
        db_cursor.execute(training_sql, ('BUY', d, ticker))

    for d in sell_dates:
        db_cursor.execute(training_sql, ('SELL', d, ticker))
    conn.commit()
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

    training_sql = "UPDATE  sp500_time_series_data set test_signal = ? WHERE trade_date = ? AND symbol = ?"

    for d in buy_dates:
        db_cursor.execute(training_sql, ('BUY', d, ticker))

    for d in sell_dates:
        db_cursor.execute(training_sql, ('SELL', d, ticker))
    conn.commit()
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

# Returns an array with each trading day and the corresponding signal: either buy, sell, or hold.
def generate_rf_signals(ticker = "AMZN", start_date = "2014-10-13", end_date = "2014-12-13", days_ahead = 1, percent_change = 0):
    # days_ahead is how many days ahead we check for either an increase or decrease to determine if the starting day is a buy/sell/hold
    # percent_change is how much of an increase or decrease is required to trigger a buy/sell. If 0, then simply increasing or decreasing is enough

    conn = sqlite3.connect(Constants.DB_DIR)
    db_cursor = conn.cursor()

    retrieve_stm = 'SELECT trade_date, close_price, BB_real_upper_band, BB_real_lower_band ' \
                   'FROM sp500_time_series_data ' \
                   'WHERE trade_date >= ? AND trade_date <= ? ' \
                   'AND symbol == ?'

    db_cursor.execute(retrieve_stm, (start_date, end_date, ticker,))
    selected_data = list(db_cursor.fetchall())

    if(len(selected_data) == 0):
        print("No results found. Please check inputs to function 'generate_rf_signals'")
        return []

    signals = []

    for counter, day in enumerate(selected_data[:-days_ahead]):
        # Increase of 5% or more in 10 trade days
        if(selected_data[counter+days_ahead][1]>= (1 + percent_change/100)*selected_data[counter][1]):
            signals.append([selected_data[counter][0],"buy"])
        # elif(selected_data[counter+days_ahead][1]<= (1 - percent_change/100)*selected_data[counter][1]):
        #     signals.append([selected_data[counter][0],"sell"])
        else:
            signals.append([selected_data[counter][0], "hold"])

    return signals