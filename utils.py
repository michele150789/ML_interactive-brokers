# -*- coding: utf-8 -*-
"""
Created on Fri May 14 17:13:27 2021

@author: Michele
"""

import pandas as pd
from pandas import DataFrame
import time
import pickle
from finvizfinance.quote import finvizfinance
import yahoo_fin.stock_info as si

### ticker for data downloader
def get_ticker_list(input_ticker):    
    ticker_list = pd.read_excel(input_ticker, header=None)
    ticker_list = ticker_list.values.T[0].tolist()
    
    return ticker_list

#### main function to download data from https://finviz.com/quote.ashx?t=KPRX&p=d
def get_fundamentals(stock_list):
    result = pd.DataFrame()
    no_data_list = []
    no_data_list_final = []
    count=0

    for ticker in stock_list:
        time.sleep(2)
        count = count +1        
        try:
            stock = finvizfinance(ticker)
            stock_fundament = stock.ticker_fundament()
            #print(stock_fundament)        
            df = pd.DataFrame(data=stock_fundament, index=[0])        
            df['Ticker'] = ticker
            #print(df)
            result = pd.concat([result, df], ignore_index=True, sort=False)
        except Exception as e:
            print(count)
            print(e)
            no_data_list.append(ticker)
    
    time.sleep(60)
    for ticker in no_data_list:
        time.sleep(2)
        #print(ticker)
        try:
            stock = finvizfinance(ticker)
            stock_fundament = stock.ticker_fundament()
            #print(stock_fundament)        
            df = pd.DataFrame(data=stock_fundament, index=[0])        
            df['Ticker'] = ticker
            print(df)
            result = pd.concat([result, df], ignore_index=True, sort=False)
        except:
            no_data_list_final.append(ticker)      
    
    no_data_list_final = pd.DataFrame(no_data_list_final)

    return result, no_data_list_final    


def get_price(stock):
    print(stock)
    try:
        stock = finvizfinance(stock)
        stock_fundament = stock.ticker_fundament() 
        price = float(stock_fundament['Price'])
    
    except:
        price = si.get_live_price(stock)

    print(price)
    return price

   
def get_open_position(df, account):
    df = DataFrame(df)
    df['contract'] = df['contract'].astype(str)
    df[['contract','contract2']]=df.contract.str.split('(', 1, expand=True)
    df = df[df['contract']=='Stock']
    df = df[df['account']== account]
    df[['contract2','contract3','contract4']]=df.contract2.str.split(',', 2, expand=True)
    df = df.drop(['contract2', 'contract4'],axis=1)
    df[['symbol','ticker']]=df.contract3.str.split('=', 1, expand=True)
    df = df.drop(['contract3', 'symbol'],axis=1)
    df['ticker'] = list(map(lambda x: x[1:-1], df['ticker'].values))

    return df

def get_account_value(df,account):
    df = DataFrame(df)
    df = df[(df['tag']=='NetLiquidation')&(df['account']==account)]
    account_value= float(df.iloc[0]['value'])

    return account_value

def holding_analysis(df_open_position,stock_to_buy_list):
    keep_stock=[]
    sell_stock=[]
    for x in df_open_position['ticker']:
        if x in stock_to_buy_list:
            keep_stock.append(x)
        else:
            sell_stock.append(x)
    
    return keep_stock,sell_stock
   
def stock_holding_quantity(df_open_position,ticker,account):
    df_open_position = df_open_position[(df_open_position['ticker']==ticker)&(df_open_position['account']==account)]
    port_quantity = int(df_open_position.iloc[0]['position'])

    return port_quantity


def prepare_result(result,number_of_stocks):

    result = result.dropna(thresh=5)
    result = result.fillna(0)
    result = result.loc[~(result==0).all(axis=1)]
    
    result = result.sort_values(by='sharpe_ratio_t0', ascending = False)
    result = result[(result['sharpe_ratio_t0'] <15)]
    result = result[(result['Volatility M'] >0.6)]
    
    result.loc[result.index[:number_of_stocks], 'decile'] = 1
    result.loc[result.index[number_of_stocks:], 'decile'] = 0
    
    print(result)
    return result


def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if '%' in x:
        if len(x) > 1:
            return float(x.replace('%', ''))
        return 'error'
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    return 0.0


def get_stock_to_buy_for_each_bucket(ml_model_file, today_df):
 
    loaded_model = pickle.load(open(ml_model_file, 'rb'))
    today_df['prediction'] = loaded_model.predict(today_df)        
    today_df = today_df[today_df['prediction']==1]
    stock_to_buy = today_df.index.values.tolist()    
       
    return today_df, stock_to_buy


