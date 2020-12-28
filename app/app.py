from flask import Flask,render_template
from flask import request,current_app
from ICS2020.algorithmtest.datatest import Initdata
from ICS2020.algorithmtest.LFM import RecommendLFM
from ICS2020.algorithmtest.ItemCF import ItemCFRecommend,ItemCFRecommendIUF,ItemCFRecommendtime
from ICS2020.algorithmtest.UserCF import UserCFRecommedation,UserCFRecommendationIIF,UserCFRecommendationtime
#from ICS2020.algorithmtest.time import RecentPopularity
from ICS2020.algorithmtest.biaoqian import RecommendBQ,RecommendBQ2
from ICS2020.algorithmtest.SVGtuijian import RecommendSVD
from ICS2020.algorithmtest.tu import Recommendtu
app=Flask(__name__)
Username='12'      #默认的用户姓名
K=5         #选取默认参数为5
N=5         #选取的默认参数为5
alpha=0.9   #选取的默认参数为0.9
lamb=0.01   #选取的默认参数为0.01
alpha1=0.0000000001
T=964982400  #选取的时间戳
T1=5   #定义迭代次数
class Init1app():             #传入所需要的数据
    def __init__(self):
        print("数据初始化开始，程序框架正逐步计算中，本程序的缺点在于没有将训练的数据存储到数据库中，导致程序运行时需要维护很大的缓存")
        self.recommendUserCF1={}          #推荐系统一
        self.recommendUserCF2={}          #推荐系统二
        self.recommendUserCF3={}          #推荐系统三
        self.recommendItemCF1={}          #推荐系统四
        self.recommendItemCF2={}          #推荐系统五
        self.recommendItemCF3={}          #推荐系统六
        self.recommendSVD={}              #推荐系统七
        self.recommendLFM={}              #推荐系统八
        self.recommendbiaoqian={}         #推荐系统九
        self.moviceTitle={}               #电影标题
        self.movices={}                   #用户喜欢的电影
        self.datalist={}                  #初始化数据集
    def Init1(self):           #负责程序的初始化
        self.datalist=Initdata()
        self.moviceTitle=self.datalist.getmoviceTitle()
        traindata,testdata=self.datalist.train_testsplitData(8,4,100)
        #user_item=self.datalist.getUser_item()
        #item_user=self.datalist.getItem_user()
        #user_itemT=self.datalist.getUser_itemT()
        #item_userT=self.datalist.getItem_userT()
        records=self.datalist.getUser_itemtags()
        user_item=testdata.user_item_ratings
        item_user=testdata.item_user_ratings
        user_itemT=testdata.user_item_tm
        item_userT=testdata.item_user_tm
        for i in user_item.keys():
            self.movices[i]=user_item[i].keys()
        self.recommendUserCF1=UserCFRecommedation(user_item,item_user,K,N)
        self.recommendUserCF2=UserCFRecommendationIIF(user_item,item_user,K,N)
        self.recommendUserCF3=UserCFRecommendationtime(user_itemT,item_userT,K,alpha1,T,N)
        self.recommendItemCF1=ItemCFRecommend(user_item,K,N)
        self.recommendItemCF2=ItemCFRecommendIUF(user_item,K,N)
        self.recommendItemCF3=ItemCFRecommendtime(user_itemT,user_item,K,alpha1,T,N)
        self.recommendSVD=RecommendSVD(user_item,item_user,20,T1,alpha,lamb,N)
        self.recommendLFM=RecommendLFM(user_item,5,T1,alpha,lamb,N)
        #self.recommendSVD=self.recommendLFM
        self.recommendbiaoqian=RecommendBQ2(records,N)

