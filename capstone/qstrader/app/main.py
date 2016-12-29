import argparse
import json
import os
import sys
from ast import literal_eval as make_tuple

import common as common
from agents.LearningAgent1 import LearningAgent1
from agents.LearningAgent2 import LearningAgent2
from agents.RandomActionAgent import RandomActionAgent
from common.RunTimeStat import  RunTimeStat
from environment.environment import Environment
from smarttrader.simulator.backtest import Simulator


def simulate(n_trials, update_delay, dummyAgents,start, destination, learningAgentType,alpha, gamma,epsilon,experiment):

    # Set up environment and agent
    e = Environment(dummyAgent=dummyAgents,start=start, destination = destination)  # create environment (also adds some dummy traffic)

    if learningAgentType == "RandomActionAgent" :
        print ""
        a = e.create_agent(RandomActionAgent)  # create agent

    elif learningAgentType == "LearningAgent1" :
        print ""
        a = e.create_agent(LearningAgent1)  # create agent
        a.setQtable(alpha=alpha, gamma=gamma,epsilon=epsilon)

    elif learningAgentType == "LearningAgent2" :
        print ""
        a = e.create_agent(LearningAgent2)  # create agent
        a.setQtable(alpha=alpha, gamma=gamma,epsilon=epsilon)

    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track
    runTimeStat = RunTimeStat(learningAgentType=learningAgentType,n_trials=n_trials,
                              alpha=alpha, gamma=gamma,epsilon=epsilon)
    e.setRunTimeStat(runTimeStat)

    # Now simulate it
    sim = Simulator(e, update_delay=update_delay)  # reduce update_delay to speed up simulation

    sim.run(n_trials=n_trials)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    runtimeStatFile = "logs/" + experiment + "runTimeStat.json"

    mergedRunTimeStat = dict()
    if os.path.isfile(runtimeStatFile):
        with open(runtimeStatFile) as f:
            oldRunTimeStat = json.load(f)
            mergedRunTimeStat = oldRunTimeStat.copy()

    runTimeStat = e.getRunTimeStat().getStat()
    print "---------------------"
    print "Runstat of current run"
    print json.dumps(runTimeStat)

    mergedRunTimeStat.update(runTimeStat)

    with open(runtimeStatFile, 'w') as f:
        json.dump(mergedRunTimeStat, f)

    #with open(runtimeStatFile) as f:
        #print json.load(f)

    print "GREAT"

if __name__ == '__main__':

    # simulate params
    # n_trials          --> No of trails
    # update_delay      --> Update delay
    # dummyAgents       --> No of Dummy Agents
    # start             --> Start position. If none, system will assign random position
    # destination       --> Destination position. If none, system will assign random position
    # learningAgentType --> RandomActionAgent or LearningAgent1 or LearningAgent2
    # alpha             --> Alpha value used in QTable update calculation
    # gamma             --> Gamma value used in QTable update calculation


    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    parser = argparse.ArgumentParser(description='This is a agent.py for smartcab')
    parser.add_argument('-d', '--debug',       help='pause step for debug', required=True)
    parser.add_argument('-x', '--experiment',   help='experiment', required=False)
    parser.add_argument('-y', '--agentType',   help='Agent type', required=False)
    parser.add_argument('-t', '--trials',      help='No of Trials', required=False)
    parser.add_argument('-a', '--alpha',       help='Alpha', required=False)
    parser.add_argument('-g', '--gamma',       help='Gamma', required=False)
    parser.add_argument('-e', '--epsilon',     help='Epsolon', required=False)
    parser.add_argument('-s', '--start',       help='start', required=False)
    parser.add_argument('-n', '--destination', help='destination', required=False)

    args = parser.parse_args()

    ## show values ##
    print ("Debug Pause : %s" % args.debug)
    print ("Agent Type  : %s" % args.agentType)

    if args.trials == None :
        args.trials = 10

    if args.agentType == None :
        args.agentType = "LearningAgent1"

    if args.alpha == None:
        args.alpha = 0.5

    if args.gamma == None:
        args.gamma = 0.5

    if args.epsilon == None:
        args.epsilon = 0.5


    if args.start == None:
        args.start = (1, 6)
    elif args.start == "random" :
        args.start = None

    if args.destination == None:
        args.destination = (4, 3)
    elif args.destination == "random" :
        args.destination = None

    experiment = args.experiment

    n_trials= int(args.trials)
    agentType = args.agentType

    dummyAgents = 1

    print args.destination

    if args.start != None :
        start = make_tuple(args.start)
    else :
        start = None

    if args.destination != None :
        destination = make_tuple(args.destination)
    else :
        destination = None

    alpha= float(args.alpha)
    gamma= float(args.gamma)
    epsilon= float(args.epsilon)

    print "Agent Type:", agentType
    print "Debug:", args.debug
    common.DEBUG=int(args.debug)

    ## support 'RandomActionAgent', 'LearningAgent1'

    print "*********************** Simulating  Agent ********************************"
    runtimeStat = simulate(n_trials=n_trials,
                 update_delay=0.005,
                 dummyAgents=dummyAgents,
                 start=start,
                 destination=destination,
                 learningAgentType=agentType,
                 alpha=alpha,
                 gamma=gamma,
                 epsilon=epsilon,
                experiment=experiment)




