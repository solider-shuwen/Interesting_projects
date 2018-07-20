# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 09:12:54 2018

@author: Administrator
"""

import networkx as nx
import re

import pandas as pd
import datetime
import numpy as np

def sigmoid(inX):  
    return 1.0/(1+np.exp(-inX))  
'''
table中每条记录要2个
table格式
team_name | time           | home_team | visiting_team | result
str       | %Y/%m/%d       | str       | str           | str（homescore-visitscore）
'''
def goal_graph(competition_process, competition_time, table):
    '''
    competition_time:为预测时间
    competition_process:为pandas表，必须包含字段‘team1’，‘team2’，‘competition_time’
    '''
    #historical_record = pd.read_csv(r"D:\worldcup\historical_record.csv")
    historical_record = table
    #去重
    historical_record = historical_record.drop_duplicates().reset_index(drop = True)
    #处理result为净胜球    
    for i in range(len(historical_record)):
        num1 = historical_record.loc[i, 'result'].split('-')[0]
        num2 = historical_record.loc[i, 'result'].split('-')[1]
        historical_record.loc[i, 'result'] = int(num1) - int(num2)
            
    #设置比赛开始时间
    historical_record = historical_record.loc[: , ['home_team', 'visiting_team', 'result', 'time']]
    historical_record['time'] = pd.to_datetime(historical_record['time'])
    start_date_str = competition_time
    start_date = datetime.datetime.strptime(start_date_str, '%Y/%m/%d %H:%M')
    #sigmode处理时间，得出权重
    historical_record['sec_from_start_to_data'] = (historical_record.loc[:, 'time']-start_date).dt.total_seconds()  
    historical_record['sfstd_non'] = historical_record.loc[:, ['sec_from_start_to_data']].apply(lambda x: (x - np.mean(x)) / (np.std(x)))

    historical_record['wight'] = sigmoid(historical_record['sfstd_non'])
    #净胜球与权重结合
    historical_record['result_wight'] = historical_record['result'] * historical_record['wight']
    historical_record['result_wight'] = historical_record['result_wight'].astype('float64')
    
    gy = historical_record.groupby(['home_team', 'visiting_team'])
    con = gy.mean()
    res_weight = con.reset_index().loc[:, ['home_team', 'visiting_team', 'result_wight']]
    
    def conv(home, visit, res):
        if res < 0:
            return (home, visit, -res)
        else:
            return (visit, home, res)
    
    weighted_edges = [conv(res_weight.loc[i, 'home_team'], res_weight.loc[i, 'visiting_team'], res_weight.loc[i, 'result_wight']) for i in range(len(res_weight))]
    '''构造图'''
    G=nx.DiGraph()
    G.add_weighted_edges_from(weighted_edges)
    '''pagerank排序'''
    pr=nx.pagerank(G,alpha=0.85)
    
    
    pre_tb = competition_process.loc[:, ['team1', 'team2', 'competition_time']]
    pre_tb['var2'] = None
    for i in range(len(pre_tb)):
        pre_tb['var2'][i] = pr[pre_tb['team1'][i]] - pr[pre_tb['team2'][i]]
        
    return pre_tb



# =============================================================================
# table = pd.read_csv("match_team.csv", encoding='gbk').loc[:,['主队', '客队', '比赛时间', '比分']]
# historical = table.rename(columns={'主队':'home_team', '客队':'visiting_team', '比赛时间':'time', '比分':'result'}).loc[:, ['home_team', 'visiting_team', 'time', 'result']]
# historical['home_team'] = historical['home_team'].str.replace('\s', '')
# historical['visiting_team'] = historical['visiting_team'].str.replace('\s', '')
# pattern = re.compile(r'[0-9]*:[0-9]*')
# historical['result'] = [pattern.findall(x)[0] for x in historical['result']]
# historical['result'] = historical['result'].str.replace('\s', '')
# historical['result'] = historical['result'].str.replace(':', '-')
# historical = historical.drop_duplicates() 
# historical['team_name'] = historical['home_team']
# historical_group1 = pd.DataFrame(historical.values, columns=['home_team', 'visiting_team', 'time', 'result', 'team_name'])
# historical['team_name'] = historical['visiting_team']
# historical_group2 = pd.DataFrame(historical.values, columns=['home_team', 'visiting_team', 'time', 'result', 'team_name'])
# 
# historical_record_group = pd.concat([historical_group1, historical_group2])
# 
# competition_process = pd.read_csv(r"competition_process_1.csv", encoding='gbk').loc[:,['主队', '客队', '比赛时间']]
# competition_process = competition_process.rename(columns={'主队':'team1', '客队':'team2', '比赛时间':'competition_time'}).loc[:, ['team1', 'team2', 'competition_time']]
# competition_process['team1'] = [re.sub(r'\s', "", x) for x in competition_process['team1']]
# competition_process['team2'] = [re.sub(r'\s', "", x) for x in competition_process['team2']]
# 
# 
# x = goal_graph(competition_process, '2018/7/20 3:0', historical_record_group)
# =============================================================================
