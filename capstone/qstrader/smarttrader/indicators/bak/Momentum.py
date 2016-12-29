# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:59:24 2016
@author: victor
"""

import numpy as np
import pandas as pd


class Momentum():
    
    def __init__(self, window_length = 5):
        self.window = window_length
    
    def addPriceSeries(self, historical):
        self.historical = historical
        
    def getIndicator(self):
        momentum = self.historical / self.historical.shift( self.window ) - 1
        
        #Rename dataframe
        return momentum.rename( columns=lambda x: "Momentum_" + x)
        
        
        
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
    
    indicator = Momentum()
    indicator.addPriceSeries( stock_prices )
    
    print indicator.getIndicator()
    

if __name__ == "__main__":
    test_run()
