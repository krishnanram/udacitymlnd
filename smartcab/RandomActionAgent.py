import json
import random
import pandas
import numpy
from environment import Agent as Agent, Environment
from planner import RoutePlanner
from simulator import Simulator



class RandomActionAgent(Agent):
    def __init__(self, env):
        super(RandomActionAgent, self).__init__(env)
        self.color = 'red'
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        self.totalActions = 0.0
        self.totalRewards = 0.0
        self.epsilon = 0.6

    def reset(self, destination=None):
        self.planner.route_to(destination)


    def getLegalActions(self):
        """
        returns the legal action from the current state
        """
        return ['forward', 'left', 'right', None]


    def flipCoin(self, p ):
        r = random.random()
        return r < p


    def update(self, t):

        print "RandomActionAgent : Update CALLED ********************* "
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator

        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # Update state
        self.state = 'light: {}, left: {}, oncoming: {}, next_waypoint: {}'.format(inputs['light'],
                                                                                   inputs['left'],
                                                                                   inputs['oncoming'],
                                                                                   self.next_waypoint)

        legalActions = self.getLegalActions()
        action = None

        if (self.flipCoin(self.epsilon)):
            print "random choice"
            action = random.choice(legalActions)

        # Execute action and get reward
        reward = self.env.act(self, action)

        self.totalRewards += reward
        self.totalActions += 1.0

        print "RandomActionAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, next_waypoint = {}".format(
            deadline, inputs, action, reward, self.next_waypoint)

