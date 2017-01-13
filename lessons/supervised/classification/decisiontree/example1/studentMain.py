#!/usr/bin/python

""" lecture and example code for decision tree unit """

import sys
from class_vis import prettyPicture, output_image
from prep_terrain_data import makeTerrainData
from time import time

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from classifyDT import classify

def submitAccuracies():
  return {"acc":round(acc,3)}


features_train, labels_train, features_test, labels_test = makeTerrainData()

### the classify() function in classifyDT is where the magic
### happens--fill in this function in the file 'classifyDT.py'!
t0 = time()
clf = classify(features_train, labels_train)
print "training time: ", round(time()-t0, 3), "s"

t1 = time()
pred = clf.predict(features_test)
print "predicting time: ", round(time()-t1, 3), "s"

score = clf.score(features_test, labels_test)
print "Score:", score
#### grader code, do not modify below this line

prettyPicture(clf, features_test, labels_test)
output_image("test.png", "png", open("test.png", "rb").read())

