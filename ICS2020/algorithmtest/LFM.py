#LFM算法的实现     隐语义模型算法
__explain__='__如下所示__'
'''
    LFM (latent factor model) 核心思想是通过隐含特征（latent factor)联系用户兴趣和物品
    隐含语义分析技术  pLSA、LDA、隐含类别模型 、隐含主题模型 、矩阵分解
    LFM在TopN推荐中的性能。在LFM中，重要的参数有4个：
    隐特征的个数F;学习速率alpha；正则化参数lamb;负样本/正样本比例ratio
    通过实验发现，ratio参数对LFM的性能影响最大。因此推荐固定F=100,alpha=0.02,lamb=0.01然后分析ratio
'''
import pandas as pd
import numpy as np
import math
import operator
import time
import random
from ICS2020.algorithmtest.datatest import Initdata

allItemSet=set()   #定义所有的物品集合
def InitAIIItemSet(item_user):        #初始化物品集合item_user={item,user,rating}
    allItemSet.clear()
    key1=item_user.keys()
    for i in key1:
        allItemSet.add(i)

def InitItems_Pool(user_item):      #初始化各个物品的采样池
    item_pool={}
    key1=user_item.keys()
    for i in key1:
        item_pool.setdefault(i,{})
        interacted_items=set(user_item[i].keys())
        num=0
        temp=list(allItemSet-interacted_items)
        for j in temp:
            item_pool[i][num]=j
            num+=1
    return item_pool

def RandomSelectNegativativeSample1(user_item,item_pool):   #负样本采样过程
    ret=dict()                                              #返回ret，如果正样本，ret[i][j]=1,否则ret[i][j]=0
    key1=user_item.keys()
    for i in key1:
        ret.setdefault(i,{})
        for j in user_item[i].keys():
            ret[i][j]=1
    for i in key1:
        key2=user_item.keys()
        n=0
        for j in range(0,len(key2)*3):
            item=item_pool[i][random.randint(0,len(item_pool[i])-1)]
            if item in ret[i]:
                continue
            ret[i][item]=0
            n+=1
            if n>len(key2):
                break
    return ret            #ret={user,item,Rui=0/1} 0为负样本   1为正样本

#以上函数主要功能为生成样本库，即正、负样本(一般来说，正负样本的个数是一样的)
#构建损失函数，使用随机梯度下降算法来求最合适的参数p和q

def InitModel(user_item,F):
    P=dict()
    Q=dict()
    for user,items in user_item.items():
        P[user]=dict()
        for f in range(0,F):
            P[user][f]=random.random()
        for i,r in items.items():
            if i not in Q:
                Q[i]=dict()
                for f in range(0,F):
                    Q[i][f]=random.random()
    return P,Q             #p={user,F,random()}   q={item,F,random()}

def LatentFactorModel(user_item,F,N,alpha,lamb):
    #F 隐因子个数   alpha学习速率  lmbd正则化  N为随机梯度下降算法的迭代次数
    #首先定义损失函数  在使用随机梯度下降算法求解损失函数最小值的P,Q
    InitAIIItemSet(user_item)
    item_pool=InitItems_Pool(user_item)
    P,Q=InitModel(user_item,F)
    ret=RandomSelectNegativativeSample1(user_item,item_pool)
    for step in range(0,N):
        for user,items in user_item.items():
            samples=ret[user]
            for item,rui in samples.items():
                eui=rui-Predict(user,item,P,Q)    #求解
                for f in range(0,F):
                    try:
                        P[user][f]+=alpha*(eui*Q[item][f]-lamb*P[user][f])   #Puk=Puk+alpha*(Qik-lamb*Puk)
                        Q[item][f]+=alpha*(eui*P[user][f]-lamb*Q[item][f])   #Qik=Qik+alpha*(Puk-lamb*Qik)
                    except Exception as e:
                        continue
        alpha*=0.9
    return P,Q        #P,Q即为随机梯度下降算法

def Predict(user,item,P,Q):
    rate=0
    for f,puf in P[user].items():
        try:
            qif=Q[item][f]
            rate+=puf*qif
        except Exception as e:
            continue
    return rate         #求解下降速率，也就是求偏导

def Recommend2(user_item,user,P,Q):   #求解user的推荐物品
    rank=dict()
    inertact_items=user_item[user]
    for i in Q:
        if i in inertact_items.keys():
            continue
        rank.setdefault(i,0)
        for f,qif in Q[i].items():
            puf=P[user][f]
            rank[i]+=puf*qif
    return rank        #rank={item,评分}

def RecommendLFM(user_item,F,T,alpha,lamb,N):  #user_item={user,item,rating} F为选取的隐子个数 T为迭代次数 alpha为学习速率,lamb为正则化因子
    users=user_item.keys()                     #N为返回的推荐物品的个数
    P,Q=LatentFactorModel(user_item,F,T,alpha,lamb)
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=Recommend2(user_item,i,P,Q)
        R=sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:N]
        #Recomendation[i]=R
        for j,item in R:
            Recomendation[i].add(j)
    return Recomendation          #返回属性{user,set()}   set()为推荐物品的值