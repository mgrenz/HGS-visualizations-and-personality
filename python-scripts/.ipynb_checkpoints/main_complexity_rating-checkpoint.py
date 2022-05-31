"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
from scipy import stats
from main_helpers import *
import main_rating
import main_complexity

'''
Plot Complexity and Preference Correlation
'''

#calculation of Spearman's correlation coeffcient
def spearman(df1, df2):
    spear = stats.spearmanr(df1, df2)
    return spear


#plot complexity scores and preference ratings 
def corr_plot(df):
    fig, ax = plt.subplots()
    sb.boxplot(data=df, ax = ax, x= 'Preference-Rating', y='Complexity-Score', order = [1,2,3,4], color = 'royalblue')
    sb.stripplot(data=df, ax = ax, x= 'Preference-Rating', y='Complexity-Score', order = [1,2,3,4], color = 'black')
    plt.title('Preference Ratings and Complexity Scores across all Visualizations')
    plt.xlabel('Preference Rating Place')
    plt.show()
    #plt.savefig('eda-pref-compl')
    return fig, ax
    
    



if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    question_path = set_question_path()
    item_path = set_item_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset_quest = question(participant_list, question_path)
    subset_item = item(participant_list, item_path)
    
    #functions for ranking
    ranking_df = main_rating.rating_questionnaire(subset_quest, participant_df) #all places per part
    ranking_df['Vis Type'].replace([1,2,3,4], ['Sunburst', 'Treemap', 'Dendrogram', 'Circlepacking'], inplace =True)
    ranking_df.loc[:,'answer'] = ranking_df['answer'].astype(int)

    #functions for complexity
    condition = main_complexity.complexity(subset_item)
    score_df = main_complexity.score(condition)
    participant_scores = main_complexity.part_score(condition) 
    participant_scores.rename(columns={'questionnaire':'Vis Type'}, inplace = True)
    
    #merge rating and complexity scores per participant
    part_compl_rating_df = pd.merge(participant_scores, ranking_df, on = ['participant', 'Vis Type'])
    part_compl_rating_df.rename(columns={'total_score':'Complexity-Score', 'answer':'Preference-Rating'}, inplace = True)
    
    #plot correlation
    corr_plot(part_compl_rating_df)
      
    #calculate Spearman's rank correaltion coefficient
    s = spearman(part_compl_rating_df['Complexity-Score'], part_compl_rating_df['Preference-Rating'])
    print("Spearman's rank correlation coefficient investigating a correlation between complexity scores and preference ratings:")
    print(s)
    
   
   
   
    