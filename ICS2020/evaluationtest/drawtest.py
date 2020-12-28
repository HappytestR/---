#本文件主要实现绘图对比的功能，功能需要逐步完成来实现
'''__explain__='__如下所示__'

    本模块负责实现算法的评估数据可视化部分

class drawtest():
    def __init__(self):
        print("开始进行数据可视化")

'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties








def plot(dict, lists):  # 画出函数图像
    fig = plt.figure()
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20)  # 临时显示中文
    plt.xlabel('召回率(R)', fontproperties=font)
    plt.ylabel('精确率(P)', fontproperties=font)
    x = np.arange(0, 0.5, 0.05)
    y = np.arange(0, 0.5, 0.05)
    plt.xticks(x)
    plt.yticks(y)
    plt.plot(dict, lists)
    plt.show()








def caculate():

    num_real = 0
    # 初始化样本标签，假设1为正例，0为负例
    trainlabel = np.random.randint(0, 2, size=100)
    # 产生100个概率值（置信度），即单个样本值为正例的概率
    traindata = np.random.rand(100)
    # 将样本数据为正例概率从大到小排序返回索引值
    sortedTraindata = traindata.argsort()[::-1]
    k = []
    v = []
    # 统计样本中实际正例的数量
    num = np.sum(trainlabel == 1)
    for i in range(100):
        num_guess = i + 1  # 假设为真的数量
        for j in range(0, i + 1):
            a = sortedTraindata[j]
            if trainlabel[a] == 1:
                num_real += 1  # 假设为真中实际也为真的数量
        p = float(num_real / (num_guess))
        r = float(num_real / (num))
        v.append(p)
        k.append(r)
        num_real = 0
    plot(k, v)

if __name__ == '__main__':
    caculate()
