#用于添加优化算法的部分
import math
import operator
#一.更改计算用户兴趣相似度的公式   UserCF-IIF
def UserSimilarity1(item_user):
    item_users=dict()
    keys=item_user.keys()
    for i in keys:
        item_users[i]=set()
        keys1=item_user[i].keys()
        for j in keys1:
            item_users[i].add(j)
    C=dict()
    N=dict()
    keys = item_users.keys()
    for i in keys:  # 初始化C
        users = item_users[i]
        for u in users:
            N[u] = 0
            C.setdefault(u, {})
            for v in users:
                C[u][v] = 0
    for i in keys:
        users = item_users[i]
        for u in users:
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                C[u][v] += 1/math.log(1+len(users))
    W=dict()
    for u,related_users in C.items():
        W.setdefault(u,{})
        for v,cuv in related_users.items():
            W[u][v]=cuv/math.sqrt(N[u]*N[v])
    return W

#二.对用户活跃度的改进   ItemCF-IUF
def ItemSimilarity1(user_item):
    users_item=dict()             #余弦相似度
    keys=user_item.keys()
    for i in keys:
        users_item[i]=set()
        keys1=user_item[i].keys()
        for j in keys1:
            users_item[i].add(j)
    C=dict()
    N=dict()
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
                C[u][v]+=1/math.log(1+len(items)*1.0)
    W=dict()
    for i,related_items in C.items():
        W.setdefault(i,{})
        for j,cij in related_items.items():
            W[i][j]=cij/math.sqrt(N[i]*N[j])
    return W

def guione(W):     #返回W评分矩阵中得分最高的
    temp=W.keys()
    temp1=0
    for i in temp:
        if (max(W[i].values()))>temp1:
            temp1=max(W[i].values())
    return temp1

#三.基于时间的ItemCF
def ItemSimilaritytime(user_item,alpha):
    users_item=dict()             #余弦相似度
    keys=user_item.keys()
    for i in keys:
        users_item[i]=set()
        keys1=user_item[i].keys()
        for j in keys1:
            users_item[i].add(j)
    C=dict()
    N=dict()
    keys = users_item.keys()
    for i in keys:  # 初始化C
        items = users_item[i]
        for u in items:
            N[u] = 0
            C.setdefault(u, {})
            for v in items:
                C[u][v] = 0
    for u,items in user_item.items():
        for i,tui in items.items():
            N[i]+=1
            for j,tuj in items.items():
                if i==j:
                    continue
                C[i][j]+=1/(1+alpha*abs(int(tui)-int(tuj)))
    W=dict()
    for i,related_items in C.items():
        W.setdefault(i,{})
        for j,cij in related_items.items():
            W[i][j]=cij/math.sqrt(N[i]*N[j])
    return W

def Recommedationtime(user_item,user_item1,user_id,W,K,t0,alpha):   #基于时间的ItemCF推荐系统,user_item是用户数据，user_id是需要推荐用户的名称，W是评分矩阵，K是选取前K个值，to是选取的时间戳
    rank=dict()                  #或者集成{user,item,ratings,timestrap}  或者{user,item,tm}和{user,item,rating}这两种选择
    ru=user_item[user_id].keys()      #在这里选取的是第二种方式进行计算
    for i in ru:
        pi=user_item[user_id][i]
        for j,wj in sorted(W[i].items(),key=operator.itemgetter(1),reverse=True)[0:K]:  #排序选取前几个评分较高的
            if j in ru:
                continue
            rank[j]=float(0)
    for i in ru:
        pi=user_item1[user_id][i]
        for j,wj in sorted(W[i].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
            if j in ru:
                continue
            tuj=user_item[user_id][i]
            rank[j]+=float(pi)*wj/(1+alpha*(int(t0)-int(tuj)))
    return rank

#基于时间的UserCF改进算法
def UserSimilaritytime(item_user,alpha):   # ser_item={user,item,tm}
    #时间错矩阵    item_user即为{item,user,tm矩阵}
    C=dict()   #得到的n*n评分矩阵
    N=dict()
    keys=item_user.keys()
    for i in keys:     #初始化C
        users=item_user[i]
        for u in users:
            N[u]=0
            C.setdefault(u,{})
            for v in users:
                C[u][v]=0
    for i,users in item_user.items():
        for u,tui in users.items():
            N[u]+=1
            for v,tvi in users.items():
                if u==v:
                    continue
                C[u][v]+=1/(1+alpha*abs(int(tui)-int(tvi)))   #u,v为用户之间的相似度
    W=dict()
    for u,related_users in C.items():
        W.setdefault(u,{})
        for v,cuv in related_users.items():
            W[u][v]=cuv/math.sqrt(N[u]*N[v])
    return W         #返回用户-用户相似度矩阵

def Recomendtime(user_item,user,T,W,K,alpha):   #T是定义的时间戳，W是评分矩阵,K是选取的前K个排行值,alpha是参数
    rank=dict()
    interacted_items=user_item[user]   #得到用户已经有的
    for u,wuv in sorted(W[user].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
        for i,tvi in user_item[u].items():
            if i in interacted_items:  #判断是否在用户已有的矩阵上
                continue
            rank[i]=0
    for u,wuv in sorted(W[user].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
        for i,tvi in user_item[u].items():
            if i in interacted_items:  #判断是否在用户已有的矩阵上
                continue
            rank[i]+=wuv/(1+alpha*(int(T)-int(tvi)))
    return rank

#时间段图模型