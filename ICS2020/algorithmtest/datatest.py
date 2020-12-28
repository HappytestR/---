#本程序负责数据集的处理
#数据分为四种  无上下文信息的隐性反馈数据集  无上下文信息的显性反馈数据集   有上下文信息的隐性反馈数据集
#本此采用的数据集为有上下文的显性反馈数据集    (UserID,ItemID,sorces,timestamp)   包含四条内容
__explain__='__如下所示__'
'''
    本部分实现的内容主要是在于数据的初始化部分，包含了几个算法使用需要用到的例子
'''
import csv
import random
class Initdata:
    def __init__(self):
        self.user_item_ratings={}    #{user,item,ratings}
        self.item_user_ratings={}    #{item,user,ratings}
        self.movies={}               #{movieId,movietitle}
        self.user_item_tm={}         #{user_item_tm}
        self.item_user_tm={}         #{item,user,tm}
        self.movie_tags={}           #{movieId,tags}
        self.user_item_tags={}       #{user,item,item_tags}
        self.tags=set()              #得到所有的标签
        self.tag1=set()              #另一个文件的标签
        self.user_item_tag={}        #另一个文件的{user,item,tag}
        self.movices_tag={}          #另一个文件的{movice_id,tag}
        self.filename_data = 'D:/python/ICS2020/data/ratings.csv'
        self.filename_movies = 'D:/python/ICS2020/data/movies.csv'
        self.filename_tags='D:/python/ICS2020/data/tags.csv'
        self.__InitDa()
    def __InitDa(self):
        count_data = 0
        count_movie = 0
        file_data = csv.reader(open(self.filename_data))
        try:
            for line in file_data:
                try:
                    userId = line[0];itemId = line[1];rating = line[2];timeStamp = line[3]
                    self.user_item_ratings.setdefault(userId,{})
                    self.item_user_ratings.setdefault(itemId, {})
                    self.user_item_tm.setdefault(userId,{})
                    self.item_user_tm.setdefault(itemId,{})
                    self.user_item_ratings[userId][itemId]=rating
                    self.item_user_ratings[itemId][userId]=rating
                    self.user_item_tm[userId][itemId] = timeStamp
                    self.item_user_tm[itemId][userId]=timeStamp
                    count_data += 1
                except Exception as e:
                    continue
            print('data_count : ', count_data)
        except Exception as e:
            print(e.__context__)
        finally:
            file_movies = csv.reader(open(self.filename_movies))
            try:
                for line in file_movies:
                    try:
                        movie_id = line[0];movie_title = line[1]  # 电影类型
                        movie_tag=line[2].split("|")
                        for i in movie_tag:
                            if i not in self.tags:
                                self.tags.add(i)
                        self.movie_tags[movie_id]=movie_tag
                        self.movies[movie_id] = movie_title
                        count_movie += 1
                    except Exception as e:
                        continue
                print('movie_count : ', count_movie)
            except Exception as e:
                print('movie_count : ', count_movie)
            finally:
                file_tags=csv.reader(open(self.filename_tags))
                try:
                    for line in file_tags:
                        try:
                            user_id=line[0];movie_id=line[1];tag=line[2]
                            if tag not in self.tag1:
                                self.tag1.add(tag)
                            self.user_item_tag.setdefault(user_id,{})
                            if movie_id not in self.user_item_tag[user_id]:
                                self.user_item_tag[user_id][movie_id]=set()
                            self.user_item_tag[user_id][movie_id].add(tag)
                            self.movies_tag[movie_id]=movie_tag
                        except Exception as e:
                            continue
                except Exception as e:
                    print("数据初始化完成，请使用相关的函数进行调用")
                finally:
                    print("数据初始化完成，请使用相关的函数进行调用")
    def getUser_item(self):
        return self.user_item_ratings
    def getItem_user(self):
        return self.item_user_ratings
    def getUser_itemT(self):
        return self.user_item_tm
    def getItem_userT(self):
        return self.item_user_tm
    def getmoviceTitle(self):
        return self.movies
    def getmovicetags(self):
        return self.movie_tags
    def getUser_itemtags(self):            #得到用户的{user,item,item_tags}
        key=self.user_item_ratings.keys()
        for i in key:
            self.user_item_tags.setdefault(i,{})
            key1=self.user_item_ratings[i].keys()
            for j in key1:
                try:
                    self.user_item_tags[i][j]=self.movie_tags[j]
                except Exception as e:
                    continue
        return self.user_item_tags
    def gettags(self):
        return self.tags
    def show(self,recommend):
        key=recommend.keys()
        print("给用户推荐的电影为：（用户ID  ,  推荐电影如下）")
        for i in key:
            print("\n")
            ret=recommend[i]
            print("( "+i+" : ",end="")
            for j in ret:
                try:
                    print(self.movies[j],end=" ")
                except Exception as e:
                    continue
    def train_testsplitData(self,M,k,seed):          #M为划分的次数，0<=k<=M-1
        traindata=train()                            #每次选取不同的k和相同的随机数种子seed
        testdata=test()
        random.seed(seed)
        num=0
        for user,item in self.user_item_ratings.items():
            for j,rate in item.items():
                if num%M==k:
                    num+=1
                    try:
                        testdata.user_item_tm.setdefault(user,{})
                        testdata.item_user_tm.setdefault(j,{})
                        testdata.user_item_ratings.setdefault(user,{})
                        testdata.item_user_ratings.setdefault(j,{})
                        testdata.user_item_ratings[user][j]=rate
                        testdata.item_user_ratings[j][user]=rate
                        testdata.user_item_tm[user][j]=self.user_item_tm[user][j]
                        testdata.item_user_tm[j][user]=self.item_user_tm[j][user]
                        testdata.movie_tags[j]=self.movie_tags[j]
                        testdata.movies[j]=self.movies[j]
                    except Exception as e:
                        continue
                else:
                    num+=1
                    try:
                        traindata.user_item_tm.setdefault(user, {})
                        traindata.item_user_tm.setdefault(j, {})
                        traindata.user_item_ratings.setdefault(user, {})
                        traindata.item_user_ratings.setdefault(j, {})
                        traindata.user_item_ratings[user][j] = rate
                        traindata.item_user_ratings[j][user] = rate
                        traindata.user_item_tm[user][j] = self.user_item_tm[user][j]
                        traindata.item_user_tm[j][user] = self.item_user_tm[j][user]
                        traindata.movie_tags[j] = self.movie_tags[j]
                        traindata.movies[j] = self.movies[j]
                    except Exception as e:
                        continue
        return traindata,testdata                      #数据集的划分

