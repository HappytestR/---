#UserCF(基于用户的协同过滤算法实现）
import math
import operator
from ICS2020.Optimization.optimizationtest import UserSimilarity1,UserSimilaritytime,Recomendtime
__explaintion__='__如下所示__'
'''
    UserCFRecommend()函数为最简单的UserCF推荐算法
    UserCFRecommendationIIF()函数为更改相似度计算公式之后的推荐算法
    UserCFRecommendationtime()函数为基于时间的UserCF推荐算法,推荐alpha参数选取0.0000000001
    算法的返回均为字典格式{userId,set()}set()为推荐列表
'''

def UserSimilarity(item_user):   #计算用户之间的相似度
    item_users=dict()             #余弦相似度
    keys=item_user.keys()
    for i in keys:
        item_users[i]=set()
        keys1=item_user[i].keys()
        for j in keys1:
            item_users[i].add(j)
    C=dict()   #得到的n*n评分矩阵
    N=dict()
    keys=item_users.keys()
    for i in keys:     #初始化C
        users=item_users[i]
        for u in users:
            N[u]=0
            C.setdefault(u,{})
            for v in users:
                C[u][v]=0
    for i in keys:
        users=item_users[i]
        for u in users:
            N[u]+=1
            for v in users:
                if u==v:
                    continue
                C[u][v]+=1
    W=dict()
    for u,related_users in C.items():
        W.setdefault(u,{})
        for v,cuv in related_users.items():
            W[u][v]=cuv/math.sqrt(N[u]*N[v])
    return W
''' num=0
    for u in W.keys():
        for v in W[u].keys():
            num+=1
            print("({},{},{})".format(u,v,W[u][v]))
    print(num)
'''

def UserCFRecommend(user,user_item,W,K):   #度量UserCF算法中用户u对物品i的感兴趣程序
    rank=dict()
    interacted_items=user_item[user].keys()
    for v,wuv in sorted(W[user].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
        for i in user_item[v].keys():
            rvi=user_item[v][i]
            if i in interacted_items:
                continue
            rank[i]=float(0)
    for v,wuv in sorted(W[user].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
        for i in user_item[v].keys():
            rvi=user_item[v][i]
            if i in interacted_items:
                continue
            rank[i]+=wuv*float(rvi)
    return rank

def UserCFRecommedation(user_item,item_user,K,N):   #返回所有的推荐矩阵列表user_item={user,item,rating}
    users=user_item.keys()                        #返回所有的推荐矩阵列表item_user={item,user,rating}
    W=UserSimilarity(item_user)                                 #K为选取的个数
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=UserCFRecommend(i,user_item,W,K)
        rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:N]
        for item,j in rank:
            Recomendation[i].add(item)
    return Recomendation

def UserCFRecommendationIIF(user_item,item_user,K,N):  #返回所有的推荐矩阵列表item_user={item,user,rating}
    users=user_item.keys()                           #返回所有的推荐矩阵列表user_item={user,item,rating}
    W=UserSimilarity1(item_user)                        #K为选取的个数
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=UserCFRecommend(i,user_item,W,K)
        rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:N]
        for j,item in rank:
            Recomendation[i].add(j)
    return Recomendation

def UserCFRecommendationtime(user_item,item_user,K,alpha,T,N): #user_item={user,item,tm}   item_user={item,user,tm}  K为选取的个数  T为选取的时间戳
    users=user_item.keys()
    W=UserSimilaritytime(item_user,alpha)
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        #rank=Recomendtime(user_item,i,W,K,T,alpha)
        rank=Recomendtime(user_item,i,T,W,K,alpha)
        R=sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:N]
        for j,item in R:
            Recomendation[i].add(j)
    return Recomendation