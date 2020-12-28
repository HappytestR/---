#基于图的模型
__explain__='__如下所示__'
'''
    基于图的模型其实就是二分图，在这里也可以等待与user_item模型
    基于图的模型主要在于求解两个用户图之间的距离长短，一般默认为1
    这里实现的是最简单的基于图的实现方式
'''
def PersonalRank(G,alpha,root,N): #从实际上来说,G=user_item  alpha为学习速率,N为阈值
    rank=dict()
    rank={x:0 for x in G.keys()}
    rank[root]=1
    for k in range(20):
        tmp={x:0 for x in G.keys()}
        for i,ri in G.items():
            for j,wij in ri.items():
                if j not in tmp:
                    tmp[j]=0
                tmp[j]+=0.6*rank[i]/(1.0*len(ri))
                if j==root:
                    tmp[j]+=1-alpha
        rank=tmp
    return rank

def Recommendtu(user_item,alpha,N):    #user_item={user,item,rating}   alpha为参数，N为控制学习的阈值
    users=user_item.keys()
    remmend={}
    for i in users:
        remmend.setdefault(i,set())
        rank=(user_item,alpha,i,N)
        for j in rank:
            remmend[i].add(j)
    return remmend           #返回{user,items}

