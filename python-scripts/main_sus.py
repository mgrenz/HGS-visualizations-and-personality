"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
from main_helpers import *

'''
System Usability Scale (SUS) Analysis Script
'''

def sus_questionnaire(subset):
    #extract sus subset
    sus_df = subset[subset['questionnaire'].str.contains('sus')]
    sus_df.name = 'sus-questionnaire'
    #change answer to numerical indication 
    dict_to_numeric = {'trifft nicht zu' : 0,'trifft eher nicht zu' : 1, 'teils - teils' : 2, 'trifft eher zu' : 3, 'trifft zu' : 4} 
    #rename column
    sus_df.loc[:,'answer_item'] = sus_df['given_answer']
    sus_df.loc[:,'answer_item'] = sus_df['answer_item'].replace(dict_to_numeric)
    #even question: 5 - answer
    even_codes = ['sus_2','sus_4', 'sus_6', 'sus_8', 'sus_10']
    sus_df.loc[sus_df.code.isin(even_codes),'answer_alteration'] = (5 - sus_df['answer_item'])
    #odd questions: answer - 1
    odd_codes = ['sus_1','sus_3', 'sus_5', 'sus_7', 'sus_9']
    sus_df.loc[sus_df.code.isin(odd_codes),'answer_alteration'] = (sus_df['answer_item'] - 1)
    return sus_df

#Calculation of sus score per participant: Sum of answers multiplied by 2.5
def score(sus_df):
    #sum of answers per participant 
    score_df = sus_df.groupby('participant', as_index=False).agg({'answer_alteration': 'sum'})
    score_df.rename(columns={'answer_alteration': 'total_score'}, inplace = True)
    #multiply sum by 2.5 to transfer scale to range of 0 - 100
    score_df['total_score'] = score_df['total_score'].multiply(2.5)
    score_df.name = 'sus-scores'
    return score_df




if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    item_path = set_item_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset = item(participant_list, item_path)
    
    #SUS functions 
    sus_df = sus_questionnaire(subset)
    scores = score(sus_df)
    
    #csv creation
    create_csv(sus_df)
    create_csv(scores)
    
   