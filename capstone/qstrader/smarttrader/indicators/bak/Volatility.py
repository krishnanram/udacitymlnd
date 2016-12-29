# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:59:24 2016
@author: victor
"""

import numpy as np
import pandas as pd


class Volatility():
    
    def __init__(self, window_length = 20):
        self.window = window_length
    
    def addPriceSeries(self, historical):
        self.historical = historical
        
    def getIndicator(self):
        returns_series = self.historical / self.historical.shift( 1 ) - 1
        std_series = pd.rolling_std(returns_series, window = self.window)
        std_series = std_series * np.sqrt(255)
        
        #Rename dataframe
        return std_series.rename( columns=lambda x: "Volatility_" + x)
        
        
def test_run():
    """Driver function."""
    
    from util import get_data
    
    # Define input parameters
    start_date = '2007-12-31'
    end_date = '2009-12-31'
    stock_symbol = ["IBM", "AAPL", "GE", "GLD", "SPY"]

    #Get stock quotation
    dates =  pd.date_range(start_date, end_date)
    stock_prices = get_data(stock_symbol, dates, addSPY=False)
    
    indicator = Volatility()
    indicator.addPriceSeries( stock_prices )
    
    print indicator.getIndicator()
    

if __name__ == "__main__":
    test_run()
