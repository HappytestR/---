#ItemCF(基于物品的协同过滤）
import math
import operator
from ICS2020.Optimization.optimizationtest import ItemSimilarity1,ItemSimilaritytime,Recommedationtime
__explaintion__='__如下所示__'
'''
    ItemCFRecommend()函数为最简单的UserCF推荐算法
    ItemCFRecommendationIUF()函数为更改相似度计算公式之后的推荐算法
    ItemCFRecommendationtime()函数为基于时间的UserCF推荐算法，推荐alpha参数选取0.0000000001
    算法的返回均为字典格式{userId,set()}set()为推荐列表
'''

def ItemSimilarity(user_item):
    users_item=dict()             #余弦相似度
    keys=user_item.keys()
    for i in keys:
        users_item[i]=set()
        keys1=user_item[i].keys()
        for j in keys1:
            users_item[i].add(j)
    C=dict()             #记录物品对物品的评分矩阵
    N=dict()            #记录物品的个数
    keys=users_item.keys()
    for i in keys:     #初始化C
        items=users_item[i]
        for u in items:
            N[u]=0
            C.setdefault(u,{})
            for v in items:
                C[u][v]=0
    for i in keys:     #初始化C
        items=users_item[i]
        for u in items:
            N[u]+=1
            for v in items:
                C[u][v]+=1
    W=dict()
    for i,related_items in C.items():
        W.setdefault(i,{})
        for j,cij in related_items.items():
            W[i][j]=cij/math.sqrt(N[i]*N[j])
    return W                                    #返回W的矩阵中是物品对物品的评分W[item][item]

def Recommendation1(user_item,user_id,W,K):        #给与用户个人推荐，输入为[user_item字典,user_id,W为物品评分矩阵，K为选取前多少个物品
    rank=dict()
    ru=user_item[user_id].keys()
    for i in ru:
        pi=user_item[user_id][i]
        for j,wj in sorted(W[i].items(),key=operator.itemgetter(1),reverse=True)[0:K]:  #排序选取前几个评分较高的
            if j in ru:
                continue
            rank[j]=float(0)
    for i in ru:
        pi=user_item[user_id][i]
        for j,wj in sorted(W[i].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
            if j in ru:
                continue
            rank[j]+=float(pi)*wj
    return rank                                  #返回给用户推荐的物品及其有效的值

def ItemCFRecommend(user_item,K,N):    #user_item={user,item,rating} W为评分矩阵，K为取前面的排行值,N为返回推荐物品的个数
    users=user_item.keys()
    W=ItemSimilarity(user_item)
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=Recommendation1(user_item,i,W,K)
        rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:N]
        for j,item in rank:
            Recomendation[i].add(j)
    return Recomendation

def ItemCFRecommendIUF(user_item,K,N):   #user_item={user,item,rating} W为评分矩阵，K为取前面的排行值
    users=user_item.keys()
    W=ItemSimilarity1(user_item)
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=Recommendation1(user_item,i,W,K)
        rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:N]
        for j,item in rank:
            Recomendation[i].add(j)
    return Recomendation

def ItemCFRecommendtime(user_item,user_item1,K,alpha,T,N):   #user_item={user,item,tm}  W为评分矩阵，K为取关联的数量  alpha为参数选择{0-1},T为选择的时间戳
    users=user_item.keys()                                              #user_item1={user,item,ratings}
    W=ItemSimilaritytime(user_item,alpha)
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=Recommedationtime(user_item,user_item1,i,W,K,T,alpha)
        rank=sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:N]
        for j,item in rank:
            Recomendation[i].add(j)
    return Recomendation
    #Recommendation={user:set()} set()