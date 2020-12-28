#时间上下文推荐算法实现
__explain__='__如下所示__'
'''
    这一部分的内容其实就是简单的基于时间上下文的推荐算法
    但是这一部分仅限于测试，而实际的应用已经结合在了userCF和itemCF中
'''
import math
import operator
#测试部分，没有什么实际意义。

def RecentPopularity(records,alpha,T):         #records为数据集{user,item,timestamp 时间戳}  alpha为系数影响因子，T为自定义的标签
    ret=dict()
    for user in records.keys():   #user为user
        for i in records[user].keys():     #i为item
            tm=records[user][i]     #tm为物品对应的时间戳
            if tm>=T:
                continue
            ret[i]=1/(1.0+alpha*(int(T)-int(tm)))
    return ret
