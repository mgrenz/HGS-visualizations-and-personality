"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from main_helpers import *
import seaborn as sb


'''
Visualization preference ratings analysis script
'''

#Creation of dataframe with participant, condition, visualization type and preference rating
def rating_questionnaire(subset, participant_df):
     #get ranking subset
    rank_df = subset[subset['type'].str.contains('ranking')]
    rank_df.name = 'ranking-questionnaire'
    #create cleaner version of rank_df
    rank_df = rank_df.loc[:, ['participant', 'question', 'answer']]
    text_dict = {'Bitte betrachte nun dein persönliches Zielsystem in verschiedenen Visualisierungen. Anschließend kannst Du die verschiedenen Visualisierungen gemäß deiner Präferenz, diese zu nutzen, anordnen. (1 – am stärksten präferiert bis 4 – am wenigsten präferiert), condition: 1' : 1,'Bitte betrachte nun dein persönliches Zielsystem in verschiedenen Visualisierungen. Anschließend kannst Du die verschiedenen Visualisierungen gemäß deiner Präferenz, diese zu nutzen, anordnen. (1 – am stärksten präferiert bis 4 – am wenigsten präferiert), condition: 2' : 2, 'Bitte betrachte nun dein persönliches Zielsystem in verschiedenen Visualisierungen. Anschließend kannst Du die verschiedenen Visualisierungen gemäß deiner Präferenz, diese zu nutzen, anordnen. (1 – am stärksten präferiert bis 4 – am wenigsten präferiert), condition: 3' : 3, 'Bitte betrachte nun dein persönliches Zielsystem in verschiedenen Visualisierungen. Anschließend kannst Du die verschiedenen Visualisierungen gemäß deiner Präferenz, diese zu nutzen, anordnen. (1 – am stärksten präferiert bis 4 – am wenigsten präferiert), condition: 4' : 4}
    rank_df['question'].replace(text_dict, inplace = True)
    rank_df.rename(columns={'question' : 'Vis Type'}, inplace = True)    
    #get conditions for participants
    condition_df = participant_df.loc[:, ['id','condition']].copy()
    condition_df.rename(columns={'id' : 'participant'}, inplace = True)
    condition_df['condition'] = condition_df['condition'].astype(int)
    #add conditions to rank dataframe
    rank_cond_df = rank_df.merge(condition_df, how='inner', on = 'participant')
    rank_cond_df.name = 'ranking-condition-df'
    return rank_cond_df

#Dataframe of first place ranked visaulizations with participant and condition. If the condition is the same as the preferred visualizaiton, bias is set to true.
def ranked_1(rank_cond_df):
    first_df = rank_cond_df.loc[rank_cond_df['answer'] == '1'].reset_index()
    first_df.loc[:,'bias'] = False
    first_df.loc[:,'bias'] = np.where(first_df['Vis Type'] == first_df['condition'], True, first_df['bias'])
    first_df.name = 'first-place'
    return first_df


#count preference ratings per visualization
def counter(position_df):
    counter_series = position_df['Vis Type'].value_counts()
    counter_df1 = pd.DataFrame(counter_series)
    counter_df = counter_df1.reset_index()
    counter_df.columns = ['Vis Type', 'counts']
    counter_df.name = f'{position_df.name}-counts'
    return counter_df


#plot visualization and first place ratings
def chart(counter_df):
    fig,ax = plt.subplots()
    sb.barplot(ax = ax, data = counter_df, x='Vis Type',y = 'counts', color = 'royalblue')
    ax.bar_label(ax.containers[0])
    plt.xlabel('Visualization type')
    plt.ylabel('Number of 1st place ratings')
    plt.title('Overall visualization preferences')
    #plt.show()
    plt.savefig('preference-visualization')
    return fig,ax


    

if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    question_path = set_question_path()

    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset = question(participant_list, question_path)
    
    #functions for ranking
    ranking_df = rating_questionnaire(subset, participant_df)
    ranking_df['Vis Type'].replace([1,2,3,4], ['Sunburst', 'Treemap', 'Dendrogram', 'Circlepacking'], inplace =True)
    first = ranked_1(ranking_df)
    count_first = counter(first)
    
    #csv creation and plotting
    create_csv(count_first)
    create_csv(first)
    chart(count_first)
    

    
    
