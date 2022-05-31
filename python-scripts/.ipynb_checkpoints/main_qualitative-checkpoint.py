"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
from main_helpers import *
from functools import reduce

'''
Qualitative data analysis script: Gathering of answers to open questions in csv along with conditions
'''

#Extraction of answers to open questions, renaming conditions and creation of anonymised dataset (without participant IDs)
def free_questions(quest, part):    
    df_quest = quest.loc[quest['type'] == 'goalsystem_questions']
    df_cond = part[['id', 'condition']]
    df_cond.rename(columns={'id':'participant'}, inplace=True)
    df_pivot = df_quest.pivot(index = 'participant', columns='question', values='answer')
    df = df_pivot.merge(df_cond, on='participant')
    df['condition'].replace({'1':'Sunburst'}, inplace = True)
    df['condition'].replace({'2':'Treemap'}, inplace = True)
    df['condition'].replace({'3':'Dendrogram'}, inplace = True)
    df['condition'].replace({'4':'Circlepacking'}, inplace = True)
    df.name = 'open-questions-pivot'
    create_csv(df) 
    df_anonym = df[['Was hat dir am wenigsten am Zielsystem gefallen?', 'Was hat dir besonders an dem Zielsystem gefallen?', 'Weitere Anmerkungen zu dem Zielsystem?']].copy()
    df_anonym.name = 'open-questions-anonym'
    create_csv(df_anonym)
    return df
    
      
    



if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    question_path = set_question_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    quest = question(participant_list, question_path)
    
    #call function
    free_questions(quest, participant_df)
    
    
