"""
date: 30.05.2022
author: Mae Grenz
"""

import pingouin as pg
import numpy as np
import pandas as pd
from main_helpers import *
from matplotlib import pyplot as plt
import seaborn as sb


''' 
Calculation of Complexity Scores for Vizualizations. The higher the score, the more complex the HGS visualization was perceived.
'''


#Numerical coding of complexity Likert scale.'''
def complexity(subset):
    #get all complexity assessments
    all_complexity_codes = ['complexity_assessment_1_1','complexity_assessment_1_2','complexity_assessment_1_3','complexity_assessment_1_4',
                       'complexity_assessment_2_1','complexity_assessment_2_2','complexity_assessment_2_3','complexity_assessment_2_4',
                       'complexity_assessment_3_1','complexity_assessment_3_2','complexity_assessment_3_3','complexity_assessment_3_4',
                       'complexity_assessment_4_1','complexity_assessment_4_2','complexity_assessment_4_3','complexity_assessment_4_4']
    all_complexity_quest = subset.iloc[np.where(subset.code.isin(all_complexity_codes))]
    all_complexity_quest.name = 'complexity-cond-all'
    #indicate items for reverse coding: True = reverse coding
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_1_2', True, False)
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_1_4', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_2_2', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_2_4', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_3_2', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_3_4', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_4_2', True, all_complexity_quest['my_reverse_code'])
    all_complexity_quest.loc[:,'my_reverse_code'] = np.where(all_complexity_quest['code'] == 'complexity_assessment_4_4', True, all_complexity_quest['my_reverse_code'])
    #change answer to numerical indication: 7 point likert scale
    dict_to_numeric = {'trifft überhaupt nicht zu' : 1,'trifft nicht zu' : 2, 'trifft eher nicht zu' : 3, 'teils-teils' : 4, 'trifft eher zu' : 5, 'trifft zu' : 6, 'trifft vollkommen zu' : 7} 
    reverse_dict_to_numeric = {'trifft überhaupt nicht zu' : 7,'trifft nicht zu' : 6, 'trifft eher nicht zu' : 5, 'teils-teils' : 4, 'trifft eher zu' : 3, 'trifft zu' : 2, 'trifft vollkommen zu' : 1} 
    all_complexity_quest['answer_item'] = all_complexity_quest['given_answer']
    all_complexity_quest['answer_item'] = np.where(all_complexity_quest['my_reverse_code'] == True, all_complexity_quest['answer_item'].replace(reverse_dict_to_numeric), all_complexity_quest['answer_item'].replace(dict_to_numeric)) 
    return all_complexity_quest


#Mean complexity score calculation
def score(condition):
    number_of_participants = condition['participant'].nunique()
    score_df = condition.groupby('questionnaire', as_index=False).agg({'answer_item': 'sum'})
    score_df.rename(columns={'answer_item': 'total_score'}, inplace = True)
    score_df['mean_score'] = score_df['total_score'] / number_of_participants
    score_df['nr_of_participants'] = number_of_participants
    score_df['questionnaire'].replace({'complexity_assessment_1':'Sunburst'}, inplace = True)
    score_df['questionnaire'].replace({'complexity_assessment_2':'Treemap'}, inplace = True)
    score_df['questionnaire'].replace({'complexity_assessment_3':'Dendrogram'}, inplace = True)
    score_df['questionnaire'].replace({'complexity_assessment_4':'Circlepacking'}, inplace = True)
    score_df.name = 'complexity-scores'
    return score_df


#Complexity score calculation per participant
def part_score(df):
    part_score = df.groupby(['participant', 'questionnaire'], as_index=False).agg({'answer_item':'sum'})
    part_score.rename(columns={'answer_item': 'total_score'}, inplace = True)
    part_score['questionnaire'].replace({'complexity_assessment_1':'Sunburst'}, inplace = True)
    part_score['questionnaire'].replace({'complexity_assessment_2':'Treemap'}, inplace = True)
    part_score['questionnaire'].replace({'complexity_assessment_3':'Dendrogram'}, inplace = True)
    part_score['questionnaire'].replace({'complexity_assessment_4':'Circlepacking'}, inplace = True)
    return part_score


#Plot complexity scores
def bar(df):
    fig,ax = plt.subplots()
    sb.barplot(ax = ax, data = df, x='questionnaire', y = 'total_score', order = ['Dendrogram', 'Treemap', 'Sunburst', 'Circlepacking'], color = 'royalblue')
    ax.bar_label(ax.containers[0])
    plt.xlabel('HGS visualization type')
    plt.ylabel('Total complexity score')
    plt.title('Total complexity scores of HGS visualization types')
    plt.show()
    #plt.savefig('complexity-rating-scores')
    return fig, ax
    
    

if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    item_path = set_item_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset = item(participant_list, item_path)
    
    #encode likert scales
    condition = complexity(subset)
    score_df = score(condition)
    participant_scores = part_score(condition)
    
    #create csvs and plot
    create_csv(condition)
    create_csv(score_df)
    bar(score_df)


    

  

    
