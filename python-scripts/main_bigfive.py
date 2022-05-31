"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
from main_helpers import *
from functools import reduce

'''
Big Five Analysis Script: Extraction of Big Five assessment and numerical coding of Likert scale respecting inverse coded items.
'''


#numerical coding of Likert scale
def big5_questionnaire(subset):
    #extract big5 subset
    big5_df = subset[subset['questionnaire'].str.contains('big_five')]
    big5_df.name = 'big5-questionnaire'
    #indicate items for reverse coding: True = reverse coding
    big5_df.loc[:,'my_reverse_code'] = False
    big5_df.loc[:,'my_reverse_code'] = np.where(big5_df['code'] == 'extra5', True, big5_df['my_reverse_code'])
    big5_df.loc[:,'my_reverse_code'] = np.where(big5_df['code'] == 'extra6', True, big5_df['my_reverse_code'])
    big5_df.loc[:,'my_reverse_code'] = np.where(big5_df['code'] == 'offen4', True, big5_df['my_reverse_code'])
    big5_df.loc[:,'my_reverse_code'] = np.where(big5_df['code'] == 'vertrag4', True, big5_df['my_reverse_code'])
    big5_df.loc[:,'my_reverse_code'] = np.where(big5_df['code'] == 'vertrag5', True, big5_df['my_reverse_code'])
    big5_df.loc[:,'my_reverse_code'] = np.where(big5_df['code'] == 'macht6', True, big5_df['my_reverse_code'])
    #change answer to numerical indication 
    dict_to_numeric = {'trifft nicht zu' : 1,'trifft eher nicht zu' : 2, 'trifft eher zu' : 3, 'trifft zu' : 4} 
    reverse_dict_to_numeric = {'trifft nicht zu' : 4,'trifft eher nicht zu' : 3, 'trifft eher zu' : 2, 'trifft zu' : 1} 
    big5_df.loc[:,'answer_item'] = big5_df['given_answer']
    big5_df.loc[:,'answer_item'] = np.where(big5_df['my_reverse_code'] == True, big5_df['answer_item'].replace(reverse_dict_to_numeric), big5_df['answer_item'].replace(dict_to_numeric))
    #return df with numerical answers already reverse coded
    return big5_df

   
    
#Extract subscales
def open_subscale(big5_df):
    open_df = big5_df[big5_df['code'].str.contains('offen')]
    open_df.name = 'big5-open'
    return open_df


def extra_subscale(big5_df):
    extra_df = big5_df[big5_df['code'].str.contains('extra')]
    extra_df.name = 'big5-extra'
    return extra_df


def neuro_subscale(big5_df):
    neuro_df = big5_df[big5_df['code'].str.contains('neuro')]
    neuro_df.name = 'big5-neuro'
    return neuro_df


def cons_subscale(big5_df):
    cons_df = big5_df[big5_df['code'].str.contains('gewissen')]
    cons_df.name = 'big5-cons'
    return cons_df


def agree_subscale(big5_df):
    agree_df = big5_df[big5_df['code'].str.contains('vertrag')]
    agree_df.name = 'big5-agree'
    return agree_df


def safe_subscale(big5_df):
    safe_df = big5_df[big5_df['code'].str.contains('sicher')]
    safe_df.name = 'big5-safety'
    return safe_df


def power_subscale(big5_df):
    power_df = big5_df[big5_df['code'].str.contains('macht')]
    power_df.name = 'big5-power'
    return power_df


def perform_subscale(big5_df):
    perform_df = big5_df[big5_df['code'].str.contains('leistung')]
    perform_df.name = 'big5-performance'
    return perform_df


def honest_subscale(big5_df):
    honest_df = big5_df[big5_df['code'].str.contains('ehrlich')]
    honest_df.name = 'big5-honesty'
    return honest_df




#Calculation of trait scores per participant
def score(subscale):
    score_df = subscale.groupby('participant', as_index=False).agg({'answer_item': 'sum'})
    score_df.rename(columns={'answer_item': subscale.name}, inplace = True)
    score_df.name = 'score_%s' % subscale.name
    return score_df


#Scores of all subscales
def total_scores(big5_df):
    #create subscale scores
    df_o = score(open_subscale(big5_df))
    df_c = score(cons_subscale(big5_df))
    df_e = score(extra_subscale(big5_df))
    df_a = score(agree_subscale(big5_df))
    df_n = score(neuro_subscale(big5_df))
    df_h = score(honest_subscale(big5_df))
    df_s = score(safe_subscale(big5_df))
    df_po = score(power_subscale(big5_df))
    df_pe = score(perform_subscale(big5_df))
    # merge subscale score dfs
    df_list = [df_o, df_c, df_e, df_a, df_n, df_s, df_po, df_pe, df_h]
    df_total_scores = reduce(lambda left, right: pd.merge(left,right,on=['participant'], how='inner'), df_list)
    df_total_scores.loc[:,'honesty-caution'] = np.where(df_total_scores['big5-honesty'] < 7, True, False)
    df_total_scores.name = 'big5-all-scores'
    return df_total_scores



#Function for calculating plausibility value
def plau_calc(big5_df):
    neuro2 = big5_df.loc[big5_df['code'] == 'neuro2', 'answer_item'].iloc[0]
    neuro7 = big5_df.loc[big5_df['code'] == 'neuro7', 'answer_item'].iloc[0]
    extra10 = big5_df.loc[big5_df['code'] == 'extra10', 'answer_item'].iloc[0]
    extra1 = big5_df.loc[big5_df['code'] == 'extra1', 'answer_item'].iloc[0]
    gewissen2 = big5_df.loc[big5_df['code'] == 'gewissen2', 'answer_item'].iloc[0]
    gewissen1 = big5_df.loc[big5_df['code'] == 'gewissen1', 'answer_item'].iloc[0]
    offen6 = big5_df.loc[big5_df['code'] == 'offen6', 'answer_item'].iloc[0]
    offen1 = big5_df.loc[big5_df['code'] == 'offen1', 'answer_item'].iloc[0]
    vertrag2 = big5_df.loc[big5_df['code'] == 'vertrag2', 'answer_item'].iloc[0]
    vertrag1 = big5_df.loc[big5_df['code'] == 'vertrag1', 'answer_item'].iloc[0]
    #calculate plausibility value 
    p = 1 - ((((neuro2 - neuro7) ** 2 ) + ((extra10 - extra1) ** 2) + ((gewissen2 - gewissen1) ** 2) + ((offen6 - offen1) ** 2) + ((vertrag2 - vertrag1) ** 2)) / 45) 
    return p
    

#apply plau_calc 
def plausibility_check(big5_df):
    plau_df = total_scores(big5_df)
    plau_list = big5_df.groupby(['participant']).apply(plau_calc)
    plau_df['plau-value'] = np.array(plau_list)
    plau_df.loc[:,'plau-caution'] = np.where(plau_df['plau-value'] < 0.8, True, False)
    plau_df.name = 'b5-plausibility_check'
    return plau_df
   

    
    
    



if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    item_path = set_item_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset = item(participant_list, item_path)
    
    #functions for big5
    big5_df = big5_questionnaire(subset)
    create_csv(big5_df)
    b5 = total_scores(big5_df)
    create_csv(b5)
    
    #plausibility check
    create_csv(plausibility_check(big5_df))
    create_csv(score(cons_subscale(big5_df)))

 
  




