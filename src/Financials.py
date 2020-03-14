import ssl
from yahoofinancials import YahooFinancials

class Financials:
    def get_financials(self, symbol):
        ssl._create_default_https_context = ssl._create_unverified_context
        yahoo_financials = YahooFinancials(symbol)
        print(yahoo_financials.get_financial_stmts('quarterly', 'income'))
