-------------------
### 2018.8.24第二轮结果分析
<br/>
正确率： 0.6
<br/>
单场平均（欧赔平均）： 1.075
<br/>
2串1平均（欧赔平均）： 0.6969199999999999
<br/>
第三轮后可能会对算法有一个大的调整

-------------------
### 2018.8.13首轮结果分析
<br/>
正确率： 0.7
<br/>
单场平均（欧赔平均）： 1.379
<br/>
2串1平均（欧赔平均）： 1.8840799999999998
<br/>
还有很多人问我，结果怎么看，我在这里统一说一下。目前只要看var1就可以了小于-0.1是负，-0.1到0.1是平。
对于首轮结果，跟世界杯差不多。
<br/>
要强调的一点是，这里预测的是多场平均准确率，要看单场绝对胜负的请右上角。
<br/>
还有29轮，如果不出意外，var1的准确率也就这样了。

-------------------
### 2018.8.10最新结果
<br/>

| competition_time | team1 | team2    |  var1    |    var2
| ------ | ------ | ------ | ------ | ------ |
|   2018/8/11 3:00 |   曼联 |  莱切城 | 0.470644  | 0.0108421
|  2018/8/11 19:30  | 纽卡斯 |   热刺 | -0.806352 | -0.0335752
| 2018/8/11 22:00  | 哈德斯  | 切尔西 | -0.783772 | -0.0122059
|  2018/8/11 22:00  | 伯恩茅 |  加的夫| -0.575607 | -0.00195972
| 2018/8/11 22:00  | 富勒姆  | 水晶宫 | -0.096452 | -0.00097609
|  2018/8/11 22:00 |  沃特福 |  布赖顿 | 0.155721 | -0.00779891
|  2018/8/12 0:30  |  狼队  | 埃弗顿  | 0.173849  | 0.00372399
|  2018/8/12 20:30 |  利物浦 |  西汉姆 | 0.609328 |  0.0383682
|  2018/8/12 20:30 |  南安普  | 伯恩利 | -0.069946 | 0.00295299
| 2018/8/12 23:00  | 阿森纳   | 曼城 | -0.988217  | -0.019511

-------------------
### 2018.7.18更新算法

var1.py是2.2中假设2的算法，也就是之前世界杯的算法
<br/>
var2.py是2.2中假设1的算法，具体参考了谷歌的pagerank算法，当然是改进了的，就叫它footballrank吧
<br/>
parse_team.py是自动爬虫的，用来更新数据的，采取的策略是按照队伍爬取最近的30场比赛
<br/>
然后，现在可以一键运行 只需要
``` python
python creat_var_run.py
```
结果：
<br/>

| competition_time | team1 | team2 | var1    |    var2 |
| ------ | ------ | ------ | ------ | ------ |
| 2018/8/11 3:00  |  曼联  | 莱切城 | 0.479978 |  0.0185568 |
| 2018/8/11 19:30 |  纽卡斯 |   热刺 |-0.836736|  -0.0193392|
| 2018/8/11 22:00  | 哈德斯 |  切尔西| -0.808886|  -0.0225223|
|  2018/8/11 22:00  | 伯恩茅 |  加的夫| -0.461924| -0.00171044|
|  2018/8/11 22:00   |富勒姆  | 水晶宫 | 0.219648 | 0.00401372|
|  2018/8/11 22:00  | 沃特福  | 布赖顿 | 0.084769 |-0.00979654|
|   2018/8/12 0:30  |  狼队  | 埃弗顿 | 0.002764  |0.00435598|
|  2018/8/12 20:30  | 利物浦 |  西汉姆 | 0.584520  |  0.054268|
|  2018/8/12 20:30  | 南安普  | 伯恩利| -0.071907  |0.00430562|
|  2018/8/12 23:00  | 阿森纳  |  曼城 |-0.968656  |-0.0321206|


-------------------
-------------------
### 2018.7.18更新源数据， 在目录parse下
-------------------
# 关于英超预测任务的一些想法



