# -*- coding: utf-8 -*-
"""
Created on Fri May 14 17:13:27 2021

@author: Michele
"""
import utils as ut
import config as cf
import pandas as pd


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


get_buy_list()    