class Init2app():
    def __init__(self,Init1app,username):
        self.recommendUserCF1=Init1app.recommendUserCF1[username]
        self.recommendUserCF2=Init1app.recommendUserCF2[username]
        self.recommendUserCF3=Init1app.recommendUserCF3[username]
        self.recommendItemCF1=Init1app.recommendItemCF1[username]
        self.recommendItemCF2=Init1app.recommendItemCF2[username]
        self.recommendItemCF3=Init1app.recommendItemCF3[username]
        self.recommendSVD=Init1app.recommendSVD[username]
        self.recommendLFM=Init1app.recommendLFM[username]
        self.recommendbiaoqian=Init1app.recommendbiaoqian[username]
        self.moviceTitle=Init1app.moviceTitle
        self.movices=Init1app.movices[username]


'''
class Init2app():
    def __init__(self,Recommend,username,movices):
        self.recommendUserCF1=Recommend[username]
        self.recommendUserCF2=Recommend[username]
        self.recommendUserCF3=Recommend[username]
        self.recommendItemCF1=Recommend[username]
        self.recommendItemCF2=Recommend[username]
        self.recommendItemCF3=Recommend[username]
        self.recommendSVD=Recommend[username]
        self.recommendLFM=Recommend[username]
        self.recommendbiaoqian=Recommend[username]
        self.moviceTitle=movices
        self.movices=Recommend[username]
'''


Initdatatest=Init1app()
Initdatatest.Init1()

def Initapp():
    datalist=Initdata()
    user_item=datalist.getUser_item()
    item_user=datalist.getItem_user()
    Recommend1=UserCFRecommedation(user_item,item_user,5,5)
    movices1=datalist.getmoviceTitle()
    return Recommend1,movices1

recommend,movices=Initapp()
DATANUM1=set()
DATANUM2={}
for i in range(5):
    str1="/static/img/test"+str(i)+'.jpg'
    DATANUM1.add(str1)
#存放入数据库中就会变得十分简单了
DATANUM2["/static/img/user1.png"]="UserCF1的推荐算法评估"
DATANUM2["/static/img/user1chart.png"]="UserCF1的推荐算法评估"
DATANUM2["/static/img/user2.png"]="UserCF2的推荐算法评估"
DATANUM2["/static/img/user2chart.png"]="UserCF2的推荐算法评估"
DATANUM2["/static/img/user3.png"]="UserCF3的推荐算法评估"
DATANUM2["/static/img/user3chart.png"]="UserCF3的推荐算法评估"
DATANUM2["/static/img/item1.png"]="ItemCF1的推荐算法评估"
DATANUM2["/static/img/item1chart.png"]="ItemCF1的推荐算法评估"
DATANUM2["/static/img/item2.png"]="ItemCF2的推荐算法评估"
DATANUM2["/static/img/item2chart.png"]="ItemCF2的推荐算法评估"
DATANUM2["/static/img/item3.png"]="ItemCF3的推荐算法评估"
DATANUM2["/static/img/item3chart.png"]="ItemCF3的推荐算法评估"
DATANUM2["/static/img/LFM.png"]="LFM推荐算法评估"
DATANUM2["/static/img/LFMchart.png"]="LFM推荐算法评估"

@app.route('/pinggumoxing',methods=['GET','POST'])
def pinggumoxing():
    return render_template('recommend.html', DATANUM=5, DATANUM1=DATANUM1, DATANUM2=DATANUM2)

@app.route('/pinggu',methods=['GET','POST'])
def pinggu():
    if request.method=='POST':
        Username=request.form['user_id']
    else:
        Username=request.args.get('user_id')
    #alldata=Init2app(recommend,Username,movices)
    alldata=Init2app(Initdatatest,Username)
    return render_template('recommend1.html',ALLDATA=alldata,Username=Username)
    #return render_template('Hello,world!')

@app.route('/')
def index():
    alldata=Init2app(Initdatatest,Username)
    #alldata=Init2app(recommend,Username,movices)
    return render_template('recommend1.html',ALLDATA=alldata,Username=Username)
    #return render_template('recommend.html',DATANUM=5,DATANUM1=DATANUM1,DATANUM2=DATANUM2)


if __name__=='__main__':
    app.run()       #运行python fask app  程序