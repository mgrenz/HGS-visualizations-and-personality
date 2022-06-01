"""
date: 30.05.2022
author: Mae Grenz
"""

import numpy as np
import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from plotnine import *

from main_helpers import *
import main_bigfive 
import main_rating


'''
Implementation of median split: Participants scoring the median value as trait score were allocated randomly to the low or high group such that the group size is balanced. (Printing of plots is currently commented)
'''
    


#split values at median, allocate median values randomly to two groups
def splitr(df, trait):
    l = df[df[trait].sort_values() < df[trait].median()]
    h = df[df[trait].sort_values() > df[trait].median()]
    mid = df[df[trait].sort_values() == df[trait].median()].sample(frac=1)
    group_size = 23 - len(l)
    mid_low = mid[:group_size]
    mid_high = mid[group_size:]
    low = pd.concat([l,mid_low])
    high = pd.concat([h, mid_high])
    return low, high
    
# counts of ratings
def counts(low, high, tree):
    c_low = low[tree].value_counts()
    c_low_df = pd.DataFrame(c_low)
    c_low_df.reset_index(inplace = True)
    c_low_df.columns=[tree, 'amount']
    
    c_high = high[tree].value_counts()
    c_high_df = pd.DataFrame(c_high)
    c_high_df.reset_index(inplace=True)
    c_high_df.columns=[tree, 'amount']
    
    merge_low = pd.merge(low,c_low_df, on = tree)
    merge_high = pd.merge(high, c_high_df, on = tree)
    return merge_low, merge_high
    
    
# plot low and high group 
def plot(dfl, dfh, trait, tree):
    fig, axes = plt.subplots(1,2)
    
    sb.barplot(data = dfl, ax = axes[0], x=tree, y='amount', order = [1,2,3,4], ci = None)
    sb.barplot(data = dfh, ax = axes[1], x=tree, y='amount', order = [1,2,3,4], ci = None)
    
    axes[0].set_xlabel(f'{tree} grading (place)')
    axes[1].set_xlabel(f'{tree} grading (place)')
    axes[0].set_ylabel('Number of ratings (arb. unit)')
    axes[1].set_ylabel('Number of ratings (arb. unit)')
    axes[0].title.set_text(f'Lower {trait} \n trait scores')
    axes[1].title.set_text(f'Higher {trait} \n trait scores')
    axes[0].set_ylim([0,15])
    axes[1].set_ylim([0,15])
    axes[0].bar_label(axes[0].containers[0])
    axes[1].bar_label(axes[1].containers[0])
        
    
    #plt.suptitle(f'Preference ratings of HGS visualization {tree} divided by {trait} median split')
    plt.suptitle(f'{tree} visualization preference ratings divided by median split over {trait} trait')
    plt.tight_layout()
    #PLOT PRINTING COMMENTED
    plt.savefig(f'median-split_{trait}-{tree}_2', bbox_inches='tight')
    #plt.show()
    return fig, axes


#Mann-Whitney-U-test: Significance test of preference rating differences between trait expressions
def mann_whitney(low,high):
    u = stats.mannwhitneyu(low['amount'], high['amount'])
    return u 
    
    
    


