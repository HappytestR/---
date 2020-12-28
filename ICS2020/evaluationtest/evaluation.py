#评估方法，评估模型
__explain__='__如下所示__'
'''
    本模块负责对算法进行评估
'''
from ICS2020.algorithmtest.ItemCF import ItemCFRecommend
from ICS2020.algorithmtest.datatest import Initdata
#class evaluation:
    #def __init__(self):
'''
datalist=Initdata()
user_item = datalist.getUser_item()
item_user = datalist.getItem_user()
'''


import operator
import math

def Recall(Recommend,test): #召回率
    hit = 0
    all = 0
    key=test.keys()
    for user in key:
        item_test=test[user].keys()
        all += len(item_test)
        try:
            rank=Recommend[user]
            for item in rank:
                if item in item_test:
                    hit += 1
        except Exception as e:
            continue
    return [hit/ (1.0 * all)]


def Precision(Recommed,test):     #精准率
    hit = 0
    all = 0
    key = test.keys()
    for user in key:
        item_test=test[user].keys()
        try:
            rank=Recommed[user]
            all += len(rank)
            for item in rank:
                if item in item_test:
                    hit +=1
        except Exception as e:
            continue
    if all==0:
        return 0.0
    else:
        return [hit / (1.0 * all)]

def Coverage(records):  #覆盖率
    total = []
    for user, items in records.items():
        total += items
    return len(total) / len(records)

def RMSE(records):  #均方根误差
    n = 0
    m = 0
    for u, i, rui, pui in records:
        m = sum((rui - pui) * (rui - pui))
    n = math.sqrt(m / len (records))
    return n


def MAE(records):   #平均绝对误差
    n = 0
    m = 0
    for u, i, rui, pui in records:
        m = sum(abs(rui - pui))
    n = sum(m / len (records))
    return n

def GiniIndex(p):   #基尼系数
    j = 1
    n = len(p)
    G = 0
    for item, weight in sorted (p.items(),key = operator.itemgetter(1)):
        G += (2*j-n-1)*weight
    return G/float(n - 1)


