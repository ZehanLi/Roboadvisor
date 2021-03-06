CREATE TABLE sp500_time_series_data (
	symbol VARCHAR(20) NOT NULL,
	company_name VARCHAR(100) NOT NULL,
	trade_date DATE NOT NULL,
	open_price DOUBLE NOT NULL,
	high_price DOUBLE NOT NULL,
	low_price DOUBLE NOT NULL,
	close_price DOUBLE NOT NULL,
	volume INT NOT NULL,
	RSI_rsi FLOAT NOT NULL,
	MACD_macd_signal FLOAT NOT NULL,
	MACD_macd_histogram FLOAT NOT NULL,
	MACD_macd FLOAT NOT NULL,
	BB_real_upper_band FLOAT NOT NULL,
	BB_real_middle_band FLOAT NOT NULL,
	BB_real_lower_band FLOAT NOT NULL,
	OBV_obv FLOAT NOT NULL,
	PRIMARY KEY (symbol, trade_date)
);

CREATE TABLE nyse_time_series_data (
	symbol VARCHAR(20) NOT NULL,
	company_name VARCHAR(100) NOT NULL,
	trade_date DATE NOT NULL,
	open_price DOUBLE NOT NULL,
	high_price DOUBLE NOT NULL,
	low_price DOUBLE NOT NULL,
	close_price DOUBLE NOT NULL,
	volume INT NOT NULL,
	RSI_rsi FLOAT NOT NULL,
	MACD_macd_signal FLOAT NOT NULL,
	MACD_macd_histogram FLOAT NOT NULL,
	MACD_macd FLOAT NOT NULL,
	BB_real_upper_band FLOAT NOT NULL,
	BB_real_middle_band FLOAT NOT NULL,
	BB_real_lower_band FLOAT NOT NULL,
	OBV_obv FLOAT NOT NULL,
	PRIMARY KEY (symbol, trade_date)
);

CREATE TABLE nasdaq_time_series_data (
	symbol VARCHAR(20) NOT NULL,
	company_name VARCHAR(100) NOT NULL,
	trade_date DATE NOT NULL,
	open_price DOUBLE NOT NULL,
	high_price DOUBLE NOT NULL,
	low_price DOUBLE NOT NULL,
	close_price DOUBLE NOT NULL,
	volume INT NOT NULL,
	RSI_rsi FLOAT NOT NULL,
	MACD_macd_signal FLOAT NOT NULL,
	MACD_macd_histogram FLOAT NOT NULL,
	MACD_macd FLOAT NOT NULL,
	BB_real_upper_band FLOAT NOT NULL,
	BB_real_middle_band FLOAT NOT NULL,
	BB_real_lower_band FLOAT NOT NULL,
	OBV_obv FLOAT NOT NULL,
	PRIMARY KEY (symbol, trade_date)
);

CREATE TABLE recommendation (
	symbol VARCHAR(20) NOT NULL,
	model_name VARCHAR(100) NOT NULL,
	recommendation VARCHAR(5) NOT NULL
);

--added test signal column that holds test data generated by TradingSignal.py
alter table sp500_time_series_data add test_signal varchar(10);
