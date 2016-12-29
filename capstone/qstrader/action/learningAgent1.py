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

    def __init__(self, ticker, signals=None, lastAction=None) :
        self.signals = signals
        self.ticker = ticker
        self.lastAction = lastAction

    def getStateString(self):

        print "Inside learningAgent1:getStateString()"
        returnStr = self.ticker + ":"
        for key, value in self.signals.iteritems():
            returnStr += "'" + str(key) + ":" + str(value.action)
        returnStr += "--" + self.lastAction
        return returnStr


class Action():

    def __init__(self, context ,instanceDict ):

        self.totalRewards = 0
        self.context = context
        self.state = None

        alpha = context['alpha']
        gamma = context['gamma']
        epsilon = context['epsilon']

        self.qTable = QTable(alpha=alpha, gamma=gamma, epsilon=epsilon)
        self.learning_indictors = None
        self.indicator_dict = None

    def reset(self, destination=None):
        print "Inside reset"


    def getTotalRewards(self):
        return self.totalRewards

    def act(self,event, action,reward_indicators, indicator_dict):

        # As of now, only one reward indicator can be passed.
        value = indicator_dict[reward_indicators[0]].getSignal(event.ticker)
        print "% changed value:", value

        ## Since, I am passing weekly performance/value change as reward indicator
        ## the change is not expected to be more than 10%. However, if I start using monthlty or Qty reward indicator
        ## the value likely to be higher. In that case, we need to normalize.  The idea here is tha
        ## if you get 10% up in a week, the reward given is maximum -which is 1

        if value > 10:
            return 1
        elif value > 5 :
            return 0.5
        elif value > 2 :
            return 0.2
        else :
            return 0.1



    def update(self, event,  learning_indictors, reward_indicators,indicator_dict, portfolio):

        print "Inside learningAgent1:Action:Update:", event, indicator_dict

        signals = dict()
        for ln in learning_indictors :
            signals[ln] = indicator_dict[ln].getSignal(event.ticker)

        # Update state from env. In this case, backtest/replay will call the update function
        tempState = State(event.ticker, signals,"NONE")
        print "current STATE:", tempState.getStateString()

        # Select action according to your policy
        action = self.qTable.chooseAction(tempState)

        # Execute action and get reward
        reward = self.act(event, action, reward_indicators, indicator_dict)

        try:
            print " Action ", action
            print " Reward for action ", reward
            if DEBUG:
                input("")

        except SyntaxError:
            pass

        newstate = State(event.ticker,signals,action)

        # Learn policy based on state, action, reward
        self.qTable.updateQTable1(self.state,
                                  action=action,
                                  reward=reward,
                                  newstate=newstate)
        self.state = newstate
        self.totalRewards += reward

        return action


    def __init_qTable(self):
        self.qTable = {}


class QTable():

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
        return ['BOT', 'SLD']


    def getStateAction(self, state=None, action=None):
        if state != None :
            return "{}=>{}".format(str(state.getStateString()), str(action))
        else :
            return "{}=>{}"

    def getQValue(self,state,action):

        if self.getStateAction(state, action=action) not in self._table :
            self._table[self.getStateAction(state,action=action)] = 0.0

        return self._table[self.getStateAction(state,action=action)]

    def setQValue(self, state, action=None, new_value=0.0):
        self._table[self.getStateAction(state,action=action)] = new_value


    def getMaxQValue(self, state):

        values = []
        for action in self.getLegalActions() :
            values.append(self.getQValue(state,action=action))

        return max(values)


    def chooseAction(self, state):
        print "\n"
        if True or random.random() < self._epsilon:
            legalActions = self.getLegalActions()
            bestAction = random.choice(legalActions)
            print " Going for random action :", bestAction
            return bestAction
        else:

            maxQ = 0.0
            bestAction = "NONE"
            for action in self.getLegalActions() :
                    q =  self.getQValue(state,action=action)
                    if q >= maxQ :
                        bestAction = action
                        maxQ = q
                    print " Going for best action for the state:", state.getStateString() , "=>", action,"\t\t",  q, ":", \
                        maxQ


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

        print " QTable  : "
        print json.dumps(self._table, indent=4)


if __name__ == "__main__":

    stgpath = getPath('strategies.data.path')
    config = settings.from_file(getqQstraderConfig())
    strategiesDict = dict()
    instancesDict = dict()

    print "STG:",stgpath

    indicators = json.load(open(stgpath + "indicators.dict"))
    for indicator, value in indicators.iteritems():
        print indicator, value

    strategies = json.load(open(stgpath + "strategy.dict"))
    for the_key, the_value in strategies.iteritems():
        strategiesDict[the_key] = the_value

    instances = json.load(open(stgpath + "instance.dict"))

    agentList = list()

    for instance, instanceDict in instances.iteritems():

        print "-------------------------Instance :",instance
        status = instanceDict["status"]
        if  status != "D" :
            ticketWeights = instanceDict["tickerWeights"]
            strategy = instanceDict["strategy"]
            benchmark = instanceDict["benchmark"]
            equity = instanceDict["equity"]

            start_date = instanceDict["startDate"]
            end_date = instanceDict["endDate"]
            strategy = instanceDict["strategy"]

            start_date = parser.parse(start_date)
            end_date = parser.parse(end_date)

            env = Environment(ticketWeights, start_date, end_date)

            agent = AgentFactory(env, config, indicators,strategiesDict.get(strategy), instanceDict)

            print agent
            agentList.append(agent)


    ## Simulate smarttrader.simulator.backtest

    from environment.event import *
    import smarttrader.indicators.TopoSort as topoSort
    eventList = list()

    for i in range(10) :
        barEvent = BarEvent("GOOG", "12.00", 100, 50, 56, 45, 55, 1111, 55)
        eventList.append(barEvent)

    for agent in agentList :

        while i in range (100) :

            event = eventList[i]
            if event.type == EventType.TICK or event.type == EventType.BAR:

                graph = dict()
                indicatorPath = getPath('strategies.data.path')
                indicators = json.load(open(indicatorPath + "indicators.dict"))
                for indicator, value in indicators.iteritems():
                    dependencies = value['dependencies']
                    graph[indicator] = dependencies

                order = topoSort.topological(graph)
                while True:
                    try:
                        ind = order.pop()
                        print (agent.indicator_dict)
                        indClass = agent.indicator_dict[ind]
                        indClass.updateIndicators(event, agent)
                    except IndexError:
                        break

            print "Portfolio:",agent.portfolio_handler.portfolio.init_cash
            agent.getLearningHandler().update(event,agent.indicator_dict,agent.portfolio_handler.portfolio)
            agent.portfolio_handler.portfolio._update_portfolio()