**英超预测**是之前世界杯预测，感觉效果还不错，才开的新坑，由于这种数据挖掘任务，不仅费脑子还费精力，所以把代码开源，如果有人有兴趣或有新的想法，欢迎留言一起探讨。

-------------------

[TOC]

## 任务简介以及自己对任务的理解



正如任务题目所示，简单来说是预测**英超未来比赛的**胜平负，如果后期进展的好，不排除直接预测进球数或净胜球（个人感觉没可能的说）

### 1.任务理解

此次任务有以下几个特点：
<br/>
**1.**这个任务总的来说属于分类；
<br/>
**2.**对于某一队的一系列比赛来说，是属于时间序列任务的，因此需要考虑的是前面的比赛对后面比赛的影响；<br/>
**3.**从任务整体上来看，其比赛质量是受球员个人能力、主帅个人能力影响的，但是这些是无法被量化的；<br/>
**4.**一些其他的因素，比如团结问题、工资能否按时发放、俱乐部团队的能力；<br/>
下面是对以上4点具体分析

## 2.具体分析

### 2.1分类任务
对与分类任务，常用的算法LR、SVM、K近邻等，有时会用神经网络，不过速度慢，效果可能也不是那么理想。<br/>
**LR：**最常用，也是目前来说最好用也最成熟的方法，几乎对任何任务都合适；<br/>
**SVM：**效果很棒，主要优点在于其优秀的泛化能力，但是由于其实际上是把低维的数据放在高纬的上计算，时间代价比LR高的多，但是如果数据量很小，则不必在意；<br/>
**K近邻：**优点就是理解简单，缺点是算的慢；<br/>

### 2.2时间序列
时间序列分析，由于工作原因经常接到时间序列的任务，对与时间序列算是比较了解，但是，这个跟普通的时间序列不一样，原因是就某一段时间而言，可能球队状态好，就牛的一b，影响这个状态的因素有很多，可能上一场逆转、主帅做了思想工作、出去打了一炮等等。<br/>
为了表现这个状态的变化，我想到的一个方法就是**去时间化**，假设如下：
<br/>
**1.假设球队 ~~在最近2场比赛的状态是一样的~~ 现在的状态与前面的比赛相关的，越接近现在相关性越高** <br/>
**2.假设球队在遇到不同的队伍所表现出的状态是不一样的** <br/>
**3.第一假设和第二假设会相互影响**<br/>
在经过去时间化的操作后，这样一个时间序列就可以变成一个常量，作为一个特征来使用。这个也就是世界杯预测上的那个特征（但是，世界杯预测上的那个特征只是使用了第二个假设），核心代码如下：
##### 代码块
``` python
def goal_fiff(team1, team2, competition_time):
    #historical_record = pd.read_csv(r"D:\worldcup\historical_record.csv")
    historical_record = pd.read_csv(r"D:\worldcup\historical_record.csv")
    del historical_record['id']
    del historical_record['create_time']
    del historical_record['update_time']
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
    res = alg.predict(np.array(res).reshape(-1, 1))[0,0]
    res_e_s = pd.DataFrame({'team1':[team1], 'team2':[team2], 'competition_time':[competition_time], '净胜球':[res]})
    return res_e_s
```
这样计算处理的特征，通过世界杯的检验，是可行的，但是这只是经过了第二假设，没有经过第一假设，因此，在最后的结果中，我们可以看到，一些队伍的预测大部分是错的，比如德国队的预测，没有考虑到队伍最近状态问题。

### 无法被量化的因素
上面时间序列的具体分析，属于单纯从结果预测结果，如果从过程来预测结果看，就需要的是球员个人能力、主帅个人能力等等，这个就我个人理解，感觉有影响，但是影响不大，所以荣后再议。

### 其他的因素
这个感觉影响还是比较大的，比如阿根廷= =。但是数据不好获取，还需要一些NLP的处理，荣后再议。

## 结尾

对于后面的程序，会按目录步骤一步步验证，慢慢来吧
