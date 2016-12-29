import json

from agents.AgentFactory import AgentFactory
from common.PropertyReader import *
from dateutil import parser
from environment.environment import Environment
from smarttrader.simulator.backtest import Backtest
import common.settings

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

            alpha_params    = instanceDict["alpha_params"]
            gamma_params    = instanceDict["gamma_params"]
            epsilon_params  =  instanceDict["epsilon_params"]
            total_trials    = instanceDict["total_trials"]
            experiment = instanceDict["experiment"]

            print "Alpha params:", alpha_params
            print "Gamma params" , gamma_params
            print "Epsilon_params", epsilon_params
            print "Total trials", total_trials

            import shutil
            from shutil import copyfile

            start_date = parser.parse(start_date)
            end_date = parser.parse(end_date)

            env = Environment(ticketWeights, start_date, end_date)

            context = dict()
            for alpha in alpha_params :
                for gamma in gamma_params :
                    for epsilon in epsilon_params :
                        for trial in range(total_trials):

                            context['alpha']    = alpha
                            context['gamma']    =  gamma
                            context['epsilon'] = epsilon
                            agent = AgentFactory(env, context, config, indicators, strategiesDict.get(strategy), instanceDict)

                            print instance,agent
                            backtest = Backtest(agent)

                            print  str(alpha) + str(gamma) + str(epsilon)
                            resultsDir  = "../data/results/"+experiment+"/"+instance + "/"
                            filename = resultsDir + str(trial) + "_" + str(strategy) +"_" +  str(alpha).replace(".","") + '_' + str(gamma).replace(".","") + '_' + str(epsilon).replace(".","")

                            logsDir = "../data/logs/" + experiment + "/" + instance + "/"
                            logfileName = logsDir + str(trial) + "_"+ str(strategy) +"_" +  str(alpha).replace(".","") + '_' + str(gamma).replace(".","") + '_' + str(epsilon).replace(".","") + ".log"

                            if not os.path.exists(logsDir):
                                os.makedirs(logsDir)

                            if not os.path.exists(resultsDir):
                                os.makedirs(resultsDir)

                            print filename

                            results = backtest.simulate_trading(filename=filename,testing=False)

                            if os.path.isfile("out.log") :
                                shutil.copy("out.log", logfileName)
                            #shutil.move("out.log", logfileName)


        print "----------End---------------"

