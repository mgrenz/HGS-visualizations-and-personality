"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta

'''
Helper functions used throughout analyses scripts. Specification of paths necessary to change when running the scripts are indicated by 'CHANGE HERE:'.
'''


#define paths to data sets
def set_participant_path():
    #CHANGE HERE:
    return "~/Documents/Uni/siddata/analyses/final/data-sets/participant-data.csv"

def set_item_path():
    #CHANGE HERE:
    return "~/Documents/Uni/siddata/analyses/final/data-sets/item-data.csv"

def set_goal_path():
    #CHANGE HERE:
    return "~/Documents/Uni/siddata/analyses/final/data-sets/goal-data.csv"

def set_question_path():
    #CHANGE HERE:
    return "~/Documents/Uni/siddata/analyses/final/data-sets/question-data.csv"



#function to save created data as csv files
def create_csv(dataframe):
    '''store df as csv file'''
    name = dataframe.name
    filename = '%s.csv' % name
    #CHANGE HERE:
    csv = dataframe.to_csv(f'~/Documents/Uni/siddata/data/04_trial/{filename}')
    print()
    print('csv sucessfully created')
    print('Name: ', name) 
    return csv



#extract data from participant file
def participant(participant_path):
    
    # read in participant csv file
    participant_df = pd.read_csv(participant_path)
    #remove test trials    
    participant_df.drop(participant_df[participant_df['subject'] == 'testt'].index, inplace = True)
    participant_df.drop(participant_df[participant_df['subject'] == 'Tesst'].index, inplace = True)
    participant_df.drop(participant_df[participant_df['subject'] == 'Testy'].index, inplace = True)
    participant_df.drop(participant_df[participant_df['subject'] == 'vfdbfdn'].index, inplace = True)
    participant_df.drop(participant_df[participant_df['subject'] == 'tester'].index, inplace = True)
    
    #drop prestudy
    participant_df.drop(participant_df[participant_df['id'] == 178].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 172].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 171].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 159].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 158].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 157].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 153].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 152].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 150].index, inplace = True)
    
    #drop unfinished participants    
    participant_df = participant_df[participant_df['finished'].notna()]
    
    #exclude participants 
    #based on constructed tree
    participant_df.drop(participant_df[participant_df['id'] == 401].index, inplace = True) 
    participant_df.drop(participant_df[participant_df['id'] == 274].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 245].index, inplace = True) 
    #based on b5 questionnaire honesty scale
    participant_df.drop(participant_df[participant_df['id'] == 244].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 254].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 261].index, inplace = True)
    participant_df.drop(participant_df[participant_df['id'] == 424].index, inplace = True)
    #based on b5 questionnaire plausibility value
    participant_df.drop(participant_df[participant_df['id'] == 420].index, inplace = True)
    
    participant_df.name = 'participant-main'
    return participant_df


#return list of participant ids
def participant_ids(participant_df):
    #solving len error
    pd.set_option("display.max_columns", None)
    #get list
    participant_list = participant_df['id']
    return participant_list


#extract data from item file
def item(participant_list, item_path):
    item_data = pd.read_csv(item_path)
    liste = participant_list
    item_df = item_data.iloc[np.where(item_data.participant.isin(liste))]
    item_df.name = 'item-main'
    return item_df


#extract data from goal file
def goal(participant_list, goal_path):
    goal_data = pd.read_csv(goal_path)
    liste = participant_list
    goal_df = goal_data.iloc[np.where(goal_data.participant.isin(liste))]
    goal_df.name = 'goal-main'
    return goal_df


#extract data from question file
def question(participant_list, question_path):
    question_data = pd.read_csv(question_path)
    liste = participant_list
    question_df = question_data.iloc[np.where(question_data.participant.isin(liste))]
    question_df.name = 'question-main'
    return question_df

