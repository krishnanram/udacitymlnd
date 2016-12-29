import importlib

import common as common
from dateutil import parser
from environment.environment import Agent as Agent
from common.compat import queue
from smarttrader.price_handler.price_parser import PriceParser
from smarttrader.price_handler.yahoo_daily_csv_bar import YahooDailyCsvBarPriceHandler
from smarttrader.strategy import Strategies

class AgentFactory(Agent):
    """An agent that learns to drive in the smartcab world."""


    def getLearningHandler(self) :
        return self.learningHandler

    def __init__(self, env, context, config, indicators, strategiesDict, instanceDict) :

        #testing, filename,
           #QQQ benchmark, ticker_weights, title_str, equity):


        super(AgentFactory, self).__init__(env)

        self.context = context

        ticketWeights = instanceDict["tickerWeights"]
        start_date = instanceDict["startDate"]
        end_date = instanceDict["endDate"]
        strategy = instanceDict["strategy"]
        benchmark = instanceDict["benchmark"]
        equity = instanceDict["equity"]

        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)

        print strategiesDict, start_date, end_date

        positionSizer   = strategiesDict['positionSizer']
        riskManager     = strategiesDict['riskManager']
        portfolioHandler =   strategiesDict['portfolioHandler']
        complianceHandler = strategiesDict['complianceHandler']
        executionHandler = strategiesDict['executionHandler']
        tearsheetStatistics = strategiesDict['tearsheetStatistics']
        displayStrategy = strategiesDict['displayStrategy']
        learningHandler = strategiesDict['learningHandler']
        strategyHandler = strategiesDict['strategyHandler']
        title = strategiesDict['title']

        tmpArray = learningHandler.split(".")
        learningClass = getattr(importlib.import_module("action." + tmpArray[0]), "Action")
        self.learningHandler = learningClass(self.context,instanceDict)

        self.totalActions = 0.0
        self.totalRewards = 0.0

        #self.config = settings.from_file(config, testing)
        self.tickers = [t for t in ticketWeights.keys()]

        # Set up variables needed for backtest
        self.events_queue = queue.Queue()

        self.csv_dir = config.CSV_DATA_DIR
        self.initial_equity = PriceParser.parse(equity)

        # Use Yahoo Daily Price Handler
        self.price_handler = YahooDailyCsvBarPriceHandler(
            self.csv_dir, self.events_queue, self.tickers,
            start_date=start_date, end_date=end_date
        )

        tmpArray=strategyHandler.split(".")
        # Use the monthly liquidate and rebalance strategy
        strategyClass = getattr(importlib.import_module("smarttrader.strategy."+tmpArray[0]), "Strategy")
        displayClass  = getattr(importlib.import_module("smarttrader.strategy.display"), displayStrategy)

        self.strategy = strategyClass(self.tickers, self.events_queue)
        strategy = Strategies(self.strategy, displayClass())

        # Use the liquidate and rebalance position sizer
        # with prespecified ticker weights
        tmpArray = positionSizer.split(".")
        rebalancingClass = getattr(importlib.import_module("smarttrader.position_sizer."+tmpArray[0]), tmpArray[1])
        self.position_sizer = rebalancingClass(ticketWeights)


        # Use an example Risk Manager
        tmpArray = riskManager.split(".")
        riskManagerClass = getattr(importlib.import_module("smarttrader.risk_manager."+tmpArray[0]), tmpArray[1])
        self.risk_manager = riskManagerClass()

        # Use the default Portfolio Handler
        tmpArray = portfolioHandler.split(".")
        portHandlerClass = getattr(importlib.import_module("smarttrader.portfolio."+tmpArray[0]), tmpArray[1])
        self.portfolio_handler = portHandlerClass(self.initial_equity, self.events_queue, self.price_handler,
          self.position_sizer, self.risk_manager)

        # Use the ExampleCompliance component
        tmpArray = complianceHandler.split(".")
        complianceClass = getattr(importlib.import_module("smarttrader.compliance."+tmpArray[0]), tmpArray[1])
        self.compliance = complianceClass(config)

        # Use a Indicator component
        self.indicator_list = list()
        self.indicator_dict = dict()
        for indicator, value in indicators.iteritems():
            print indicator, value
            tmpArray = value['indicator'].split(".")
            indicatorClass = getattr(importlib.import_module("smarttrader.indicators."+tmpArray[0]), tmpArray[1])
            instance = indicatorClass(self.tickers, self.events_queue,value)
            self.indicator_list.append(instance)
            self.indicator_dict[value['indicator']] = instance


        # Use a simulated IB Execution Handler
        tmpArray = executionHandler.split(".")
        execHandlerClass = getattr(importlib.import_module("smarttrader.execution_handler." + tmpArray[0]), tmpArray[1])
        self.execution_handler = execHandlerClass(self.events_queue, self.price_handler, self.compliance)


        # Use the default Statistics
        self.title = [title]
        tmpArray = tearsheetStatistics.split(".")
        statClass = getattr(importlib.import_module("smarttrader.statistics."+tmpArray[0]), tmpArray[1])
        self.statistics = statClass(config, self.portfolio_handler, self.title, benchmark)


  
