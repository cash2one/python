# coding:utf-8
__author__ = '613108'

from numpy import *
import operator, sys


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inx, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffmat = tile(inx, (dataSetSize, 1)) - dataSet
    sqDiffmat = diffmat ** 2
    sqDistances = sqDiffmat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    # labelsOk=[[labels[i],sortedDistIndicies[i]] for i in range(len(labels))]
    # labelsOk=zip(labels,sortedDistIndicies)
    # print labelsOk
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        # print classCount.get(voteIlabel, 0)
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
        # print classCount[voteIlabel]
        # print classCount
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(fileName='datingTestSet2.txt'):
    fileName = r'C:\Users\613108\Desktop\Project\machineLearning\machinelearninginaction\Ch02' + '/' + fileName
    fr = open(fileName)
    arrayOfLines = fr.readlines()
    fr.close()
    numberOfLines = len(arrayOfLines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    print minVals
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    # normDataSet=zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def pltShow(x, y, labels):
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, y, 15.0 * array(labels), 15.0 * array(labels))
    plt.show()


def datingClassTest(k=3):
    hoRatio = 0.05
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], k)
        print 'The classifier came back with : %d,the real answer is : %d' % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print 'The total error rate is : %f' % (errorCount / float(numTestVecs))


if __name__ == '__main__':
    # group, labels = createDataSet()
    # test = classify0([1, 1], group, labels, 3)
    # print test

    # datingDataMat, datingLabels = file2matrix()
    # normDataSet,ranges,minVals=autoNorm(datingDataMat)
    # print normDataSet
    # print datingDataMat
    # print datingLabels
    # pltShow(datingDataMat[:,1],datingDataMat[:,0],datingLabels)

    datingClassTest()
