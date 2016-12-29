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

    def __init__(self,action=None, crossover_signal1=None, crossover_signal2=None, position_change_per=0) :

        self.lastTickerAction                   = action
        self.crossover_signal1                 = crossover_signal1
        self.crossover_signal2                  = crossover_signal2
        self.position_change_per                = position_change_per

    def getStateString(self):
        returnStr = 'lastTickerAction{}' +  'crossover_signal1{}'  + 'crossover_signal2' + 'position_change_per'
        return returnStr.format(self.lastTickerAction, self.crossover_signal1, self.crossover_signal2, self.position_change_per)

    def toString(self):
        print "lastTickerAction"

class Action():

    def __init__(self, instanceDict ):

        self.state = State()
        self.totalRewards = 0
        alpha = 0.5
        gamma = 0.3
        epsilon = 0.5
        self.qTable = QTable(alpha=alpha, gamma=gamma, epsilon=epsilon)

    def reset(self, destination=None):
        print "Inside reset"


    def getTotalRewards(self):
        return self.totalRewards

    def act(self,action,portfolio):
        return random.choice(list([0.5, 0.8, 2, 1, 0.2, 0.7, 2, 3]))


    def update(self, event, learning_indictors, indicator_dict, portfolio):

        print "Inside Agent Update:", event, indicator_dict

        signals = list()
        for ln in learning_indictors :
            signals.append(indicator_dict[ln].getSignal())


        # Update state
        self.state.crossover_signal1           = crossover_signal1
        self.state.crossover_signal2           = crossover_signal2
        self.state.position_change_per   = position_change_per

        # Select action according to your policy
        action = self.qTable.chooseAction(self.state)

        print "current STATE:", self.state.getStateString()
        print "Queue:", portfolio.value_queue

        # Execute action and get reward
        reward = self.act(action,portfolio)

        try:
            print " Action ", action
            print " Reward for action ", reward
            if DEBUG:
                input("")

        except SyntaxError:
            pass

        newstate = State(action, crossover_signal1, crossover_signal2, position_change_per )


        # Learn policy based on state, action, reward
        self.qTable.updateQTable1(self.state,
                                  action=action,
                                  reward=reward,
                                  newstate=newstate)

        self.totalRewards += reward
        #self.totalActions += 1.0

        # common.debuglog("LearningAgent1.update(): deadline = {}, inputs = {}, action = {}, reward = {}, next_waypoint = {}".format(deadline, inputs, action, reward, self.next_waypoint) )

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
        return "{}=>{}".format(str(state), str(action))


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
                    print " Going for best action for the state:", state.getStateString() , "=>", action,"\t\t",  q, ":", maxQ


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