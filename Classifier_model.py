# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 05:57:08 2015
For: Xerox Innovation Contest
Author: Gaurav_Shrivastava
"""
import numpy as np
from sklearn import cross_validation
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold
import xgboost as xgb
#import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
import os
import pandas as pd
#os.chdir('C:\\Users\\Gaurav\\Desktop\\features')


#---------------------------Get_Performance-------------------------------------# 


def get_performance(y_est, y_test):
    #assert(y_est.shape == y_test.shape)
    m = len(list(y_test))
    #raw_input()
    print 'lol %d'%m
    count = 0
    tp, fp, tn, fn = 0, 0, 0, 0
    for i in range(m):
            if y_test[i] == 1 and y_est[i] == 1:
                tp += 1
            elif y_test[i] == 1 and y_est[i] == 0:
                fn += 1
            elif y_test[i] == 0 and y_est[i] == 1:
                fp += 1
            elif y_test[i] == 0 and y_est[i] == 0:
                tn += 1
    #if y_est[i][j] == y_test[i][j]:
    #count += 1
    #print float(count)/(m*n)
    return tp, fp, fn, tn
#--------------------------------------------------------------------------------#

#-------------------------------File_Inputs--------------------------------------#


labels = np.loadtxt('last20.csv')
# labels = pd.read_csv("last.csv")
# labels = pd.np.array(labels)
print labels.shape

#labels = to_dense(labels)
#print labels.shape
f = pd.read_csv('test_data/final/1/trainfinal.csv')
f= f.fillna(method = 'ffill')
f= f.fillna(method = 'bfill')
f= f.fillna(0)
features = pd.np.array(f)
print features.shape
# fpr = 0 
# tpr = 0
# mean_tpr = 0.0
# mean_fpr = np.linspace(0,1,100)
# k_fold = cross_validation.KFold(n=509105, n_folds=3, shuffle=False)

# sens = []
# spec = []
# acc = []
# i = 1
#allauc = []
#x = []
#x = [i for i in range(100000,509105)]
X = features
# X = features[100000:500000,:]
print X.shape
Y = labels
# Y = labels[100000:500000]
print X.shape


# scaler = StandardScaler()
# scaler.fit(X)  
# X = scaler.transform(X)

# pca = PCA(n_components=75)
# pca.fit(X)
# X = pca.transform(X)


#clf = RandomForestClassifier(n_estimators=100,n_jobs=-1)
#clf = LogisticRegression()
##clf = SVC(kernel= 'linear')
#clf.fit(X,Y)
#os.chdir('C:\\Users\\Gaurav\\Desktop')

dtrain = xgb.DMatrix(X,Y)

# test_data/features_final_test.csv
Test = pd.read_csv('test_data/final/1/testfinal.csv')
# tlabels = np.loadtxt('VLabel/Vlast10.csv')
Test =  Test.fillna(method = 'ffill')
Test =  Test.fillna(method = 'bfill')
Test =  Test.fillna(0)

test = pd.np.array(Test)
# test = features[1:100000,:]
# dtlabel = labels[1:100000]
##test = scaler.transform(test)

#test = pca.transform(test)
# ,tlabels
dtest = xgb.DMatrix(test)
param = {'bst:max_depth':6,'bst:eta':.3,'silent':0,'max_delta_step': 1 ,'objective':'binary:logistic' }
param['nthread'] = 6
plst = param.items()
# plst += [('eval_metric', 'auc')]
# evallist = [(dtest,'eval'), (dtrain, 'train') ]

num_rounds = 10
# , evallist, early_stopping_rounds =10
bst = xgb.train(plst, dtrain, num_rounds)
##label = clf.predict(test)
label = bst.predict(dtest)
label = pd.DataFrame(label)
label.to_csv('output_new_test.csv')
#--------------------------------------------------------------------------------#
