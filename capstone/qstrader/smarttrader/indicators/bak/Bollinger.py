# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:59:24 2016
@author: victor
"""

import numpy as np
import pandas as pd
import qstrader.common.Util as util
import datetime

class Bollinger():
    
    def __init__(self, window_length = 20, dev_factor=2):
        self.window = window_length
        self.dev = dev_factor
    
    def addPriceSeries(self, historical):
        self.historical = historical
        
    def getIndicator(self):
        #Compute rolling mean and std    
        ma = pd.rolling_mean(self.historical, window = self.window)
        sd = pd.rolling_std(self.historical, window = self.window)
        
        #Normalized indicator
        bollinger_ind = (self.historical - ma) / ( 2 * sd)
                
        #Rename dataframe
        return bollinger_ind.rename( columns=lambda x: "Bollinger_" + x)
        
        
def test_run():
    """Driver function."""

    ticker_weights = {
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

    util.downloadData(ticker_weights, start_date.timetuple()[0:3], end_date.timetuple()[0:3])

    for ticket, wgt in ticker_weights.iteritems():
        results = util.get_data(ticket)

        indicator = Bollinger()
        indicator.addPriceSeries(results )
    
        print indicator.getIndicator()
    

if __name__ == "__main__":
    test_run()
