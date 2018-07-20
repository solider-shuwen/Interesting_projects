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
        print(url)
        return ""
 
def getListId(lst, stockURL):
    list_team = ['西汉姆联', '沃特福德', '托特纳姆热刺', '切尔西', '纽卡斯尔联',
                 '南安普敦', '曼彻斯特联', '曼彻斯特城', '利物浦', '狼队','莱切斯特城',
                 '加的夫城', '哈德斯菲尔德', '富勒姆', '布赖顿', '伯恩利', '伯恩茅斯',
                 '埃弗顿', '阿森纳', '水晶宫']
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser') 
    a = soup.find_all('a')
    for i in a:
        if i.string in list_team:
            try:
                href = i.attrs['href']
                lst.append(re.findall(r"/[0-9]+/", href)[0][1:-1])
            except:
                continue
    
def getListUrl(lstid, lst, stockURL):
    for id_ in lstid:
        temp = stockURL +'&tid=' + str(id_) + '&hoa=0'
        lst.append(temp)

def getInfo(lst):
    match = []
    a = len(lst)
    b = 0
    for l in lst:
        b = b +1
        #print(b)
        url = l
        html = getHTMLText(url)
        try:
            if html=="":
                print('url错误：', url)
                continue
            infoDict = json.loads(html)
            matchlist = infoDict['list']
            for m in matchlist:
                if m['WIN']==None:
                    pei = None
                else:
                    pei = m['WIN']+m['DRAW']+m['LOST']
                tmp_m = [m['SIMPLEGBNAME'],#'赛事':
                         m['MATCHDATE'],#'比赛时间':
                         m['HOMETEAMSXNAME'],#'主队':
                         str(m['HOMESCORE']) + ':' + str(m['AWAYSCORE']) + '(' + str(m['HOMEHTSCORE']) + ':' + str(m['AWAYHTSCORE']) + ')',#'比分': 
                         m['AWAYTEAMSXNAME'], #'客队':
                         re.findall(r"[\u4e00-\u9fa5]+", m['RESULT'])[0], #'赛果':
                         pei, #'赔率':
                         m['HANDICAPLINENAME'], #'澳门盘口':
                         m['PAN'], #'盘路':
                         m['BS'], #'大小':
                         '析' #'分析':
                         ]
                match.append(tmp_m)
              
            print("\r爬虫当前进度: {0}%".format((b/a)*100),end="")
        except:
            traceback.print_exc()
            break
    match = pd.DataFrame(match, columns = ['赛事','比赛时间','主队','比分','客队','赛果','赔率','澳门盘口','盘路','大小','分析'])
    return match
 
def parse():
    list_url = 'http://liansai.500.com/zuqiu-4826/teams/'
    Info_url = 'http://liansai.500.com/index.php?c=teams&a=ajax_fixture&records=30'#+'&tid=1286&hoa=0'
    slist=[]
    getListId(slist, list_url)
    #print(slist)
    listUrl=[]
    getListUrl(slist, listUrl, Info_url)
    #print(listUrl)
    match = getInfo(listUrl)
    return match
 
#match = parse()