class train():        #得到训练集
    def __init__(self):
        self.user_item_ratings={}    #{user,item,ratings}
        self.item_user_ratings={}    #{item,user,ratings}
        self.movies={}               #{movieId,movietitle}
        self.user_item_tm={}         #{user_item_tm}
        self.item_user_tm={}         #{item,user,tm}
        self.movie_tags={}           #{movieId,tags}
        self.user_item_tags={}       #{user,item,item_tags}
        self.tags=set()              #得到所有的标签
        def getUser_itemtags(self):  # 得到用户的{user,item,item_tags}
            key = self.user_item_ratings.keys()
            for i in key:
                self.user_item_tags.setdefault(i, {})
                key1 = self.user_item_ratings[i].keys()
                for j in key1:
                    try:
                        self.user_item_tags[i][j] = self.movie_tags[j]
                    except Exception as e:
                        continue
            return self.user_item_tags

class test():         #得到测试集合
    def __init__(self):
        self.user_item_ratings={}    #{user,item,ratings}
        self.item_user_ratings={}    #{item,user,ratings}
        self.movies={}               #{movieId,movietitle}
        self.user_item_tm={}         #{user_item_tm}
        self.item_user_tm={}         #{item,user,tm}
        self.movie_tags={}           #{movieId,tags}
        self.user_item_tags={}       #{user,item,item_tags}
        self.tags=set()              #得到所有的标签
        def getUser_itemtags(self):  # 得到用户的{user,item,item_tags}
            key = self.user_item_ratings.keys()
            for i in key:
                self.user_item_tags.setdefault(i, {})
                key1 = self.user_item_ratings[i].keys()
                for j in key1:
                    try:
                        self.user_item_tags[i][j] = self.movie_tags[j]
                    except Exception as e:
                        continue
            return self.user_item_tags

if __name__=='__main__':             #测试数据集的划分是否正确
    datalist=Initdata()
    traindata,testdata=datalist.train_testsplitData(8,4,10)
    user_item=datalist.getUser_item()
    tags=datalist.tag1
    tagnum=0
    for i in tags:
        tagnum+=1
    print(tagnum)
    user=0;item=0
    for i in user_item.keys():
        user+=1
        for j in user_item[i].keys():
            item+=1
    print("(user number, item number)\n({},{})".format(user,item))
    user=0;item=0
    for i in traindata.user_item_ratings.keys():
        user+=1
        for j in traindata.user_item_ratings[i].keys():
            item+=1
    print("(user number, item number)\n({},{})".format(user,item))
    user=0;item=0
    for i in testdata.user_item_ratings.keys():
        user+=1
        for j in testdata.user_item_ratings[i].keys():
            item+=1
    print("(user number, item number)\n({},{})".format(user,item))

