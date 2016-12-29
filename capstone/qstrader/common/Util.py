#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py
import os
import pandas as pd
import pandas.io.data
import matplotlib.pyplot as plt
import version

import datetime
import warnings
from qstrader.common import settings
import requests
import os


def getAppDir() :
    return version.ROOT_DIR


def getConfigDir() :
    configDir = getAppDir() + "/" + "config"
    return configDir


def getqQstraderConfig() :
    return  getConfigDir() + "/qstrader.yml"


def get_daily_historic_data_yahoo(
        ticker, start_date=(2000,1,1),
        end_date=datetime.date.today().timetuple()[0:3]
    ):
    # type: (object, object, object) -> object
    """
    Obtains data from Yahoo Finance returns and a list of tuples.

    ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D) format
    end_date: End date in (YYYY, M, D) format
    """
    # Construct the Yahoo URL with the correct integer query parameters
    # for start and end dates. Note that some parameters are zero-based!
    ticker_tup = (
        ticker, start_date[1]-1, start_date[2],
        start_date[0], end_date[1]-1, end_date[2],
        end_date[0]
    )
    yahoo_url = "http://ichart.finance.yahoo.com/table.csv"
    yahoo_url += "?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s"
    yahoo_url = yahoo_url % ticker_tup

    # Try connecting to Yahoo Finance and obtaining the data
    # On failure, print an error message.
    try:
        yf_data = requests.get(yahoo_url).text.split("\n")[1:-1]
        prices = []
        for y in yf_data:
            p = y.strip().split(',')
            prices.append(
                (datetime.datetime.strptime(p[0], '%Y-%m-%d'),
                p[1], p[2], p[3], p[4], p[5], p[6])
            )
    except Exception as e:
        print("Could not download Yahoo data: %s" % e)
    return prices


def get_data(symbol):

    config = settings.from_file(getqQstraderConfig())

    csvFile = config.CSV_DATA_DIR + "/" + symbol + ".csv"
    print "CSV file", csvFile
    # Read only dates and Adj Close column
    df_temp = pd.read_csv(csvFile,usecols=[0, 1], na_values=['nan'])

    #df_temp = df_temp.rename(columns={'Adj Close': symbol})

    # Join this symbol to the global data frame
    #df = df.join(df_temp)
    #if symbol == 'SPY':  # drop dates SPY did not trade
     #   df = df.dropna(subset=["SPY"])

    return df_temp


def downloadData(ticker_weights, start_date=(2007, 12, 4), end_date=(2016, 10, 12)) :

    config = settings.from_file(getqQstraderConfig())

    for ticker in ticker_weights:

        csvFile = config.CSV_DATA_DIR + "/" + ticker + ".csv"

        data = get_daily_historic_data_yahoo(ticker, start_date,end_date )

        # Date,Open,High,Low,Close,Volume,Adj Close

        comma = ","

        if os.path.exists(csvFile) :
            os.remove(csvFile)

        print ("Creating CSV file:", csvFile)
        with open(csvFile, 'w') as the_file:

            for line in data:
                # col1 = datetime.datetime.strptime( str(line[0]), '%Y-%m-%d')
                col1 = line[0]
                col2 = line[1]
                col3 = line[2]
                col4 = line[3]
                col5 = line[4]
                col6 = line[5]
                col7 = line[6]

                # 2016-10-12 00:00:00
                dat = datetime.datetime.strptime(str(col1), '%Y-%m-%d %H:%M:%S').date()
                the_file.write(str(dat) + comma +
                               str(col2) + comma +
                               str(col3) + comma +
                               str(col4) + comma +
                               str(col5) + comma +
                               str(col6) + comma +
                               str(col7) + '\n')



if __name__ == "__main__":

    print getAppDir()
    print getConfigDir()

    os._exit(1)
    ticker_weights ={
                         "SPY": 0.125,
                         "IJS": 0.125,
                         "EFA": 0.125,
                         "EEM": 0.125,
                         "AGG": 0.125,
                         "JNK": 0.125,
                         "DJP": 0.125,
                         "RWR": 0.125
                     }

    start_date = datetime.datetime(2007, 12, 4)
    end_date = datetime.datetime(2016, 10, 12)

    print "Starting..."

    downloadData(ticker_weights, start_date.timetuple()[0:3], end_date.timetuple()[0:3])

    for ticket, wgt in ticker_weights.iteritems():
        results = get_data(ticket)
        print (results)