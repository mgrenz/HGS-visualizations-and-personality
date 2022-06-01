"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
from main_helpers import *
from main_bigfive import big5_questionnaire, open_subscale, score, total_scores
import main_sus


'''
Correlation between openness trait scores and System Usability Scale scores.
'''


#Linearity check with Linear Regression and plot of Openness and SUS scores
def check(dualx, dualy):
    res = stats.linregress(dualx, dualy)
    print(res)
    print(f"R-squared: {res.rvalue**2:.6f}")
    fig, ax = plt.subplots()    
    plt.scatter(dualx, dualy, label = 'Original data') 
    plt.plot(dualx, res.intercept + res.slope*dualx, 'r', label = 'Linear regression model')
    plt.xlabel('Openness trait score (arb. unit)')
    plt.ylabel('SUS score (arb. unit)')
    plt.legend(loc='lower left')
    plt.show()
    #plt.savefig('hypo2-open-usability')
    return fig, ax

#calculation of Spearman's rank correlation coefficient
def spearman(dual):
    spear = stats.spearmanr(dual['big5-open'], dual['total_score'])
    return spear




if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    item_path = set_item_path()
   

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset_item = item(participant_list, item_path)
    
    
    #get openness subscale
    big5_all = big5_questionnaire(subset_item)
    big5_open = open_subscale(big5_all)
    open_scores = score(big5_open)

    
    #get sus scores
    sus_all = main_sus.sus_questionnaire(subset_item)
    sus_scores = main_sus.score(sus_all)

    
    #merge sus and open dfs
    dual = open_scores.merge(sus_scores, on = 'participant')
    dual.name = 'openness-sus-df'
  
    #create csv 
    create_csv(dual)

    #check linearity
    print("Linear Regresion result: ")
    check(dual['big5-open'], dual['total_score'])
    
    #Spearman's rank correlation coefficient calculation
    print("")
    print("Spearman's rank correlation coeffcient investigating a correlation between openness trait scores and SUS scores: ")
    print(spearman(dual))
    
  
    