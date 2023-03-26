# -*- coding: utf-8 -*-
"""
Created on Fri May 14 18:13:01 2021

@author: Michele
"""
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

import operator
import time
import pickle
import pandas as pd

import config as cf
import utils as ut


def train_model(result, number_of_stock):
     
    X = result.iloc[:,:-2] # excluding 'sharpe_ratio_t0', 'decile'
    y = result.iloc[:,-1] # taking deciles

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30) 
    #X_train.to_excel(cf.dir_control_file + f'X_train_{number_of_stock}.xlsx')
    #y_train.to_excel(cf.dir_control_file + f'y_train_{number_of_stock}.xlsx')  
    
    random_forest = RandomForestClassifier(n_estimators=300)
    neural_network = MLPClassifier(alpha=1, max_iter=1000)
    neighbors = KNeighborsClassifier(3)

    scores_rf = cross_val_score(random_forest, X_train, y_train, cv=4)
    scores_nn = cross_val_score(neural_network, X_train, y_train, cv=4)
    scores_neig = cross_val_score(neighbors, X_train, y_train, cv=4)

    print("%0.2f accuracy with a standard deviation of %0.2f" % (scores_rf.mean(), scores_rf.std()))
    print("%0.2f accuracy with a standard deviation of %0.2f" % (scores_nn.mean(), scores_nn.std()))
    print("%0.2f accuracy with a standard deviation of %0.2f" % (scores_neig.mean(), scores_neig.std()))
          
    random_forest.fit(X_train, y_train)
    neural_network.fit(X_train, y_train)
    neighbors.fit(X_train, y_train) 
    
    yhat_rf = random_forest.predict(X_test)
    yhat_nn = neural_network.predict(X_test)
    yhat_neig = neighbors.predict(X_test)
     
    # evaluate predictions
    acc_rf = accuracy_score(y_test, yhat_rf)  
    acc_nn = accuracy_score(y_test, yhat_nn)
    acc_neig = accuracy_score(y_test, yhat_neig)
    
    models_res =  {'acc_rf':acc_rf, 'acc_nn':acc_nn, 'acc_neig': acc_neig}

    # pick the model with highest accuracy
    best_model = max(models_res.items(), key=operator.itemgetter(1))[0]
    print(best_model)
         
    # save the best moodel in finalized_model.sav
    if best_model == 'acc_rf':             
        pickle.dump(random_forest, open(f"{cf.path}\ml_models\\finalized_model_{number_of_stock}.sav", 'wb'))
        model = random_forest 
    elif best_model == 'acc_nn':
        pickle.dump(neural_network, open(f"{cf.path}\ml_models\\finalized_model_{number_of_stock}.sav", 'wb'))
        model = neural_network 
    else:
        pickle.dump(neighbors, open(f"{cf.path}\ml_models\\finalized_model_{number_of_stock}.sav", 'wb'))
        model = neighbors 
  
    print('Accuracy_rf: %.3f' % acc_rf)
    print('Accuracy_nn: %.3f' % acc_nn)
    print('Accuracy_neig: %.3f' % acc_neig)    
    return model


def prepare_df_for_ml(number_of_stocks, today, one_month):
    """
    the goal of this function is prepare a dataframe to train the model. The final dataframe is made of data of previuos month (t-1) and the relavitve sharpe ratio 
    recorded after ~30 days (t). ML should classify the stocks based on old data and actual sharpe ratio.
    """

    # upload fundamentals downloaded today #######################################    update file date   ##############################################################
    #fund = pd.read_pickle(r'C:\Users\Michele\Desktop\ib_code\data\fundamental_db_num_'+today+'.pkl')
    data_today = pd.read_pickle(cf.dir_output + 'fundamental_db_num_' + today +'.pkl')
    print(today)
    print(data_today.head(5))
    data_today = data_today[(data_today['sharpe_ratio'] <15)]
    data_today = data_today[(data_today['Volatility M'] >0.6)]
    
    # upload fundamentals downloaded 1 months ago ##################################   update file date   ##############################################################
    #fund_prev_month = pd.read_pickle(r'C:\Users\Michele\Desktop\ib_code\data\fundamental_db_num_'+one_month+'.pkl')
    data_prev_month = pd.read_pickle(cf.dir_output + 'fundamental_db_num_'+ one_month +'.pkl')
    print(one_month)
    print(data_prev_month.head(5))

    #get sharpe ratio realized in the last month and merge with data of previous month
    result = pd.merge(data_prev_month, data_today[["sharpe_ratio"]], on='Ticker', how="left")
    result = result.rename(columns={'sharpe_ratio_x':'sharpe_ratio', 'sharpe_ratio_y':'sharpe_ratio_t0',})
    print(result.head(5))
    result = ut.prepare_result(result,number_of_stocks)
        
    return result


def train_model_with_diff_number_of_stocks(number_of_stocks_list):
    """
    we run multiple machine learning training based on different buckets.
    Less is n, stronger is the prediction.
    """

    for n in number_of_stocks_list:
        data_to_train_ml = prepare_df_for_ml(n, cf.today, cf.one_month)
        data_to_train_ml = data_to_train_ml.reset_index()
        data_to_train_ml = data_to_train_ml[cf.col_to_keep_2]
        data_to_train_ml = data_to_train_ml.set_index('Ticker')

        train_model(data_to_train_ml, n)

def main():
    print(cf.one_month)

    start = time.time()
    train_model_with_diff_number_of_stocks(cf.number_of_stocks)
    end = time.time()
    elapsed_time = end - start    
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))


main()
