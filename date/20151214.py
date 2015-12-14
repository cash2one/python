# coding:utf8
__author__ = '613108'

import zipfile
import pandas as pd
z=zipfile.ZipFile(r'd:\ml\train.zip')
df=pd.read_csv(z.open(z.namelist()[0]),header=0,delimiter='\t')

############################################################
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
import zipfile

z=zipfile.ZipFile(r'd:\ml\train.zip')
df=pd.read_csv(z.open(z.namelist()[0]),header=0,delimiter='\t')

pipeline=Pipeline([
    ('vect',TfidfVectorizer(stop_words='english')),
    ('clf',LogisticRegression())
])

parameters={
    'vect__max_df':(0.25,0.5),
    'vect__ngram_range':((1,1),(1,2)),
    'vect__use_idf':(True,False),
    'clf__C':(0.1,1,10),
}

X,y=df['Phrase'],df['Sentiment'].as_matrix()
X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.5)
grid_search=GridSearchCV(pipeline,parameters,n_jobs=2,verbose=1,scoring='accuracy')
grid_search.fit(X_train,y_train)

print('最佳效果：%0.3f' % grid_search.best_score_)
print('最优参数组合：')
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print('\t%s: %r' % (param_name, best_parameters[param_name]))

predictions=grid_search.predict(X_test)
print '准确率：',accuracy_score(y_test,predictions)
print '混淆矩阵：',confusion_matrix(y_test,predictions)
print '分类报告：',classification_report(y_test,predictions)