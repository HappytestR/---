#基于SVG的推荐评分系统
__explain__='__解释如下__'
'''
    主要的算法是实现在于如何对SVG矩阵中P,Q的生成
    生成的数据集是物品的评分矩阵'
    评分预测问题
    需要的数据集就是{user,item,rating}但是是要求对所有的user,item都做评分的化
'''
import math
import operator
import random
from numpy import linalg as la
import numpy as np
from ICS2020.algorithmtest.datatest import Initdata
def ecludSim(inA,inB):      #计算余弦距离
    return 1.0/(1.0+la.norm(inA,inB))
def pearsSim(inA,inB):   #计算皮尔逊相关系数矩阵
    if len(inA)<3:
        return 1.0
    return 0.5+0.5*np.corrcoef(inA,inB,rowvar=0)[0][1]
def cosSim(inA, inB):   #计算余弦相似度
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    if denom != 0:
        return 0.5 + 0.5 * (num / denom)  # 将相似度归一到0与1之间
    else:
        return 0.5

def Initdata1(user_item,item_user):
    users_items={}
    key1=user_item.keys()
    key2=item_user.keys()
    for i in key1:               #初始化全部的user_item矩阵
        users_items.setdefault(i,{})
        for j in key2:
            users_items[i][j]=0
    for i in key1:
        key=user_item[i].keys()
        for j in key:
            users_items[i][j]=user_item[i][j]
    return users_items

def Pridect(user,item,p,q):        #预测user对item的评分
    return sum(p[user][f]*q[item][f] for f in range(0,len(p[user])))

def InitModel(users_items,F):
    P=dict()
    Q=dict()
    for user,items in users_items.items():
        P[user]=dict()
        for f in range(0,F):
            P[user][f]=random.random()
        for i,r in items.items():
            if i not in Q:
                Q[i]=dict()
                for f in range(0,F):
                    Q[i][f]=random.random()
    return P,Q             #p={user,F,random()}   q={item,F,random()}

def Learning(users_items,F,N,alpha,lamb):
    #F 隐因子个数   alpha学习速率  lmbd正则化  N为随机梯度下降算法的迭代次数
    #首先定义损失函数  在使用随机梯度下降算法求解损失函数最小值的P,Q
    P,Q=InitModel(users_items,F)
    for step in range(0,N):
        for user,items in users_items.items():
            samples=users_items[user]
            for item,rui in samples.items():
                eui=float(rui)-float(Pridect(user,item,P,Q))  #求解
                for f in range(0,F):
                    P[user][f]+=alpha*(eui*Q[item][f]-lamb*P[user][f])   #Puk=Puk+alpha*(Qik-lamb*Puk)
                    Q[item][f]+=alpha*(eui*P[user][f]-lamb*Q[item][f])   #Qik=Qik+alpha*(Puk-lamb*Qik)
        alpha*=0.9
    return P,Q        #P,Q即为随机梯度下降算法

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

def RecommendSVD(user_item,item_user,F,T,alpha,lamb,N):  #user_item={user,item,rating} F为选取的隐子个数 T为迭代次数 alpha为学习速率,lamb为正则化因子
    users=user_item.keys()   #N为返回的推荐物品的个数
    users_items=Initdata1(user_item,item_user)
    P,Q=Learning(users_items,F,T,alpha,lamb)
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=Recommend2(user_item,i,P,Q)
        R=sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:N]
        #Recomendation[i]=R
        for j,item in R:
            Recomendation[i].add(j)
    return Recomendation          #返回属性{user,set()}   set()为推荐物品的值
