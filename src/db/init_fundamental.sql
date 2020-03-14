CREATE TABLE fund_actions (
      date TEXT
     ,action TEXT
     ,ticker TEXT
     ,name TEXT
     ,value REAL
     ,contraticker TEXT
     ,contraname TEXT
     ,PRIMARY KEY(date, action, ticker, contraticker)
);

CREATE TABLE fund_daily (
      ticker TEXT
     ,date TEXT
     ,lastupdated TEXT
     ,ev REAL
     ,evebit REAL
     ,evebitda REAL
     ,marketcap REAL
     ,pb REAL
     ,pe REAL
     ,ps REAL
     ,PRIMARY KEY(ticker, date)
);

CREATE TABLE fund_events (
      ticker TEXT
     ,date TEXT
     ,eventcodes TEXT
     ,PRIMARY KEY (date, ticker)
);

CREATE TABLE fund_indicators (
      [table] TEXT
     ,indicator TEXT
     ,isfilter TEXT
     ,isprimarykey TEXT
     ,title TEXT
     ,description TEXT
     ,unittype TEXT
     ,PRIMARY KEY([table], indicator, isfilter, isprimarykey)
);

CREATE TABLE fund_sf1 (
      ticker TEXT
     ,dimension TEXT
     ,calendardate TEXT
     ,datekey TEXT
     ,reportperiod TEXT
     ,lastupdated TEXT
     ,accoci REAL
     ,assets REAL
     ,assetsavg REAL
     ,assetsc REAL
     ,assetsnc REAL
     ,assetturnover REAL
     ,bvps REAL
     ,capex REAL
     ,cashneq REAL
     ,cashnequsd REAL
     ,cor REAL
     ,consolinc REAL
     ,currentratio REAL
     ,de REAL
     ,debt REAL
     ,debtc REAL
     ,debtnc REAL
     ,debtusd REAL
     ,deferredrev REAL
     ,depamor REAL
     ,deposits REAL
     ,divyield REAL
     ,dps REAL
     ,ebit REAL
     ,ebitda REAL
     ,ebitdamargin REAL
     ,ebitdausd REAL
     ,ebitusd REAL
     ,ebt REAL
     ,eps REAL
     ,epsdil REAL
     ,epsusd REAL
     ,equity REAL
     ,equityavg REAL
     ,equityusd REAL
     ,ev REAL
     ,evebit REAL
     ,evebitda REAL
     ,fcf REAL
     ,fcfps REAL
     ,fxusd REAL
     ,gp REAL
     ,grossmargin REAL
     ,intangibles REAL
     ,intexp REAL
     ,invcap REAL
     ,invcapavg REAL
     ,inventory REAL
     ,investments REAL
     ,investmentsc REAL
     ,investmentsnc REAL
     ,liabilities REAL
     ,liabilitiesc REAL
     ,liabilitiesnc REAL
     ,marketcap REAL
     ,ncf REAL
     ,ncfbus REAL
     ,ncfcommon REAL
     ,ncfdebt REAL
     ,ncfdiv REAL
     ,ncff REAL
     ,ncfi REAL
     ,ncfinv REAL
     ,ncfo REAL
     ,ncfx REAL
     ,netinc REAL
     ,netinccmn REAL
     ,netinccmnusd REAL
     ,netincdis REAL
     ,netincnci REAL
     ,netmargin REAL
     ,opex REAL
     ,opinc REAL
     ,payables REAL
     ,payoutratio REAL
     ,pb REAL
     ,pe REAL
     ,pe1 REAL
     ,ppnenet REAL
     ,prefdivis REAL
     ,price REAL
     ,ps REAL
     ,ps1 REAL
     ,receivables REAL
     ,retearn REAL
     ,revenue REAL
     ,revenueusd REAL
     ,rnd REAL
     ,roa REAL
     ,roe REAL
     ,roic REAL
     ,ros REAL
     ,sbcomp REAL
     ,sgna REAL
     ,sharefactor REAL
     ,sharesbas REAL
     ,shareswa REAL
     ,shareswadil REAL
     ,sps REAL
     ,tangibles REAL
     ,taxassets REAL
     ,taxexp REAL
     ,taxliabilities REAL
     ,tbvps REAL
     ,workingcapital REAL
     ,PRIMARY KEY(ticker, dimension, datekey, reportperiod)
);

