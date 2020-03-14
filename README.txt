DESCRIPTION:
The package folder structure is shown below.
At the Top level we have data, logs, lstm_logs, and src folders
    data: This folder holds properties, databases, generated images, and models
    src: This folder holds all other python source code and the initial db scripts required to create database from scratch
    logs/logs_lstm: These folders are where application generated logs are created

Main.py has the bootstrap code that will fetch the data using APIs, persist to db, build models, and generate
recommendation and persist it to database.

RoboAdvisorApp.py under src folder has the Flask application code. This will by default-start the webapp at http://127.0.0.1:5000/
and render the UI for the application.

RoboAdvisor
    |   Main.py
    |   readme.txt
    |   requirements.txt
    |   __init__.py
    |
    data
    |   |   indicator.properties
    |   |   nasdaq.csv
    |   |   nyse.csv
    |   |   symbol.list
    |   |   typeahead.txt
    |   |
    |   db
    |   |       Fundamental_Data.db
    |   |       trading.db
    |   |       training.db
    |   |
    |   images
    |   model
    |           AMZN.h5
    |           LSTM_AMZN.h5
    |           LSTM_SCHW.h5
    |           SCHW.h5
    logs
    lstm_logs
    src
    |   |   AlphaV.py
    |   |   Constants.py
    |   |   fetch_historical_prices.py
    |   |   Financials.py
    |   |   Fundamental.py
    |   |   GenerateImages.py
    |   |   GenerateImagesNoHold.py
    |   |   ImageBasedClassifier.py
    |   |   LSTMClasifier.py
    |   |   NewsClient.py
    |   |   Persister.py
    |   |   PersisterSqlite.py
    |   |   RandomForestClassifier.py
    |   |   Recommender.py
    |   |   RoboAdvisorApp.py
    |   |   Scraper.py
    |   |   TrainingSignals.py
    |   |   TrainingSignalsNoHold.py
    |   |   Utils.py
    |   db
    |   |       init.sql
    |   |       init_fundamental.sql
    |   |       trading.db
    |   static
    |   |   styles
    |   |           index.css
    |   |
    |   templates
    |   |       index.html


INSTALLATION:
To install the code in local machine follow the below steps:
1.Create project directory in your local disk
2.Unzip team46final.zip from the submission and copy RoboAdvisor directory into your created project directory from step 1.
Go to the RoboAdvisor directory.
3.Install
    python3 (https://www.python.org/downloads/)
    pip (pip install pip)
    anaconda(https://docs.anaconda.com/anaconda/install)
4.Create a virtual environment
    >conda env create
    >conda activate roboadvisor
5.Get the AlphaVantage API key by following the instructions here: https://www.alphavantage.co/support/#api-key
6.Get the news-api API key by following the instructions here: https://newsapi.org/docs/get-started
7.Set the environment variable for AlphaVantage key
    export ALPHA_VANTAGE_KEY='62VU0Z7IKBLN5VYE' (For Linux/MacOs terminals)
    set ALPHA_VANTAGE_KEY=<Your Key> (For windows command prompt)
8.Set the environment variable for news-api key (You WILL need this key if you want to view the full functionality of the app!)
    export NEWS_API_KEY='82cfeff574a349b789025b6370f63369' (For Linux/MacOs terminals)
    set NEWS_API_KEY=<Your Key> (For windows command prompt)
9.Download and install sqlite3 from https://www.sqlite.org/index.html

# If you want to create your own tables then execute steps 10-12
10.Create the database and tables for time series and technical indicators data using the command below:
    mv data/db/trading.db data/db/trading.db.previousrun
    sqlite3 data/db/trading.db < src/db/init.sql
11.Create the database and tables for fundamental data using the command below:
    sqlite3 data/db/fundamental_Data.db < src/db/init_fundamental.sql
12. cp data/db/Fundamental_Data-mini.db data/db/Fundamental_Data.db

# If you want to use our toy datasets then execute steps 13-14
13. cp data/db/trading-mini.db data/db/trading.db
14. cp data/db/Fundamental_Data-mini.db data/db/Fundamental_Data.db
15. If you see any folder related errors on Windows machine, please create them manually.

EXECUTION:
To start data fetching and model generation, run below command from RoboAdvisor folder (You can skip this step if you want to use the toy datasets provided)
> python3 Main.py -image generate -model create -database sqllite -mode test -training_period 5

Run the app
 > python3 src/RoboAdvisorApp.py

 Now open http://127.0.0.1:5000 in the browser which would display the app.
 By default, we will display charts and other information for AMZN.
 You can search AAPL, DIS etc. and see all the charts and other information on the UI.