import json

from agents.AgentFactory import AgentFactory
from common.PropertyReader import *
from dateutil import parser
from qstrader.environment.environment import Environment
from smarttrader.simulator.backtest import Backtest

if __name__ == "__main__":

    stgpath = getPath('strategies.data.path')
    config = settings.from_file(getqQstraderConfig())
    strategiesDict = dict()
    instancesDict = dict()

    print "STG:",stgpath

    strategies = json.load(open(stgpath + "strategy.dict"))

    for the_key, the_value in strategies.iteritems():
        strategiesDict[the_key] = the_value


    instances = json.load(open(stgpath + "instance.dict"))


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

            agent = AgentFactory(env, config, strategiesDict.get(strategy), instanceDict)
            print instance,agent

            backtest = Backtest(agent)

            results = backtest.simulate_trading(filename="../data/results/"+instance.replace(".","_")+"_"+strategy.replace(".","_"),testing=False)

        print "----------End---------------"