CREATE TABLE fund_sp500 (
      date TEXT
     ,action TEXT
     ,ticker TEXT
     ,name TEXT
     ,contraticker TEXT
     ,contraname TEXT
     ,note TEXT
     ,PRIMARY KEY(date, action, ticker)
);

CREATE TABLE fund_tickers (
      [table] TEXT
     ,permaticker INTEGER
     ,ticker TEXT
     ,name TEXT
     ,exchange TEXT
     ,isdelisted TEXT
     ,category TEXT
     ,cusips REAL
     ,siccode INTEGER
     ,sicsector TEXT
     ,sicindustry TEXT
     ,famasector TEXT
     ,famaindustry TEXT
     ,sector TEXT
     ,industry TEXT
     ,scalemarketcap TEXT
     ,scalerevenue TEXT
     ,relatedtickers TEXT
     ,currency TEXT
     ,location TEXT
     ,lastupdated TEXT
     ,firstadded TEXT
     ,firstpricedate TEXT
     ,lastpricedate TEXT
     ,firstquarter TEXT
     ,lastquarter TEXT
     ,secfilings TEXT
     ,companysite TEXT
     ,PRIMARY KEY([table], permaticker, ticker)
);

DELETE FROM fund_actions WHERE date = 'date' AND action = 'action' AND ticker = 'ticker' AND name = 'name' AND value = 'value' AND contraticker = 'contraticker' AND contraname = 'contraname';
DELETE FROM fund_daily WHERE ticker = 'ticker' AND date = 'date' AND lastupdated = 'lastupdated' AND ev = 'ev' AND evebit = 'evebit' AND evebitda = 'evebitda' AND marketcap = 'marketcap' AND pb = 'pb' AND pe = 'pe' AND ps = 'ps';
DELETE FROM fund_events WHERE ticker = 'ticker' AND date = 'date' AND eventcodes = 'eventcodes';
DELETE FROM fund_indicators WHERE [table] = 'table' AND indicator = 'indicator' AND isfilter = 'isfilter' AND isprimarykey = 'isprimarykey' AND title = 'title' AND description = 'description' AND unittype = 'unittype';
DELETE FROM fund_sf1 WHERE ticker = 'ticker' AND dimension = 'dimension' AND calendardate = 'calendardate' AND datekey = 'datekey' AND reportperiod = 'reportperiod' AND lastupdated = 'lastupdated' AND accoci = 'accoci' AND assets = 'assets' AND assetsavg = 'assetsavg' AND assetsc = 'assetsc' AND assetsnc = 'assetsnc' AND assetturnover = 'assetturnover' AND bvps = 'bvps' AND capex = 'capex' AND cashneq = 'cashneq' AND cashnequsd = 'cashnequsd' AND cor = 'cor' AND consolinc = 'consolinc' AND currentratio = 'currentratio' AND de = 'de' AND debt = 'debt' AND debtc = 'debtc' AND debtnc = 'debtnc' AND debtusd = 'debtusd' AND deferredrev = 'deferredrev' AND depamor = 'depamor' AND deposits = 'deposits' AND divyield = 'divyield' AND dps = 'dps' AND ebit = 'ebit' AND ebitda = 'ebitda' AND ebitdamargin = 'ebitdamargin' AND ebitdausd = 'ebitdausd' AND ebitusd = 'ebitusd' AND ebt = 'ebt' AND eps = 'eps' AND epsdil = 'epsdil' AND epsusd = 'epsusd' AND equity = 'equity' AND equityavg = 'equityavg' AND equityusd = 'equityusd' AND ev = 'ev' AND evebit = 'evebit' AND evebitda = 'evebitda' AND fcf = 'fcf' AND fcfps = 'fcfps' AND fxusd = 'fxusd' AND gp = 'gp' AND grossmargin = 'grossmargin' AND intangibles = 'intangibles' AND intexp = 'intexp' AND invcap = 'invcap' AND invcapavg = 'invcapavg' AND inventory = 'inventory' AND investments = 'investments' AND investmentsc = 'investmentsc' AND investmentsnc = 'investmentsnc' AND liabilities = 'liabilities' AND liabilitiesc = 'liabilitiesc' AND liabilitiesnc = 'liabilitiesnc' AND marketcap = 'marketcap' AND ncf = 'ncf' AND ncfbus = 'ncfbus' AND ncfcommon = 'ncfcommon' AND ncfdebt = 'ncfdebt' AND ncfdiv = 'ncfdiv' AND ncff = 'ncff' AND ncfi = 'ncfi' AND ncfinv = 'ncfinv' AND ncfo = 'ncfo' AND ncfx = 'ncfx' AND netinc = 'netinc' AND netinccmn = 'netinccmn' AND netinccmnusd = 'netinccmnusd' AND netincdis = 'netincdis' AND netincnci = 'netincnci' AND netmargin = 'netmargin' AND opex = 'opex' AND opinc = 'opinc' AND payables = 'payables' AND payoutratio = 'payoutratio' AND pb = 'pb' AND pe = 'pe' AND pe1 = 'pe1' AND ppnenet = 'ppnenet' AND prefdivis = 'prefdivis' AND price = 'price' AND ps = 'ps' AND ps1 = 'ps1' AND receivables = 'receivables' AND retearn = 'retearn' AND revenue = 'revenue' AND revenueusd = 'revenueusd' AND rnd = 'rnd' AND roa = 'roa' AND roe = 'roe' AND roic = 'roic' AND ros = 'ros' AND sbcomp = 'sbcomp' AND sgna = 'sgna' AND sharefactor = 'sharefactor' AND sharesbas = 'sharesbas' AND shareswa = 'shareswa' AND shareswadil = 'shareswadil' AND sps = 'sps' AND tangibles = 'tangibles' AND taxassets = 'taxassets' AND taxexp = 'taxexp' AND taxliabilities = 'taxliabilities' AND tbvps = 'tbvps' AND workingcapital = 'workingcapital';
DELETE FROM fund_sp500 WHERE date = 'date' AND action = 'action' AND ticker = 'ticker' AND name = 'name' AND contraticker = 'contraticker' AND contraname = 'contraname' AND note = 'note';
DELETE FROM fund_tickers WHERE [table] = 'table' AND permaticker = 'permaticker' AND ticker = 'ticker' AND name = 'name' AND exchange = 'exchange' AND isdelisted = 'isdelisted' AND category = 'category' AND cusips = 'cusips' AND siccode = 'siccode' AND sicsector = 'sicsector' AND sicindustry = 'sicindustry' AND famasector = 'famasector' AND famaindustry = 'famaindustry' AND sector = 'sector' AND industry = 'industry' AND scalemarketcap = 'scalemarketcap' AND scalerevenue = 'scalerevenue' AND relatedtickers = 'relatedtickers' AND currency = 'currency' AND location = 'location' AND lastupdated = 'lastupdated' AND firstadded = 'firstadded' AND firstpricedate = 'firstpricedate' AND lastpricedate = 'lastpricedate' AND firstquarter = 'firstquarter' AND lastquarter = 'lastquarter' AND secfilings = 'secfilings' AND companysite = 'companysite';

