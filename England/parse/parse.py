# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:40:10 2018

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import traceback
import re
import json
import pandas as pd

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
 
def getList(lst, stockURL):
    len_ = 2018 - 2003
    for i in range(len_):
        start = 2003 + i
        end = start + 1
        for j in range(38):
            round_ = j + 1
            temp = stockURL + 'season=' + str(start) + '-' + str(end) + '&round=' + str(round_) + '&matchType=0'
            lst.append(temp)

def getInfo(lst):
    match = []
    for l in lst:
        url = l
        html = getHTMLText(url)
        try:
            if html=="":
                print('url错误：', url)
                continue
            infoDict = json.loads(html)
            matchlist = infoDict['result']['matchList']
            for m in matchlist:
                
                tmp_m = [m['matchTimeStr'],#'比赛日期':
                         m['hostTeamName'],#'主队':
                         str(m['hostScore']) + '-' + str(m['awayScore']),#'比分': 
                         m['awayTeamName'] #'客队':
                         ]
                match.append(tmp_m)
 
            round_ = m['round']
            time_ = m['matchTime']['year']
             
            print("\r当前进度: {0}, 当前轮速: {1}".format(time_, round_),end="")
        except:
            traceback.print_exc()
            break
    match = pd.DataFrame(match, columns = ['比赛日期', '主队', '比分', '客队'])
    return match
 
def main():
    list_url = 'http://league.aicai.com/league/scoreresult!ajaxscoreResult.htm?leagueId=43&'
    slist=[]
    getList(slist, list_url)
    match = getInfo(slist)
    match.to_csv('match.csv')
 
main()