import numpy as np
from sklearn.model_selection import  train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import pandas as pd
import pickle

clf = KNeighborsClassifier(n_neighbors=5)
clf1 = SVC(class_weight="balanced")
def training ():
    
    df=pd.read_csv('output1.csv')
    df.drop(['frames'],1,inplace=True)
    df.drop(['car_ID'],1, inplace=True)
    
    x=np.array(df.drop(['class'],1))
    y=np.array(df['class'])
      
    #knn
    clf.fit(x, y)
    filename = 'KNN_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    
    #svm
    clf1.fit(x, y)
    filename1 = 'svm_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    
#random_state=100,max_iter=1000,kernel='rbf',gamma='auto'
def testing_knn (text):
    
    df=pd.read_csv('output1.csv')
    df.drop(['frames'],1,inplace=True)
    df.drop(['car_ID'],1, inplace=True)
    
    x=np.array(df.drop(['class'],1))
    y=np.array(df['class'])
    
 
    accuracy_knn = clf.score(x, y)
  
    print('knn',accuracy_knn,clf.predict([text]))
    return clf.predict([text])
    
def testing_svm(text):    
    df=pd.read_csv('output1.csv')
    df.drop(['frames'],1,inplace=True)
    df.drop(['car_ID'],1, inplace=True)
    
    x=np.array(df.drop(['class'],1))
    y=np.array(df['class'])
  
    #knn
 
    accuracy_svm = clf1.score(x, y)
    
    print('svm',accuracy_svm,clf1.predict([text]))
    return clf1.predict([text])