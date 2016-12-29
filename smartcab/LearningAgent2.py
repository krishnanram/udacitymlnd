import json
import random
import pandas
import numpy
import common as common
from environment import Agent as Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from LearningAgentQTable import LearningAgentQTable


class LearningAgent2(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent2, self).__init__(env)
        self.color = 'red'
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        self.qTable = LearningAgentQTable(alpha=0.5, gamma=0.3,epsilon=0.5)
        self.totalActions = 0.0
        self.totalRewards = 0.0

    def setQtable(self, alpha=0.5, gamma=0.3):
        self.qTable = LearningAgentQTable(alpha=alpha, gamma=gamma)

    def reset(self, destination=None):
        self.planner.route_to(destination)

    def update(self, t):

        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator

        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # Update state
        self.state = 'light: {}, left: {}, oncoming: {}, next_waypoint: {}'.format(inputs['light'],
                inputs['left'],
                inputs['oncoming'],
                self.next_waypoint)

        # Select action according to your policy
        action = self.qTable.chooseAction(light=inputs['light'],
                next_waypoint=self.next_waypoint,
                left=inputs['left'],
                oncoming=inputs['oncoming'])

        # Execute action and get reward
        reward = self.env.act(self, action)

        # Learn policy based on state, action, reward
        self.qTable.updateQTable2(light=inputs['light'],
                next_waypoint=self.next_waypoint,
                left=inputs['left'],
                oncoming=inputs['oncoming'],
                action=action,
                reward=reward)

        self.totalRewards += reward
        self.totalActions += 1.0

        print "LearningAgent2.update(): deadline = {}, inputs = {}, action = {}, reward = {}, next_waypoint = {}".format(deadline, inputs, action, reward, self.next_waypoint)  # [debug]

    def __init_qTable(self):
        self.qTable = {}
