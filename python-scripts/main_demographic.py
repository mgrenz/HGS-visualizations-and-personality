"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from main_helpers import *
import seaborn as sns
from plotnine import *
import ast

"""
Extract demographic information: Gender and age distribution, number of completed semesters, study tracks, computer experience and studytool usage. 
"""

#Summary Statistics of age and semster number
def sum_stat(df):
    total_sum = participant_df[['age', 'semester']].describe()
    total_count = participant_df[['id']].count()    
    return total_sum, total_count

#Gender distribution
def gender_count(df):
    gender_counts = participant_df[['id', 'gender']].groupby('gender').count()
    return gender_counts


#Computer experience of participants
def pc_experience_count(df):
    #get relevant columns
    h_df = df[['id', 'additional_data']]
    
    #transform into dictionary
    i = 0
    for i in h_df.index:
        h_df['additional_data'][i] = ast.literal_eval(h_df['additional_data'][i])
    
    #get computer handling
    option1 = "Ich fühle mich im Umgang mit Computern sicher und finde mich in neuen Programmen intuitiv und schnell zurecht."
    option2 = "Ich fühle mich im Umgang mit Computern sicher, aber finde mich in neuen Programmen nicht intuitiv zurecht."
    option3 = "Ich fühle mich im Umgang mit Computern unsicher, aber finde mich in neuen Programmen intuitiv zurecht."
    option4 = "Ich fühle mich im Umgang mit Computern unsicher und finde mich in neuen Programmen nicht intuitiv zurecht."
    
    count_o1 = 0
    count_o2 = 0
    count_o3 = 0
    count_o4 = 0
    
    #select keys 'computer_handling'
    i=0
    for i in h_df.index:
        h_df['additional_data'][i] = {key: h_df['additional_data'][i][key] for key in h_df['additional_data'][i].keys() & {'computer_handling'}}
    
    #count occurences of options
    i = 0
    for i in h_df.index:
        if option1 in h_df['additional_data'][i].values():
            count_o1 = count_o1 + 1
        if option2 in h_df['additional_data'][i].values():
            count_o2 = count_o2 + 1
        if option3 in h_df['additional_data'][i].values():
            count_o3 = count_o3 + 1
        if option4 in h_df['additional_data'][i].values():
            count_o4 = count_o4 + 1
        else:
            continue
        
    #list counts and names
    answer_counts = [count_o1, count_o2, count_o3, count_o4]
    names = ['confident computer usage, intuitive program understanding', 'confident computer usage, no intuitive program understanding', 'no confident computer usage, intuitive program understanding', 'no confident computer usage, no intuitive program understanding']
    
    data = {'Object':names, 'counts': answer_counts}
    pc_data = pd.DataFrame(data)
 
 
    return pc_data
    
    
    data = participant_df[['id', 'additional_data']]
    return data
    

#Study subjects with associated amount of participants
def studysubject(df):
    study_subject_counts = df[['subject']].value_counts()
    study_subject_total = df[['subject']].count()
    return study_subject_counts, study_subject_total


#Studytool usage
def studytool_use(df):
    #get relevant columns
    pc_df = participant_df[['id', 'additional_data']]
    #transform additional data from string format to dictionary format
    i = 0
    for i in pc_df.index:
        pc_df['additional_data'][i] = ast.literal_eval(pc_df['additional_data'][i])
        
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    
    #select relevant keys and save them into seperate columns
    pc_df.loc[:,'studytool'] = 0
    pc_df.loc[:,'consulting'] = 0
    i=0
    for i in pc_df.index:
        pc_df['studytool'][i] = {key: pc_df['additional_data'][i][key] for key in pc_df['additional_data'][i].keys() & {'studytool_used'}}
        pc_df['consulting'][i] = {key: pc_df['additional_data'][i][key] for key in pc_df['additional_data'][i].keys() & {'consulting_requested'}}
        
    #count occurences of options
    i = 0
    for i in pc_df.index:
        if 'yes' in pc_df['studytool'][i].values():
            count1 = count1 + 1
        if 'no' in pc_df['studytool'][i].values():
            count2 = count2 + 1
        if 'yes' in pc_df['consulting'][i].values():
            count3 = count3 + 1
        if 'no' in pc_df['consulting'][i].values():
            count4 = count4 + 1
        else:
            continue
    answer_counts = [count1, count2, count3, count4]
    names = ['studytool used', 'no studytool used', 'consulting requested', 'no consulting requested']
    data = {'Object':names, 'counts': answer_counts}
    studytool_df = pd.DataFrame(data)
    return studytool_df    


if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path).fillna(0)
    

    #call functions and print output                                           
    print("Summary Statistic")                                           
    print(sum_stat(participant_df))
    print(" ")
    print("Gender distribution")
    print(gender_count(participant_df))
    print(" ")
    print("Computer handling")
    print(pc_experience_count(participant_df))
    print(" ")
    print("Study subjects")
    print(studysubject(participant_df))
    print(" ")
    print("Study tools")
    print(studytool_use(participant_df))                                                   
                                                       
                                             
                                                       
                                            
    
