import os

import matplotlib.pyplot as plt
import numpy as np
import pandas
import smarttrader.indicators.bak.technical_indicators as ti
from qstrader.common.yahoo_finance_historical_data_extract import YFHistDataExtr

if __name__ == '__main__':

    prices = np.array([0, 11045.27, 11167.32, 11008.61, 11151.83, 10926.77,
                       10868.12, 10520.32, 10380.43, 10785.14, 10748.26, 10896.91, 10782.95,
                       10620.16, 10625.83, 10510.95, 10444.37, 10068.01, 10193.39, 10066.57,
                       10043.75])

    prices = np.array([0, 11045.27, 11167.32])
    print(ti.sma(prices, period=12))

    os._exit(1)

    data_ext = YFHistDataExtr()
    data_ext.set_interval_to_retrieve(200)  # in days
    data_ext.set_multiple_stock_list(['BN4.SI'])
    data_ext.get_hist_data_of_all_target_stocks()
    # convert the date column to date object
    data_ext.all_stock_df['Date'] = pandas.to_datetime(data_ext.all_stock_df['Date'])
    temp_data_set = data_ext.all_stock_df.sort('Date', ascending=True)  # sort to calculate the rolling mean

    temp_data_set['20d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20)
    temp_data_set['50d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=50)
    temp_data_set['Bol_upper'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) + 2 * pandas.rolling_std(
        temp_data_set['Adj Close'], 20, min_periods=20)
    temp_data_set['Bol_lower'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) - 2 * pandas.rolling_std(
        temp_data_set['Adj Close'], 20, min_periods=20)
    temp_data_set['Bol_BW'] = (
                              (temp_data_set['Bol_upper'] - temp_data_set['Bol_lower']) / temp_data_set['20d_ma']) * 100
    temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(temp_data_set['Bol_BW'], window=50)  # cant get the 200 daa
    temp_data_set['Bol_BW_200MA'] = temp_data_set['Bol_BW_200MA'].fillna(method='backfill')  ##?? ,may not be good
    temp_data_set['20d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=20)
    temp_data_set['50d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=50)
    data_ext.all_stock_df = temp_data_set.sort('Date', ascending=False)  # revese back to original

    print temp_data_set
    data_ext.all_stock_df.plot(x='Date', y=['Adj Close', '20d_ma', '50d_ma', 'Bol_upper', 'Bol_lower'])
    data_ext.all_stock_df.plot(x='Date', y=['Bol_BW', 'Bol_BW_200MA'])
    plt.show()
