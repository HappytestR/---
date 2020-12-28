#负责程序运行的主框架部分
__explain__='__如下所示__'
'''
    本程序负责整个框架的运行部分
    可以从整个框架的执行训练出整个算法的对比度等比较
'''
from ICS2020.algorithmtest.datatest import Initdata
from ICS2020.algorithmtest.LFM import RecommendLFM
from ICS2020.algorithmtest.ItemCF import ItemCFRecommend,ItemCFRecommendIUF,ItemCFRecommendtime
from ICS2020.algorithmtest.UserCF import UserCFRecommedation,UserCFRecommendationIIF,UserCFRecommendationtime
#from ICS2020.algorithmtest.time import RecentPopularity
from ICS2020.algorithmtest.biaoqian import RecommendBQ,RecommendBQ2
from ICS2020.algorithmtest.SVGtuijian import RecommendSVD
from ICS2020.algorithmtest.tu import Recommendtu
from ICS2020.evaluationtest.drawtest import drawtest
from ICS2020.evaluationtest.evaluation import evaluation
if __name__=='__main__':
    print("整个程序框架开始运行")
    datalist=Initdata()
    num=0
    traindata,testdata=datalist.train_testsplitData(8,4,10)
    user_item=testdata.user_item_ratings
    item_user=datalist.getItem_user()
    user_itemT=testdata.user_item_tm
    item_userT=testdata.item_user_tm
    recommend=RecommendSVD(user_item,item_user,20,2,0.02,0.01,5)
    datalist.show(recommend)