# coding:utf8
__author__ = 'Administrator'
from sklearn.metrics import accuracy_score

y_pred, y_true = [0, 1, 1, 0], [1, 1, 1, 1]
print(accuracy_score(y_true, y_pred))

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split, cross_val_score

df = pd.read_csv('D:\ML\SMSSpamCollection.txt', delimiter='\t', header=None)
df.columns = ['temp', 'message']
df['label'] = df['temp'].apply(lambda x: 1 if x == 'ham' else 0)
df = df.drop(['temp'], axis=1)
X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['message'], df['label'])
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
scores = cross_val_score(classifier, X_train, y_train, cv=5)
print '准确率：', np.mean(scores), scores
precisions = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision')
print '精确率：', np.mean(precisions), precisions
recalls = cross_val_score(classifier, X_train, y_train, cv=5, scoring='recall')
print '召回率：', np.mean(recalls), recalls

X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['message']
                                                            , df['label'])
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
precisions = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision')
print('精确率：', np.mean(precisions), precisions)

############################################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.metrics import roc_curve, auc

df = pd.read_csv('D:\ML\SMSSpamCollection.txt', delimiter='\t', header=None)
df.columns = ['temp', 'message']
df['label'] = df['temp'].apply(lambda x: 1 if x == 'ham' else 0)
df = df.drop(['temp'], axis=1)
X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['message'], df['label'])
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)

classifier = LogisticRegression()
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

false_positive_rate, recall, thresholds = roc_curve(y_test, list(predictions))
roc_auc=auc(false_positive_rate,recall)

############################################################
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score,recall_score,accuracy_score

pipeline=Pipeline([
    ('vect',TfidfVectorizer(stop_words='english')),
    ('clf',LogisticRegression())
])

parameters={
    'vect__max_df':(0.25,0.5,0.75),
    'vect__stop_words':('english',None),
    'vect__max_features':(2500,5000,10000,None),
    'vect__ngram_range':((1,1),(1,2)),
    'vect__use_idf':(True,False),
    'vect__norm':('11','12'),
    'clf__penalty':('11','12'),
    'clf__C':(0.01,0.1,1,10),
}

grid_search=GridSearchCV(pipeline,parameters,n_jobs=-1,verbose=1,scoring='accuracy',cv=3)

df = pd.read_csv('D:\ML\SMSSpamCollection.txt', delimiter='\t', header=None)
df.columns = ['temp', 'message']
df['label'] = df['temp'].apply(lambda x: 1 if x == 'ham' else 0)
df = df.drop(['temp'], axis=1)

X,y,=df['message'],df['label']
X_train,X_test,y_train,y_test=train_test_split(X,y)
grid_search.fit(X_train,y_train)

print '最佳效果：%0.3f'%grid_search.best_score_
print '最优参数组合：'
for param_name in sorted(parameters.keys()):
    print '\t%s:%r'%(param_name,best_parameters[param_name])

predictions=grid_search.predict(X_test)
print '准确率：',accuracy_score(y_test,predictions)
print '精确率：',precision_score(y_test,predictions)
print '召回率：',recall_score(y_test,predictions)