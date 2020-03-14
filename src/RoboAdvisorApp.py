from sqlite3.dbapi2 import Cursor
from flaskext.mysql import MySQL
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Utils import Utils
from NewsClient import NewsClient
import Fundamental

import sqlite3

import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '/../db/trading.db')
app.config['MYSQL_DATABASE_USER'] = Utils.read_properties().get('DATABASE','aws_user')
app.config['MYSQL_DATABASE_PASSWORD'] = Utils.read_properties().get('DATABASE', 'aws_password')
app.config['MYSQL_DATABASE_DB'] = Utils.read_properties().get('DATABASE','aws_database')
app.config['MYSQL_DATABASE_HOST'] = Utils.read_properties().get('DATABASE','aws_host')
mysql = MySQL()
mysql.init_app(app)

conn1 = sqlite3.connect(os.path.join(basedir, '..', "data/db/trading.db"), check_same_thread=False)
curr1: Cursor = conn1.cursor()
curr_recommend: Cursor = conn1.cursor()

database = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/data/<symbol>")
def getData(symbol):
    results = []
    exchange = getExchange(symbol)
    if exchange:
        with mysql.connect() as cur:
            query = "select (UNIX_TIMESTAMP(trade_date) * 1000), high_price, low_price, open_price, close_price, volume, RSI_rsi, MACD_macd_signal, MACD_macd_histogram, MACD_macd, BB_real_upper_band, BB_real_middle_band, BB_real_lower_band, OBV_obv from {} where symbol=%s".format(exchange)
            cur.execute(query, list([symbol]))
            results = cur.fetchall()
    return jsonify(results)

@app.route("/recommendation/<symbol>")
def getRecommendation(symbol):
    results = curr_recommend.execute("select recommendation, count(*) from recommendation where symbol= ? group by recommendation order by count(*)  limit 1 ",list([symbol])).fetchall()
    if (len(results) > 0 and len(results[0])):
        return jsonify([results[0][0]])
    else:
        return jsonify(['NONE'])

@app.route("/news/<symbol>")
def getNewsArticles(symbol):

    news_client = NewsClient(symbol)
    all_articles = news_client.fetch_news_articles()

    return jsonify(all_articles)

@app.route("/typeahead")
def getTypeaheadSymbols():
    results = {"symbols": []}
    with open(os.path.join(basedir, "../data/typeahead.txt"), "r") as f:
        for company in f:
            results["symbols"].append(company)
    return jsonify(results)

def get_symbol_list(exchange):
    output = []
    with mysql.connect() as cur:
        cur.execute("select DISTINCT CONCAT(symbol, ', ', company_name) FROM " + exchange)
        output = cur.fetchall()
    return output

def getExchange(symbol):
    results = []
    out = ""
    with mysql.connect() as cur:
        cur.execute("select symbol from sp500_time_series_data where symbol=%s limit 1", list([symbol]))
        results = cur.fetchall()
        if len(results) == 1:
            return "sp500_time_series_data"
        cur.execute("select symbol from nyse_time_series_data where symbol=%s limit 1", list([symbol]))
        results = cur.fetchall()
        if len(results) == 1:
            return "nyse_time_series_data"
        cur.execute("select symbol from nasdaq_time_series_data where symbol=%s limit 1", list([symbol]))
        results = cur.fetchall()
        if len(results) == 1:
            return "nasdaq_time_series_data"
    return ""

@app.route("/fundamentals/<symbol>")
def getFundamentals(symbol):
    conn2 = sqlite3.connect(basedir + "/../data/db/Fundamental_Data.db", check_same_thread=False)
    curr2 = conn2.cursor()

    fundamental = Fundamental.Fundamental(conn2, curr2, symbol)
    data = fundamental.get_fundamentals()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)