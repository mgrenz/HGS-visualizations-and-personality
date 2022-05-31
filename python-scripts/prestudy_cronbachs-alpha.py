"""
date: 30.05.2022
author: Mae Grenz
"""

import pingouin as pg
import numpy as np
import pandas as pd
from prestudy_helpers import *
from datetime import datetime


'''
Calcualte Cronbach's Alpha to evaluate internal consistency of the complexity Likert Scale. 
'''
 
#extract complexity assessment and code Likert scale nummerically
def complexity_csv(item_df):
    
    #filter complexity assessments
    all_complexity_codes = ['complexity_assessment_1_1','complexity_assessment_1_2','complexity_assessment_1_3','complexity_assessment_1_4',
                       'complexity_assessment_2_1','complexity_assessment_2_2','complexity_assessment_2_3','complexity_assessment_2_4',
                       'complexity_assessment_3_1','complexity_assessment_3_2','complexity_assessment_3_3','complexity_assessment_3_4',
                       'complexity_assessment_4_1','complexity_assessment_4_2','complexity_assessment_4_3','complexity_assessment_4_4']
    all_complexity_quest = item_df.iloc[np.where(item_df.code.isin(all_complexity_codes))]
    all_complexity_quest.name = 'complexity-cond-all'
    
    #mark Likert scale items 2 and 4 fro reverse coding by setting the boolean variable to True
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_1_2', True, False)
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_1_4', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_2_2', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_2_4', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_3_2', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_3_4', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_4_2', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest['my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_4_4', True, all_complexity_quest['my_reverse_code'])
    
    #change answers to numerical indication according to coding scheme
    dict_to_numeric = {'trifft nicht zu' : 1,'trifft eher nicht zu' : 2, 'teils - teils' : 3, 'trifft eher zu' : 4, 'trifft zu' : 5} 
    reverse_dict_to_numeric = {'trifft nicht zu' : 5,'trifft eher nicht zu' : 4, 'teils - teils' : 3, 'trifft eher zu' : 2, 'trifft zu' : 1} 
    all_complexity_quest['answer_item'] = all_complexity_quest['given_answer']
    all_complexity_quest['answer_item'] = np.where(all_complexity_quest['my_reverse_code'] == True, all_complexity_quest['answer_item'].replace(reverse_dict_to_numeric), all_complexity_quest['answer_item'].replace(dict_to_numeric))
    
    #csv creation of entire complexity assessment 
    #create_csv(all_complexity_quest)
    return all_complexity_quest
    
    
    
#calculate cronbach's alpha
def cronbachs_alpha(complexity):

    ca = pg.cronbach_alpha(data=complexity, items='code', scores='answer_item', subject='participant')
    return ca


    
if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    item_path = set_item_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset = item(participant_list, item_path)
    
    #encode likert scales
    complexity_all = complexity_csv(subset)
    
    #calculate CAs
    result_all = cronbachs_alpha(complexity_all)
    
    #print CAs results
    print("Likert scale reliability check with Cronbach's alpha")
    print("Cronbach's alpha: ", result_all)
    