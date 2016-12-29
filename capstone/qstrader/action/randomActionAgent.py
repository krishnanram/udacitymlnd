import json
import random
from common.common import *
from agents.AgentFactory import AgentFactory
from common.PropertyReader import *
from dateutil import parser
from environment.environment import Environment
from smarttrader.simulator.backtest import Backtest
import random

class State() :

    def __init__(self) :
        print "Inside RandomActionAgenState"


class Action():

    def __init__(self, context,instanceDict ):
        self.state = State()

    def reset(self, destination=None):
        print "Inside reset"

    def getTotalRewards(self):
        return 0

    def getLegalActions(self):
        """
        returns the legal action from the current state
        """
        return ['BOT', 'SLD', 'NONE']

    def update(self, event,  learning_indictors, reward_indicators,indicator_dict, portfolio):

        print "Inside Random Action Agent:update", event, indicator_dict

        # Select action according to your policy
        action = random.choice(list(self.getLegalActions()))

        try:
            print " Action ", action
            if DEBUG:
                input("")

        except SyntaxError:
            pass


        return action


