import numpy as np
import operator

# 构造数据
def createDataSet():
    group = np.array([[1.0, 2.0], [1.2, 0.1], [0.1, 1.4], [0.3, 3.5]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

# 使用KNN进行分类
def classify(input, dataSet, label, k):
    dataSize = dataSet.shape[0]
    # 计算欧式距离
    diff = np.tile(input, (dataSize, 1)) - dataSet
    sqdiff = diff ** 2
    squareDist = np.sum(sqdiff, axis=1)
    dist = squareDist ** 0.5

    sortedDistIndex = np.argsort(dist)

    classCount = {}

    for i in range(k):
        voteLabel = label[sortedDistIndex[i]]
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
    
    maxCount = 0
    for key, value in classCount.items():
        if value > maxCount:
            maxCount = value
            classes = key

    return classes

