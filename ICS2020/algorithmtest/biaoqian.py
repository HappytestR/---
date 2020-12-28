#基于标签的的推荐系统设置
__explain__='__如下所示__'
'''
    一个用户标签行为的数据集一般由一个三元组的集合表示
    对算法的改进主要在于三方面
    1.TF-IDF   2.数据稀疏度    3.标签请理
'''
import math
import operator
def Initdata1(item_user,movie_tags,tags):     #计算item_tags矩阵{user,item,item_tags}
    key1=item_user.keys()                     #在这里的化标签的标出应该在文件tags.csv中，从那里面获取数据
    item_tags={}
    for i in key1:
        item_tags.setdefault(i,{})
        for j in tags:
            item_tags[i][j]=0
    for i in movie_tags.keys():
        for j in movie_tags[i]:
            try:
                item_tags[i][j]+=1
            except Exception as e:
                continue
    return item_tags

def CosineSim(item_tags,i,j):   #计算物品标签的相似度
    ret=0
    for b,wib in item_tags[i].items():
        if b in item_tags[j]:
            ret+=wib*item_tags[j][b]
    ni=0
    nj=0
    for b,w in item_tags[i].items():
        ni+=w*w
    if ret==0:
        return 0
    return ret/math.sqrt(ni*nj)

def Wpinfengereate(item_user,movie_tags,tags):   #生成用户的评分矩阵W item_user={item,user,rating}
    item_tags=Initdata1(item_user,movie_tags,tags)
    W=dict()
    key1=item_user.keys()
    for i in key1:
        W.setdefault(i,{})
        for j in key1:
            if i==j:
                continue
            W[i][j]=CosineSim(item_tags,i,j)
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

def RecommendBQ(item_user,user_item,movie_tags,tags,K,N):       #标签推荐系统  W为物品评分矩阵，K为选取前多少个物品,N为推荐物品的个数
    users=user_item.keys()
    W=Wpinfengereate(item_user,movie_tags,tags)
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=Recommendation1(user_item,i,W,K)
        R=sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:N]
        for j,item in R:
            Recomendation[i].add(j)
    return Recomendation

def InitStat(records):  #从records中统计出user_tags和tag_items
    user_tags=dict()  #records是存储标签的三元组records[i]=[user,item,tag]
    tag_items=dict()
    user_items=dict()
    for user,item in records.items():
        key1=records[user].keys()
        for j in key1:
            key2=records[user][j]
            for tag in key2:
                user_tags.setdefault(user,{})
                user_tags[user][tag]=1
                tag_items.setdefault(tag,{})
                tag_items[tag][j]=1
                user_items.setdefault(user,{})
                user_items[user][j]=1
    return user_tags,user_items,tag_items

def RecommendBQ1(user,records):
    recommend_items=dict()
    user_tags,user_items,tag_items=InitStat(records)
    tagged_items=user_items[user]
    for tag,wut in user_tags[user].items():
        for item,wti in tag_items[tag].items():
            if item in tagged_items:
                continue
            if item not in recommend_items:
                recommend_items[item]=wut*wti
            else:
                recommend_items[item]+=wut*wti
    return recommend_items

def RecommendBQ2(records,N):  #N设置的为阈值，输入为0-10
    recommend={}
    users=records.keys()
    Recomendation={}
    for i in users:
        Recomendation[i]=set()
        rank=RecommendBQ1(i,records)
        R=sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:N]
        for j,item in R:
            Recomendation[i].add(j)
    return Recomendation

