import json
import random
import pandas
import numpy
import os
from collections import OrderedDict

class RunTimeStat(object):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self,learningAgentType, n_trials,
                              alpha, gamma,epsilon):

        self.learningAgentType = learningAgentType
        self.n_trials = n_trials
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.key = self.learningAgentType + ", alpha " + str(self.alpha) + ", gamma " + str(self.gamma) + ", epsilon " + str(self.epsilon)
        self.totalActions = 0.0
        self.totalRewards = 0.0
        self.currentTrial = 0
        self.trialHashMap = OrderedDict()


    def getTrialStat(self, trial):
        return self.trialHashMap.get(trial);

    def getStat(self):
        return self.trialHashMap

    def setTrial(self, trial):
        self.currentTrial = trial


    def setTotalRewards(self, stat):
        self.trialHashMap[self.key+', trial '+ str( self.currentTrial)] = stat


