# -*- coding: utf-8 -*-
"""
Created on Fri May 14 17:13:27 2021

script to download data from finviz https://finviz.com/quote.ashx?t=AAPL&p=d

@author: Michele
"""

import pandas as pd
import time

from config import *
import utils as ut


today_dd = date.today().strftime("%Y%m%d")

def main():

    start = time.time()

    ### get ticker list from excel file with universe
    tickers = ut.get_ticker_list(ticker_list)

    ###### tickers for testing
    # tickers = ['aapl', 'f', 'tr', 'mfg', 'meta', 'fb'] 

    ### get dataframe with data for all tickers
    result, no_data_list = ut.get_fundamentals(tickers)
    print(result)

    no_data_list.to_excel(dir_control_file + 'no_data_list.xlsx')

    ### map industry and sector string in numbers
    result['Industry'] = result['Industry'].map(industry_map)
    result['Sector'] = result['Sector'].map(sector_map)

    ### fix values and column
    result = result.replace('-', 0)
    result[['Short Float', 'Ratio']] = result['Short Float / Ratio'].str.split('/', 1, expand=True)

    ### change %, K, M and B string in numbers                 
    for col in col_list:
        result[col] = result[col].apply(ut.value_to_float)

    ### keep columns needed for machine learning    
    result = result[col_to_keep]
    result = result.set_index('Ticker')

    ### drop line with more than 5 nan and fill others
    result = result.dropna(thresh=5)
    result = result.apply(pd.to_numeric).fillna(0)

    ### drop sharpe ratio too high (M&A?) and too low vol (acquisition ongoing?)
    result['sharpe_ratio'] = result['Perf Month'] / result['Volatility M']
    result = result[(result['Volatility M'] >0.5)]
    result = result[(result['sharpe_ratio'] <10)]

    result.to_excel(dir_control_file + 'fundamental_db_num_' + today_dd + '.xlsx')
    result.to_pickle(dir_output + 'fundamental_db_num_' + today_dd + '.pkl')

    time.sleep(2)
    end = time.time() 
    elapsed_time = end - start
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

main()    
