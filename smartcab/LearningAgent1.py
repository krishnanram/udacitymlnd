import json
import random
import pandas
import numpy
import os
import common as common
from environment import Agent as Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from LearningAgentQTable import LearningAgentQTable


class LearningAgent1(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent1, self).__init__(env)
        self.color = 'red'
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        self.qTable = LearningAgentQTable(alpha=0.5, gamma=0.3,epsilon=0.5)
        self.totalActions = 0.0
        self.totalRewards = 0.0

    def setQtable(self, alpha=0.5, gamma=0.3,epsilon=0.5):
        self.qTable = LearningAgentQTable(alpha=alpha, gamma=gamma,epsilon=epsilon)

    def reset(self, destination=None):
        self.planner.route_to(destination)

    def getTotalRewards(self):
        return self.totalRewards

    def update(self, t):

        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator

        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)



        try:
            print "\n\n ---------------------------Next event -----------------------------------"
            print " Car :", self.color
            print "     Received next waypoint  :", self.next_waypoint
            print "     Input deadline = {} ".format(deadline)  # [debug]
            print "             signal           :",  inputs['light']
            print "             oncoming traffic :",  inputs['oncoming']
            print "             left     traffic :",  inputs['left']
            print "             right    traffic :",  inputs['right']
            if common.DEBUG:
                input("")
        except SyntaxError:
            pass

        # Update state
        self.state = 'light:{},left:{},oncoming:{},next_waypoint:{}'.format(inputs['light'],
                inputs['left'],
                inputs['oncoming'],
                self.next_waypoint)

        # Select action according to your policy
        action = self.qTable.chooseAction(self.state,self.next_waypoint)

        # Execute action and get reward
        reward = self.env.act(self, action)


        try:
            print " Action ", action
            print " Reward for action ", reward
            if common.DEBUG:
                input("")
        except SyntaxError:
            pass

        newstate = 'light:{},left:{},oncoming:{},next_waypoint:{}'.format(inputs['light'],
                inputs['left'],
                inputs['oncoming'],
                action)

        # Learn policy based on state, action, reward
        self.qTable.updateQTable1(self.state,
                action=action,
                reward=reward,
                newstate=newstate)

        self.totalRewards += reward
        self.totalActions += 1.0

        #common.debuglog("LearningAgent1.update(): deadline = {}, inputs = {}, action = {}, reward = {}, next_waypoint = {}".format(deadline, inputs, action, reward, self.next_waypoint) )

    def __init_qTable(self):
        self.qTable = {}

  
