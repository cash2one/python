# coding:utf8
__author__ = 'Administrator'

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\msyh.ttf", size=10)
import numpy as np

X0 = np.array([7, 5, 7, 3, 4, 1, 0, 2, 8, 6, 5, 3])
X1 = np.array([5, 7, 7, 3, 6, 4, 0, 2, 7, 8, 5, 7])
plt.figure()
plt.axis([-1, 9, -1, 9])
plt.grid(True)
plt.plot(X0, X1, 'k.')
plt.xlabel('this is x_axis', fontproperties=font)

############################################################
import numpy as np

cluster1 = np.random.uniform(0.5, 1.5, (2, 10))
cluster2 = np.random.uniform(3.5, 4.5, (2, 10))
X = np.hstack((cluster1, cluster2)).T
plt.figure()
plt.axis([0, 5, 0, 5])
plt.plot(X[:, 0], X[:, 1], 'k.')

############################################################
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

K = range(1, 10)
meandistortions = []
for k in K:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    tt = cdist(X, kmeans.cluster_centers_, metric='euclidean')
    meandistortions.append(sum(np.min(cdist(X, kmeans.cluster_centers_, metric='euclidean'), axis=1)) / X.shape[0])
plt.plot(K, meandistortions, 'bx-')
plt.xlabel('K')
plt.ylabel(u'平均畸变程序', fontproperties=font)

############################################################
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics


def plt_t(plt):
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xlabel(u'x1水平轴表现', fontproperties=font)
    plt.ylabel(u'y1垂直轴表现', fontproperties=font)


font = FontProperties(fname=r'c:\windows\fonts\msyh.ttf', size=10)
x1 = np.array([1, 2, 3, 1, 5, 6, 5, 5, 6, 7, 8, 9, 7, 9])
x2 = np.array([1, 3, 2, 2, 8, 6, 7, 6, 7, 1, 2, 1, 1, 3])
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
plt.figure(figsize=(15, 8))
plt.subplot(2, 3, 1)
plt_t(plt)
plt.title(u'样本总体表现', fontproperties=font)
plt.scatter(x1, x2)

colors = 'b g r c m y k b'.split(' ')
markers = 'o s D v ^ p * +'.split(' ')

tests = [2, 3, 4, 5, 8]
subplot_counter = 1

for t in tests:
    subplot_counter += 1
    plt.subplot(2, 3, subplot_counter)
    kmeans_model = KMeans(n_clusters=t).fit(X)
    for i, l in enumerate(kmeans_model.labels_):
        plt.plot(x1[i], x2[i], color=colors[l], marker=markers[l], ls='None')
        plt_t(plt)
        plt.title(u'K=%s，轮廓系数=%0.3f' % (t, metrics.silhouette_score(X, kmeans_model.labels_, metric='euclidean')),
                  fontproperties=font)

############################################################
import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import mahotas as mh
import matplotlib.pyplot as plt

original_img = np.array(mh.imread('C:\Users\Public\Pictures\Sample Pictures\Desert.jpg'), dtype=float) / 255
original_dimensions = width, height, depth = tuple(original_img.shape)
image_flattend=np.reshape(original_img,(width*height,depth))
image_array_sample=shuffle(image_flattend,random_state=0)[:1000]
estimator=KMeans(n_clusters=64,random_state=0)
estimator.fit(image_array_sample)
cluster_assigments=estimator.predict(image_flattend)
compressed_palette=estimator.cluster_centers_
compressed_img=np.zeros((width,height,compressed_palette.shape[1]))
label_idx=0
for i in range(width):
    for j in range(height):
        compressed_img[i][j]=compressed_palette[cluster_assigments[label_idx]]
        label_idx+=1
plt.subplot(122)
plt.title('Original Image')
plt.imshow(original_img)
plt.axis('off')
plt.subplot(121)
plt.title('Compressed Image')
plt.imshow(compressed_img)
plt.axis('off')
plt.show()