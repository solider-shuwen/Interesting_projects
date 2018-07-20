# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 20:06:54 2018

@author: Administrator
"""
import var1
import var2
import pandas as pd
import re
import datetime
import parse_team

newmatch = parse_team.parse().loc[:,['主队', '客队', '比赛时间', '比分']]

table = pd.read_csv("parse\match_team.csv", encoding='gbk').loc[:,['主队', '客队', '比赛时间', '比分']]
table = pd.concat([table, newmatch])

historical = table.rename(columns={'主队':'home_team', '客队':'visiting_team', '比赛时间':'time', '比分':'result'}).loc[:, ['home_team', 'visiting_team', 'time', 'result']]
historical['home_team'] = historical['home_team'].str.replace('\s', '')
historical['visiting_team'] = historical['visiting_team'].str.replace('\s', '')
pattern = re.compile(r'[0-9]*:[0-9]*')
historical['result'] = [pattern.findall(x)[0] for x in historical['result']]
historical['result'] = historical['result'].str.replace('\s', '')
historical['result'] = historical['result'].str.replace(':', '-')
historical = historical.drop_duplicates() 
historical['team_name'] = historical['home_team']
historical_group1 = pd.DataFrame(historical.values, columns=['home_team', 'visiting_team', 'time', 'result', 'team_name'])
historical['team_name'] = historical['visiting_team']
historical_group2 = pd.DataFrame(historical.values, columns=['home_team', 'visiting_team', 'time', 'result', 'team_name'])

historical_record_group = pd.concat([historical_group1, historical_group2])

competition_process = pd.read_csv("parse\competition_process_1.csv", encoding='gbk').loc[:,['主队', '客队', '比赛时间']]
competition_process = competition_process.rename(columns={'主队':'team1', '客队':'team2', '比赛时间':'competition_time'}).loc[:, ['team1', 'team2', 'competition_time']]
competition_process['team1'] = [re.sub(r'\s', "", x) for x in competition_process['team1']]
competition_process['team2'] = [re.sub(r'\s', "", x) for x in competition_process['team2']]

"""var1"""
var1_ = pd.DataFrame({'team1':[] , 'team2':[], 'competition_time':[], 'var1':[]})
for i in range(len(competition_process)):
    var1_ = pd.concat([var1_, var1.goal_fiff(competition_process.loc[i, 'team1'], competition_process.loc[i, 'team2'], competition_process.loc[i, 'competition_time'], historical_record_group)]).reset_index(drop = True)
    #print(i)

"""var2"""
nowTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
var2_ = var2.goal_graph(competition_process, nowTime, historical_record_group)

var = var1_.merge(var2_, on = ['competition_time','team1','team2'])
print('\n',var)