from datetime import datetime

class Fundamental(object):

    def __init__(self, conn, cur, ticker):
        self.conn = conn
        self.cur = cur
        self.ticker = ticker

    def sign(self, x):
        sign = 1-(x<=0)
        if sign == 0:
            signStr = '-'
        else:
            signStr = ''
        return signStr

    def largeNumberConverter(self, n):
        signStr = self.sign(n)
        n = abs(n)
        if (n >= 1000000) and (n < 1000000000):
            n = n / 1000000
            nstr = "{0:,.2f}".format(n)
            nstr = signStr + nstr + 'M'
        elif (n >= 1000000000) and (n < 1000000000000):
            n = n / 1000000000
            nstr = "{0:,.2f}".format(n)
            nstr = signStr + nstr + 'B'
        elif (n >= 1000000000000) and (n < 1000000000000000):
            n = n / 1000000000000
            nstr = "{0:,.2f}".format(n)
            nstr = signStr + nstr + 'T'
        else:
            nstr = "{0:,.2f}".format(n)
            if n > 99:
                nstr = signStr + "{0:,.2f}".format(n)
            else:
                nstr = "{0:,.2f}".format(n)
                nstr = signStr + nstr
        return nstr

    def get_fundamentals(self):
        self.cur.execute('SELECT '
                        'a.[name] as [00: Company Name] '
                        ',a.[companysite] as [01: Company Website URL] '
                        ',a.[exchange] as [02: Stock Exchange] '
                        ',a.[secfilings] as [03: SEC Filings URL] '
                        ',a.[sector] as [04: Sector] '
                        ',a.[industry] as [05: Industry] '
                        ',a.[sicindustry] as [06: SIC Industry] '
                        ',b.[calendardate] as [14: Report Date] '
                        ',b.[sharesbas] as [15: Shares (Basic)] '
                        ',b.[epsusd] as [16: Earnings per Basic Share] '
                        ',b.[pe1] as [17: Price to Earnings Ratio] '
                        ',b.[bvps] as [18: Book Value per Share] '
                        ',b.[dps] as [19: Dividends per Basic Common Share] '
                        ',b.[divyield] as [20: Dividend Yield] '
                        ',b.[payoutratio] as [21: Payout Ratio] '
                        ',b.[ncfdiv] as [22: Payment of Div. & Other Dist.] '
                        ',b.[revenueusd] as [23: Revenues] '
                        ',a.[scalerevenue] as [24: Company Scale - Revenue] '
                        ',b.[marketcap] as [25: Market Capitalization] '
                        ',a.[scalemarketcap] as [26: Company Scale - Market Cap] '
                        ',b.[sps] as [27: Sales per Share] '
                        ',b.[gp] as [28: Gross Profit] '
                        ',b.[grossmargin] as [29: Gross Margin] '
                        ',b.[opinc] as [30: Operating Income] '
                        ',b.[depamor] as [31: Depreciation Amortization & Accretion] '
                        ',b.[ebitdausd] as [32: EBITDA] '
                        ',b.[ebitdamargin] as [33: EBITDA Margin] '
                        ',b.[ebitusd] as [34: Earning Before Interest & Taxes] '
                        ',b.[ebt] as [35 Earnings before Tax] '
                        ',b.[netinc] as [36: Net Income] '
                        ',b.[netmargin] as [37: Profit Margin] '
                        ',b.[consolinc] as [38: Consolidated Income] '
                        ',b.[fcfps] as [39: Free Cash Flow per Share] '
                        ',b.[fcf] as [40: Free Cash Flow] '
                        ',b.[ncfo] as [41: Net Cash Flow from Operations] '
                        ',b.[cashnequsd] as [42: Cash on Hand] '
                        ',b.[retearn] as [43: Accumulated Retained Earnings (Deficit)] '
                        ',b.[assetsc] as [44: Current Assets] '
                        ',b.[liabilitiesc] as [45: Current Liabilities] '
                        ',b.[currentratio] as [46: Current Ratio] '
                        ',b.[workingcapital] as [47: Working Capital] '
                        ',b.[assetsavg] as [48: Average Assets] '
                        ',b.[assetturnover] as [49: Asset Turnover] '
                        ',b.[roa] as [50: Return on Average Assets (ROA)] '
                        ',b.[roe] as [51: Return on Average Equity (ROE)] '
                        ',b.[debtc] as [52: Debt Current] '
                        ',b.[debtnc] as [53: Debt Non-Current] '
                        ',b.[equity] as [54: Shareholders Equity] '
                        ',b.[de] as [55: Debt to Equity Ratio] '
                        ',b.[roic] as [56: Return on Invested Capital] '
                        ',b.[ros] as [57: Return on Sales] '
                    'FROM (SELECT * FROM fund_sf1 '
                          'WHERE ticker =? '
                            'AND dimension = \'ART\' '
                            'AND calendardate = (SELECT MAX(calendardate) from fund_sf1 '
                                                'WHERE ticker =? '
                                                '  AND dimension = \'ART\')) as b '
                    'LEFT JOIN (SELECT * FROM fund_tickers '
                               'WHERE ticker =? '
                                 'AND lastupdated = (SELECT MAX(lastupdated) from fund_tickers '
                                                    'WHERE ticker =?)) as a '
                          'ON b.ticker = a.ticker', (self.ticker, self.ticker, self.ticker, self.ticker))
        row = self.cur.fetchone()
        if row == None:
            data = {}
        else:
            desc = self.cur.description
            column_names = [col[0] for col in desc]
            data = {col:val for (col, val) in zip(column_names, row)}
        # Convert numeric and date values to formatted string
        percent_format_columns = ['20: Dividend Yield', '21: Payout Ratio', '29: Gross Margin', '33: EBITDA Margin', '37: Profit Margin', '50: Return on Average Assets (ROA)', '51: Return on Average Equity (ROE)', '56: Return on Invested Capital', '57: Return on Sales']
        date_format_columns = ['07: Date', '14: Report Date']
        string_columns = ['00: Company Name', '01: Company Website URL', '02: Stock Exchange', '03: SEC Filings URL', '04: Sector', '05: Industry', '06: SIC Industry', '24: Company Scale - Revenue', '26: Company Scale - Market Cap']
        for k, v in data.items():
            if k in percent_format_columns:
                data[k] = "{:.2%}".format(v)
            elif k in date_format_columns:
                data[k] = datetime.strptime(v, '%Y-%m-%d').strftime('%B %d, %Y')
            elif k not in string_columns:
                data[k] = self.largeNumberConverter(v)

        return data
