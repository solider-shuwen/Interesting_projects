# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 08:46:29 2018

@author: Administrator
"""
import pandas as pd
import re
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
def goal_fiff(team1, team2, competition_time, table):
    '''
    competition_time:为比赛时间
    '''
    #historical_record = pd.read_csv(r"D:\worldcup\historical_record.csv")
    historical_record = table
    #去重
    historical_record = historical_record.drop_duplicates().reset_index(drop = True)
    #处理result为净胜球    
    for i in range(len(historical_record)):
        num1 = historical_record.loc[i, 'result'].split('-')[0]
        num2 = historical_record.loc[i, 'result'].split('-')[1]
        if historical_record.loc[i, 'home_team'] == historical_record.loc[i, 'team_name']:
            historical_record.loc[i, 'result'] = int(num1) - int(num2)
        else:
            historical_record.loc[i, 'result'] = int(num2) - int(num1)
    #选出team1和team2
    historical_record_1 = historical_record.loc[historical_record["team_name"] == team1]
    historical_record_2 = historical_record.loc[historical_record["team_name"] == team2]
    e_df = set(historical_record_1['home_team'].tolist()).union(set(historical_record_1['visiting_team'].tolist()))
    s_df = set(historical_record_2['home_team'].tolist()).union(set(historical_record_2['visiting_team'].tolist()))
    e_union_s = e_df.intersection(s_df)
    #print(e_union_s)
    #选出即和team1交手又和team2交手的队伍
    int_inf_2 = historical_record_2.loc[historical_record_2["visiting_team"].isin(e_union_s) | historical_record_2["home_team"].isin(e_union_s)]
    int_inf_1 = historical_record_1.loc[historical_record_1["visiting_team"].isin(e_union_s) | historical_record_1["home_team"].isin(e_union_s)]
    concat_e_s = pd.concat([int_inf_1, int_inf_2]).reset_index(drop=True)  
    
    #print(e_df)
    #设置比赛开始时间
    concat_e_s_sle = concat_e_s.loc[: , ['team_name', 'home_team', 'visiting_team', 'time', 'result', 'score']]
    concat_e_s_sle['time'] = pd.to_datetime(concat_e_s_sle['time'])
    start_date_str = competition_time
    start_date = datetime.datetime.strptime(start_date_str, '%Y/%m/%d %H:%M')
    #sigmode处理时间，得出权重
    concat_e_s_sle['sec_from_start_to_data'] = (concat_e_s_sle.loc[:, 'time']-start_date).dt.total_seconds()  
    concat_e_s_sle['sfstd_non'] = concat_e_s_sle.loc[:, ['sec_from_start_to_data']].apply(lambda x: (x - np.mean(x)) / (np.std(x)))

    concat_e_s_sle['wight'] = sigmoid(concat_e_s_sle['sfstd_non'])
    #净胜球与权重结合
    concat_e_s_sle['result_wight'] = concat_e_s_sle['result'] * concat_e_s_sle['wight']
    #计算结合平均值
    union_1 = pd.DataFrame({'team_name':[],'oppose_team':[],'mean_result_1':[]})
    union_2 = pd.DataFrame({'team_name':[],'oppose_team':[],'mean_result_2':[]})
    for i in e_union_s:
        if i != team1:
            mean_1 = concat_e_s_sle.loc[(concat_e_s_sle['team_name'] == team1)&((concat_e_s_sle['home_team'] == i) | (concat_e_s_sle['visiting_team'] == i))].loc[:, 'result_wight'].mean()
            union_1 = pd.concat([union_1, pd.DataFrame({'team_name':[team1],'oppose_team':[i],'mean_result_1':[mean_1]})])
        if i != team2:
            mean_2 = concat_e_s_sle.loc[(concat_e_s_sle['team_name'] == team2)&((concat_e_s_sle['home_team'] == i) | (concat_e_s_sle['visiting_team'] == i))].loc[:, 'result_wight'].mean()
            union_2 = pd.concat([union_2, pd.DataFrame({'team_name':[team2],'oppose_team':[i],'mean_result_2':[mean_2]})])
        
        
    union = union_1.merge(union_2, on = 'oppose_team')
    #print(union)
    
    #team1与team2直接对抗结果
    mean_1_2 = concat_e_s_sle.loc[(concat_e_s_sle['team_name'] == team1)&((concat_e_s_sle['home_team'] == team2) | (concat_e_s_sle['visiting_team'] == team2))].loc[:, 'result_wight'].mean()
    op_1_2 = pd.DataFrame({'team_name':[team1],'oppose_team':[team2],'mean_result_1':[mean_1_2]})
    mean_2_1 = concat_e_s_sle.loc[(concat_e_s_sle['team_name'] == team2)&((concat_e_s_sle['home_team'] == team1) | (concat_e_s_sle['visiting_team'] == team1))].loc[:, 'result_wight'].mean()
    op_2_1 = pd.DataFrame({'team_name':[team2],'oppose_team':[team1],'mean_result_2':[mean_2_1]})
    #合并所有
    union_all = pd.concat([union, op_2_1, op_1_2]).fillna(0)
    #print(pd.concat([union, op_2_1, op_1_2]).fillna(0))
    
    res = (union_all['mean_result_1'] - union_all['mean_result_2']).mean()
    #修改
    #res = alg.predict(np.array(res).reshape(-1, 1))[0,0]
    res_e_s = pd.DataFrame({'team1':[team1], 'team2':[team2], 'competition_time':[competition_time], 'var1':[res]})
    return res_e_s