if __name__ == "__main__":
    
    # set paths
    participant_path = set_participant_path()
    item_path = set_item_path()
    question_path = set_question_path()   
   
    #use helper functions to get relevant subset
    participant_df = participant(participant_path)    
    participant_list = participant_ids(participant_df)
    subset = item(participant_list, item_path)
    subset_quest = question(participant_list, question_path)    
    
    #functions for big5
    big5_df = main_bigfive.big5_questionnaire(subset)
    all_b5 = main_bigfive.total_scores(big5_df)
    
    #dataframe with all places
    rank_df = main_rating.rating_questionnaire(subset_quest, participant_df) 
    
    #function for merging
    dual = rank_df.merge(all_b5, on = 'participant')
    dual.loc[:,'answer'] = dual['answer'].astype(int)
    dual.name = 'hypo3-df'
    
    #pivot visualization types
    dual_tree = dual[['participant','Vis Type','answer', 'condition', 'big5-open', 'big5-cons', 'big5-extra', 'big5-agree', 'big5-neuro']]
    dual_tree = dual_tree.pivot(index='participant', columns='Vis Type', values='answer')
    dual_tree.rename(columns={1: 'Sunburst', 2:'Treemap', 3:'Dendrogram', 4:'Circlepacking'}, inplace = True) 
    
    #merge
    d2 = dual[['participant', 'condition', 'big5-open', 'big5-cons', 'big5-extra', 'big5-agree', 'big5-neuro']]
    d3 = dual_tree.merge(d2, on = 'participant')
    d3 = d3.drop_duplicates(subset='participant').reset_index()
    #drop irrelevant columns
    d3.drop(labels = 'index', axis = 1, inplace = True)
    d3.drop(labels= 'condition', axis = 1, inplace = True)
    d3.rename(columns={'big5-open':'openness', 'big5-cons':'conscientiousness', 'big5-agree':'agreeableness', 'big5-neuro':'neuroticism', 'big5-extra':'extraversion'}, inplace=True)
    
    #split trait by median 
    so = splitr(d3, 'openness')
    sc = splitr(d3, 'conscientiousness')
    sa = splitr(d3, 'agreeableness')
    sn = splitr(d3, 'neuroticism')
    se = splitr(d3, 'extraversion')



    #count ratings of visualizations seperated by trait 
    cos = counts(so[0], so[1], 'Sunburst')
    cod = counts(so[0], so[1], 'Dendrogram')
    cot = counts(so[0], so[1], 'Treemap')
    coc = counts(so[0], so[1], 'Circlepacking')

    ccs = counts(sc[0], sc[1], 'Sunburst')
    ccd = counts(sc[0], sc[1], 'Dendrogram')
    cct = counts(sc[0], sc[1], 'Treemap')
    ccc = counts(sc[0], sc[1], 'Circlepacking')

    cas = counts(sa[0], sa[1], 'Sunburst')
    cad = counts(sa[0], sa[1], 'Dendrogram')
    cat = counts(sa[0], sa[1], 'Treemap')
    cac = counts(sa[0], sa[1], 'Circlepacking')
    
    cns = counts(sn[0], sn[1], 'Sunburst')
    cnd = counts(sn[0], sn[1], 'Dendrogram')
    cnt = counts(sn[0], sn[1], 'Treemap')
    cnc = counts(sn[0], sn[1], 'Circlepacking')
    
    ces = counts(se[0], se[1], 'Sunburst')
    ced = counts(se[0], se[1], 'Dendrogram')
    cet = counts(se[0], se[1], 'Treemap')
    cec = counts(se[0], se[1], 'Circlepacking')

    
    #plot counts of visualization preferences seperated by trait
    
    plot(cos[0], cos[1],'openness', 'Sunburst')
    plot(coc[0], coc[1], 'openness', 'Circlepacking')
    plot(cot[0], cot[1], 'openness', 'Treemap')
    plot(cod[0], cod[1], 'openness', 'Dendrogram')
    
    plot(ccs[0], ccs[1], 'conscientiousness', 'Sunburst')
    plot(ccc[0], ccc[1], 'conscientiousness', 'Circlepacking')
    plot(cct[0], cct[1], 'conscientiousness', 'Treemap')
    plot(ccd[0], ccd[1], 'conscientiousness', 'Dendrogram')
    
    plot(cas[0], cas[1], 'agreeableness', 'Sunburst')
    plot(cac[0], cac[1], 'agreeableness', 'Circlepacking')
    plot(cat[0], cat[1], 'agreeableness', 'Treemap')
    plot(cad[0], cad[1], 'agreeableness', 'Dendrogram')
    
    plot(cns[0], cns[1], 'neuroticism', 'Sunburst')
    plot(cnc[0], cnc[1], 'neuroticism', 'Circlepacking')
    plot(cnt[0], cnt[1], 'neuroticism', 'Treemap')
    plot(cnd[0], cnd[1], 'neuroticism', 'Dendrogram')
    
    plot(ces[0], ces[1], 'extraversion', 'Sunburst')
    plot(cec[0], cec[1], 'extraversion', 'Circlepacking')
    plot(cet[0], cet[1], 'extraversion', 'Treemap')
    plot(ced[0], ced[1], 'extraversion', 'Dendrogram')
    
    #Mann-Whitney-U-test
    print('Mann-Whitney-U test')
    print('Openness')
    print('Sunburst:', mann_whitney(cos[0], cos[1])) 
    print('Circlepacking:', mann_whitney(coc[0], coc[1])) 
    print('Treemap:', mann_whitney(cot[0], cot[1])) 
    print('Dendrogram:', mann_whitney(cod[0], cod[1]))

    print('Conscientiousness')
    print('Sunburst:', mann_whitney(ccs[0], ccs[1]))
    print('Circlepacking:', mann_whitney(ccc[0], ccc[1])) 
    print('Treemap:', mann_whitney(cct[0], cct[1]))
    print('Dendrogram:', mann_whitney(ccd[0], ccd[1])) 

    print("Agreeableness")
    print('Sunburst:', mann_whitney(cas[0], cas[1])) 
    print('Circlepacking:', mann_whitney(cac[0], cac[1])) 
    print('Treemap:', mann_whitney(cat[0], cat[1])) 
    print('Dendrogram:', mann_whitney(cad[0], cad[1])) 

    print("Neuroticism")
    print('Sunburst:', mann_whitney(cns[0], cns[1])) 
    print('Circlepacking:', mann_whitney(cnc[0], cnc[1])) 
    print('Treemap:', mann_whitney(cnt[0], cnt[1])) 
    print('Dendrogram:', mann_whitney(cnd[0], cnd[1])) 

    print("Extraversion")
    print('Sunburst:', mann_whitney(ces[0], ces[1])) 
    print('Circlepacking:', mann_whitney(cec[0], cec[1])) 
    print('Treemap:', mann_whitney(cet[0], cet[1]))
    print('Dendrogram:', mann_whitney(ced[0], ced[1]))


    
  
   
    