-------------------------------------------------------------
-- Create Industry USD Ratio Average, Min and Max View for --
-- MRY: Annual dimension; including restatements           --
-------------------------------------------------------------

CREATE VIEW avgMinMaxByIndustryMRY
AS
SELECT
  b.sicsector as [SIC Sector],
  b.sicindustry as [SIC Industry],
  b.sector as [Sector],
  b.industry as [Industry],
  b.scalemarketcap as [Scale Market Cap],
  b.scalerevenue as [Scale Revenue],
  a.dimension as [Dimension],
  a.calendardate as [Calendar Date],
  a.datekey as [Date Key],
  AVG(a.cashnequsd) as [Avg Cash Equiv (USD)],
  AVG(a.currentratio) as [Avg Current Ratio],
  AVG(a.ebitdausd) as [Avg EBITDA (USD)],
  AVG(a.ebitusd) as [AVG EBIT (USD)],
  AVG(a.epsusd) as [Avg EPS Basic (USD)],
  AVG(a.ev) as [Avg Enterprise Value],
  AVG(a.evebit) as [Avg Enterprise Value over EBIT],
  AVG(a.evebitda) as [ Avg Enterprise Value over EBITDA],
  AVG(a.netinccmnusd) as [Avg NI CS (USD)],
  AVG(a.payoutratio) as [Avg Payout Ratio],
  AVG(a.pb) as [Avg Price to Book Value],
  AVG(a.pe) as [Avg Price Earnings (Damodaran Method)],
  AVG(a.pe1) as [Avg Price to Earnings Ratio],
  AVG(a.ps) as [Avg Price Sales (Damodaran Method)],
  AVG(a.revenueusd) as [Avg Revenues (USD)],
  AVG(a.sps) as [Avg Sales per Share],
  MIN(a.cashnequsd) as [Min Cash Equiv (USD)],
  MIN(a.currentratio) as [Min Current Ratio],
  MIN(a.ebitdausd) as [Min EBITDA (USD)],
  MIN(a.ebitusd) as [MIN EBIT (USD)],
  MIN(a.epsusd) as [Min EPS Basic (USD)],
  MIN(a.ev) as [Min Enterprise Value],
  MIN(a.evebit) as [Min Enterprise Value over EBIT],
  MIN(a.evebitda) as [ Min Enterprise Value over EBITDA],
  MIN(a.netinccmnusd) as [Min NI CS (USD)],
  MIN(a.payoutratio) as [Min Payout Ratio],
  MIN(a.pb) as [Min Price to Book Value],
  MIN(a.pe) as [Min Price Earnings (Damodaran Method)],
  MIN(a.pe1) as [Min Price to Earnings Ratio],
  MIN(a.ps) as [Min Price Sales (Damodaran Method)],
  MIN(a.revenueusd) as [Min Revenues (USD)],
  MIN(a.sps) as [Min Sales per Share],
  MAX(a.cashnequsd) as [Max Cash Equiv (USD)],
  MAX(a.currentratio) as [Max Current Ratio],
  MAX(a.ebitdausd) as [Max EBITDA (USD)],
  MAX(a.ebitusd) as [MAX EBIT (USD)],
  MAX(a.epsusd) as [Max EPS Basic (USD)],
  MAX(a.ev) as [Max Enterprise Value],
  MAX(a.evebit) as [Max Enterprise Value over EBIT],
  MAX(a.evebitda) as [ Max Enterprise Value over EBITDA],
  MAX(a.netinccmnusd) as [Max NI CS (USD)],
  MAX(a.payoutratio) as [Max Payout Ratio],
  MAX(a.pb) as [Max Price to Book Value],
  MAX(a.pe) as [Max Price Earnings (Damodaran Method)],
  MAX(a.pe1) as [Max Price to Earnings Ratio],
  MAX(a.ps) as [Max Price Sales (Damodaran Method)],
  MAX(a.revenueusd) as [Max Revenues (USD)],
  MAX(a.sps) as [Max Sales per Share]
FROM (SELECT * FROM fund_sf1
      WHERE dimension = 'ARY') as a
LEFT JOIN (SELECT * FROM fund_tickers
           WHERE isdelisted = 'N') as b
     ON a.ticker = b.ticker
GROUP BY b.sicsector, b.sicindustry, b.sector,
         b.industry, b.scalemarketcap, b.scalerevenue;
