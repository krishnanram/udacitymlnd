import json
import random
import pandas
import numpy
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

#https://github.com/studywolf/blog/blob/master/RL/SARSA%20vs%20Qlearn%20cliff/qlearn.py

class LearningAgentQTable():

    def __init__(self, alpha, gamma, epsilon):

        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon
        self._table = {}

    def getAlpha(self):
        return self._alpha

    def getGamma(self):
        return self._gamma

    def getLegalActions(self):
        """
        returns the legal action from the current state
        """
        return ['forward', 'left', 'right', None]

    def getNextWayPoint(self, light, next_waypoint):
        return self._table['light'][light]['next_waypoint'][next_waypoint]

    def getStateAction(self, state=None, action=None):
        return "{}=>{}".format(str(state), str(action))


    def getQValue(self,state,action):

        if self.getStateAction(state, action=action) not in self._table :
            self._table[self.getStateAction(state,action=action)] = 0.0

        return self._table[self.getStateAction(state,action=action)]

    def setQValue(self, state, action=None, new_value=0.0):
        self._table[self.getStateAction(state,action=action)] = new_value


    def getMaxQValue(self, state):

        values = []
        for action in ['forward', 'left', 'right', None]:
            values.append(self.getQValue(state,action=action))

        return max(values)


    def chooseAction(self, state, nextwaypoint):

        print "\n"
        if random.random() < self._epsilon:
            legalActions = self.getLegalActions()
            bestAction = random.choice(legalActions)
            print " Going for random action :", bestAction
            return bestAction

        else:

            maxQ = 0.0
            bestAction = nextwaypoint
            for action in ['forward', 'left', 'right',None]:
                    q =  self.getQValue(state,action=action)
                    if q >= maxQ :
                        bestAction = action
                        maxQ = q
                    print " Going for best action for the state:", state, "=>", action,"\t\t",  q, ":", maxQ


            if maxQ == 0.0  :
                legalActions = self.getLegalActions()
                bestAction = random.choice(legalActions)
                print " No prev state-action found. Going for random action for the state:", bestAction

            else :
                print " ++++++++++++++++++++ Self Learned action for the state:", bestAction, "having Q:", maxQ

            return bestAction



    def updateQTable1(self,state,action,reward,newstate):

        oldQvalue = self.getQValue(state,action=action)

        maxValue = self.getMaxQValue(state)

        newQvalue = oldQvalue  + self._alpha * ( (reward + self._gamma * maxValue) - oldQvalue)

        self.setQValue(state,action=action,new_value=newQvalue)

        print " QTable  : ", "signal :left : oncoming : next_waypoint :action"

        print json.dumps(self._table, indent=4)


