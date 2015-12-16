# coding:utf8
__author__ = 'Administrator'

import mahotas as mh
import glob
import numpy as np
from mahotas.features import surf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import *
from sklearn.cluster import MiniBatchKMeans

all_instance_filenames = []
all_instance_targets = []

for f in glob.glob('d:/ML/cat_dog/*.jpg'):
    target = 1 if 'cat' in f else 0
    all_instance_filenames.append(f)
    all_instance_targets.append(target)

surf_features = []

counter = 0
for f in all_instance_filenames:
    print('reading image:', f)
    image = mh.imread(f, as_grey=True)
    surf_features.append(surf.surf(image)[:, 5:])

"""if MemoryError,use this to train;only once"""
"""
t1, t2 = all_instance_filenames[:len(all_instance_filenames) / 2], \
         all_instance_filenames[len(all_instance_filenames) / 2:]
t1, t2 = t1[:len(t1) / 2], t2[:len(t2) / 2]
all_instance_filenames = t1 + t2

T1, T2 = all_instance_targets[:len(all_instance_targets) / 2], \
         all_instance_targets[len(all_instance_targets) / 2:]
T1, T2 = T1[:len(T1) / 2], T2[:len(T2) / 2]
all_instance_targets = T1 + T2

S1, S2 = surf_features[:len(surf_features) / 2], surf_features[len(surf_features) / 2:]
S1, S2 = S1[:len(S1) / 2], S2[:len(S2) / 2]
surf_features = S1 + S2
"""
"""END"""

train_len = int(len(all_instance_filenames) * 0.6)
X_train_surf_features = np.concatenate(surf_features[:train_len])
x_test_surf_features = np.concatenate(surf_features[train_len:])
y_train = all_instance_targets[:train_len]
y_test = all_instance_targets[train_len:]

n_clusters = 300
"""n_clusters need to be 150"""

print 'Clustering', len(X_train_surf_features), 'features'
estimator = MiniBatchKMeans(n_clusters=n_clusters)
estimator.fit_transform(X_train_surf_features)

X_train = []
for instance in surf_features[:train_len]:
    clusters = estimator.predict(instance)
    features = np.bincount(clusters)
    if len(features) < n_clusters:
        features = np.append(features, np.zeros((1, n_clusters, len(features))))
    X_train.append(features)

X_test = []
for instance in surf_features[train_len:]:
    clusters = estimator.predict(instance)
    features = np.bincount(clusters)
    if len(features) < n_clusters:
        features = np.append(features, np.zeros((1, n_clusters, len(features))))
    X_test.append(features)

clf = LogisticRegression(C=0.001, penalty='l2')
clf.fit_transform(X_train, y_train)
predictions = clf.predict(X_test)
print(classification_report(y_test, predictions))
print('Precision: ', precision_score(y_test, predictions))
print('Recall: ', recall_score(y_test, predictions))
print('Accuracy: ', accuracy_score(y_test, predictions))