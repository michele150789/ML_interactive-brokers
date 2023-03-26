# -*- coding: utf-8 -*-
"""
Created on Fri May 14 17:13:27 2021

@author: Michele
"""
from ib_insync import *
import src.utils as ut
import src.config as cf
import pandas as pd
#from src.get_buy_list import *

#####  settings  #######
account = 'DU2333834'
leverage = 0.01 # account usage
limit_tolerance = 0.015 # upper limit for buy order and lower limit for sell order (large enough to execute it 1.5%)
#######################
def get_buy_list():
    final_df = pd.DataFrame()
    for n in cf.number_of_stocks:
        print(n)
        data_today = pd.read_pickle(cf.dir_output + 'fundamental_db_num_' + cf.today + '.pkl')
        today_df, stock_to_buy = ut.get_stock_to_buy_for_each_bucket(f"{cf.path}\ml_models\\finalized_model_{n}.sav", data_today)
        today_df = today_df.reset_index()
        today_df['bucket'] = today_df.apply(lambda x: n, axis=1)       
        #today_df.loc[:,'bucket'] = n
        final_df = pd.concat([final_df, today_df])    
        today_df.to_excel(f"{cf.path}\stock_to_buy\stock_to_buy_{n}.xlsx")
        print(stock_to_buy)

    print(len(final_df))
    final_df = final_df.reset_index()
    final_df = final_df.drop_duplicates(subset='Ticker', keep='first')    
    if len (final_df) > 10:
        final_df = final_df.drop_duplicates(subset='Industry', keep='first')
        final_df = final_df[:10]
    else:
        final_df

    final_df.to_excel(f"{cf.path}\stock_to_buy\stock_to_buy_final.xlsx")
    print(len(final_df))

    stock_to_buy_list_final = final_df['Ticker'].values.tolist()

    print(f'stock_to_buy_list={stock_to_buy_list_final}')
    print(f'stock_to_buy_list: {len(stock_to_buy_list_final)}')

    return stock_to_buy_list_final

# Interactive brokers connection
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=999)
position_ib = ib.positions(account)
print(position_ib)
account_summary = ib.accountSummary(account)

# upload today data
data_today = pd.read_pickle(cf.dir_output + 'fundamental_db_num_' + cf.today + '.pkl')
#data_today = pd.read_pickle(cf.dir_output + 'fundamental_db_num_' + '05232022' + '.pkl')

# get the new fundamental in get_stock_to_buy
# get list of stock to buy using the ML model saved
stock_to_buy_list = get_buy_list()
print(f'stock_to_buy_list={stock_to_buy_list}')


df_open_position={}
if not position_ib:
    keep_stock = []
    sell_stock = []

else:
    df_open_position = ut.get_open_position(position_ib,account)
    keep_stock,sell_stock = ut.holding_analysis(df_open_position,stock_to_buy_list)
    print(f'keep_stock={keep_stock}')
    print(f'sell_stock={sell_stock}')


print(f'holdings={df_open_position}')
account_value = ut.get_account_value(account_summary,account)
print(f'account_value={account_value}')

if len(stock_to_buy_list) == 0:
    usd_amount_each_stock = 0
else:
    usd_amount_each_stock = account_value*leverage/10


for x in sell_stock:     
    all_position = ut.stock_holding_quantity(df_open_position,x,account) 
    price = ut.get_price(x)
    limit = round(float(price*(1-limit_tolerance)),1)
    stock = Stock(x, 'SMART', 'USD')
    limitOrder = LimitOrder('SELL', all_position, limit)
    limitTrade = ib.placeOrder(stock, limitOrder)
    ib.sleep(2)

for x in stock_to_buy_list:
    # list keep stock is empty
    if not keep_stock:
        price = ut.get_price(x)
        desire_quantity = int(usd_amount_each_stock/price)
        limit = round(float(price*(1+limit_tolerance)),1)
        stock = Stock(x, 'SMART', 'USD')
        limitOrder = LimitOrder('BUY', desire_quantity, limit)
        limitTrade = ib.placeOrder(stock, limitOrder)
        ib.sleep(2)        
    else:
        # ticker is not in keep stock list           
        if x not in keep_stock:
            price = ut.get_price(x)
            desire_quantity = int(usd_amount_each_stock/price)
            limit = round(float(price*(1+limit_tolerance)),1)
            stock = Stock(x, 'SMART', 'USD')
            limitOrder = LimitOrder('BUY', desire_quantity, limit)
            print(limit)
            limitTrade = ib.placeOrder(stock, limitOrder)
            ib.sleep(2)
        else:
            price = ut.get_price(x)
            desire_quantity = int(usd_amount_each_stock/price)
            holding_quantity = ut.stock_holding_quantity(df_open_position,x,account)
            # rebalancing the existing position depending on the holding quantity
            if holding_quantity>desire_quantity:
                sell_quantity = holding_quantity - desire_quantity
                limit = round(float(price*(1-limit_tolerance)),1)
                stock = Stock(x, 'SMART', 'USD')
                limitOrder = LimitOrder('SELL', sell_quantity, limit)
                limitTrade = ib.placeOrder(stock, limitOrder)
                ib.sleep(2)
            elif holding_quantity<desire_quantity:
                buy_quantity = desire_quantity - holding_quantity
                limit = round(float(price*(1+limit_tolerance)),1)
                stock = Stock(x, 'SMART', 'USD')
                limitOrder = LimitOrder('BUY', buy_quantity, limit)
                limitTrade = ib.placeOrder(stock, limitOrder)
                ib.sleep(2)
            else:
                pass

        

        
    





