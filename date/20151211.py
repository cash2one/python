# coding:utf8
__author__ = '613108'
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\msyh.ttf", size=10)


def runplt():
    plt.figure()
    plt.title('匹萨价格与直径数据', fontproperties=font)
    plt.xlabel('直径（英寸）', fontproperties=font)
    plt.ylabel('价格（美元）', fontproperties=font)
    plt.axis([0, 25, 0, 25])
    plt.grid(True)
    return plt


x_train = [[6], [8], [10], [14], [18]]
y_train = [[7], [9], [13], [17.5], [18]]
x_test = [[6], [8], [11], [16]]
y_test = [[8], [12], [15], [18]]
regressor = LinearRegression()
regressor.fit(x_train, y_train)
xx = np.linspace(0, 26, 100)
yy = regressor.predict(xx.reshape(xx.shape[0], 1))
plt = runplt()
plt.plot(x_train, y_train, 'k.')
plt.plot(xx, yy)

quadratic_featurizer = PolynomialFeatures(degree=2)
x_train_quadratic = quadratic_featurizer.fit_transform(x_train)
x_test_quadratic = quadratic_featurizer.transform(x_test)
regressor_quadratic = LinearRegression()
regressor_quadratic.fit(x_train_quadratic, y_train)
xx_quadratic = quadratic_featurizer.transform(xx.reshape(xx.shape[0], 1))
plt.plot(xx, regressor_quadratic.predict(xx_quadratic), 'r-')

# PART2 Logistic Regression
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r'c:\windows\fonts\msyh.ttf', size=10)
import numpy as np

plt.figure()
plt.axis([-6, 6, 0, 1])
plt.grid(True)
x = np.arange(-6, 6, 0.1)
y = 1 / (1 + np.e ** (-x))
plt.plot(x, y, 'b-')

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split

df = pd.read_csv(r'd:\ml\SMSSpamCollection.txt', delimiter='\t', header=None)
x_train_raw, x_test_raw, y_train, y_test = train_test_split(df[1], df[0])

vectorizer = TfidfVectorizer()
x_train = vectorizer.fit_transform((x_train_raw))
x_test = vectorizer.transform(x_test_raw)

classifier = LogisticRegression()
classifier.fit(x_train, y_train)
predictions = classifier.predict(x_test)

for i, prediction in enumerate(predictions[-20:]):
    print('预测模型：%s. 信息：%s' % (prediction, y_test.iloc[i]))


from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

y_test = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
y_pred = [0, 1, 0, 0, 0, 0, 0, 1, 1, 1]
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)
plt.title(u'混淆矩阵', fontproperties=font)
plt.colorbar(4)
plt.ylabel(u'实际类型', fontproperties=font)
plt.xlabel(u'预测类型', fontproperties=font)

