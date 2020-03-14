import requests
import json
import sys
import bs4 as bs
import mysql.connector

aws_host = "database-2.cmrdipsyt8zj.us-east-2.rds.amazonaws.com"
aws_database = "market_data"
aws_db = mysql.connector.connect(host=aws_host, user=sys.argv[2], passwd=sys.argv[3], database=aws_database)
aws_db_cursor = aws_db.cursor()

def get_SP500_symbols():
  resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  soup = bs.BeautifulSoup(resp.text, 'lxml')
  table = soup.find('table', {'class': 'wikitable sortable'})
  tickers = []
  for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text.rstrip()
    tickers.append(ticker)
  return tickers

def fetch_historical_prices():
  tickers = get_SP500_symbols()
  max_requests = 250
  api_key = sys.argv[1]
  api_prefix_url = "https://api.worldtradingdata.com/api/v1/history?api_token=" + api_key + "&sort=newest&symbol="
  for i in range(1, max_requests):
    api_url = api_prefix_url + tickers[i]
    try:
      stock_prices = requests.get(api_url)
      stock_prices_json = json.loads(stock_prices.text)
      ticker = stock_prices_json['name']
      for date, price_data in stock_prices_json["history"].items():
        open_price = float(price_data["open"])
        close_price = float(price_data["close"])
        high_price = float(price_data["high"])
        low_price = float(price_data["low"])
        volume = int(price_data["volume"])
        values = (ticker, open_price, close_price, high_price, low_price, volume, date)
        write_prices_to_db(values)
    except Exception as e:
      print(str(e))
    break

def write_prices_to_db(stock_prices):
    sql_insert = "INSERT INTO stock_market_data (ticker, open_price, close_price, high_price, low_price, volume, price_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    aws_db_cursor.execute(sql_insert, stock_prices)
    aws_db.commit()

if __name__== "__main__":
  fetch_historical_prices()