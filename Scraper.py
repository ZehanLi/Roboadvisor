import requests
import bs4 as bs
import pickle
import csv
import os

class Scraper:
    @staticmethod
    def get_sp500_symbols():
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = {}
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text.strip()
            if ticker not in tickers:
                tickers[ticker] = row.findAll('td')[1].text.strip()
        return tickers

    @staticmethod
    def get_exchange_symbols(exchange):
        stock_symbols_file = os.getcwd() + "/data/" + exchange + ".csv"
        tickers = {}
        with open(stock_symbols_file, "r") as symbols_file:
            csv_reader = csv.reader(symbols_file, delimiter='\t')
            next(csv_reader)
            for row in csv_reader:
                tickers[row[0].strip()] = row[1].strip()         
        return tickers;

    @staticmethod
    def read_symbols():
        symbol_file = open(os.getcwd() + "/data/symbol.list")
        symbol_data = symbol_file.readlines()
        symbol_list = {}
        for symbol in symbol_data:
            symbol_tok = symbol.split(",")
            symbol_list[symbol_tok[1].strip('\n')] = symbol_tok[0].strip('\n')
        return symbol_list