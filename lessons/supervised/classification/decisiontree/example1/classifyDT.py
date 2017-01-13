from sklearn import tree
from time import time
from sklearn.metrics import accuracy_score

def classify(features_train, labels_train):
    
    ### your code goes here--should return a trained decision tree classifer

    clf = tree.DecisionTreeClassifier()
    clf.fit(features_train, labels_train)
    
    return clf
