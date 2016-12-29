import datetime

from environment.environment import Agent as Agent
from action import LearningAgentQTable
from qstrader.common.compat import queue
from smarttrader.compliance import ExampleCompliance
from smarttrader.execution_handler.ib_simulated import IBSimulatedExecutionHandler
from smarttrader.portfolio.portfolio_handler import PortfolioHandler
from smarttrader.position_sizer.rebalance import LiquidateRebalancePositionSizer
from smarttrader.price_handler.price_parser import PriceParser
from smarttrader.price_handler.yahoo_daily_csv_bar import YahooDailyCsvBarPriceHandler
from smarttrader.risk_manager.example import ExampleRiskManager
from smarttrader.statistics import TearsheetStatistics
from smarttrader.strategy import Strategies, DisplayStrategy
from smarttrader.strategy.buy_and_hold import BuyAndHoldStrategy


class AgentFactory(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, config, strategyDict, instanceDict):

        print instanceDict
        ticketWeights = instanceDict["tickerWeights"]
        start_date = instanceDict["startDate"]
        end_date = instanceDict["endDate"]
        strategy = instanceDict["strategy"]
        benchmark = instanceDict["benchmark"]
        equity = instanceDict["equity"]

        start_date = datetime.datetime(2007, 12, 4)
        end_date = datetime.datetime(2016, 10, 12)

        self.color = 'red'
        self.qTable = LearningAgentQTable(alpha=0.5, gamma=0.3, epsilon=0.5)
        self.totalActions = 0.0
        self.totalRewards = 0.0

        # self.config = settings.from_file(config, testing)
        self.tickers = [t for t in ticketWeights.keys()]

        # Set up variables needed for backtest
        self.events_queue = queue.Queue()

        self.csv_dir = config.CSV_DATA_DIR
        self.initial_equity = PriceParser.parse(500000.00)

        # Use Yahoo Daily Price Handler
        self.price_handler = YahooDailyCsvBarPriceHandler(
            self.csv_dir, self.events_queue, self.tickers,
            start_date=start_date, end_date=end_date
        )

        # Use the monthly liquidate and rebalance strategy

        self.strategy = BuyAndHoldStrategy(self.tickers, self.events_queue)
        strategy = Strategies(self.strategy, DisplayStrategy())

        #strategyClass = getattr(importlib.import_module("qstrader.strategy.buy_and_hold"), "BuyAndHoldStrategy")
        #displayClass  = getattr(importlib.import_module("qstrader.strategy.display"), "DisplayStrategy")
        #strategy = strategyClass(self.strategy, displayClass())


        # Use the liquidate and rebalance position sizer
        # with prespecified ticker weights
        self.position_sizer = LiquidateRebalancePositionSizer(ticketWeights)
        #rebalancingClass = getattr(importlib.import_module("qstrader.position_sizer.rebalance"), "LiquidateRebalancePositionSizer")
        #strategy = rebalancingClass(ticketWeights)


        # Use an example Risk Manager
        self.risk_manager = ExampleRiskManager()
        #riskManagerClass = getattr(importlib.import_module("qstrader.risk_manager.example"), "ExampleRiskManager")
        #self.risk_manager = riskManagerClass()


        # Use the default Portfolio Handler
        self.portfolio_handler = PortfolioHandler(
            self.initial_equity, self.events_queue, self.price_handler,
            self.position_sizer, self.risk_manager
        )
        #portHandlerClass = getattr(importlib.import_module("qstrader.portfolio.portfolio_handler"), "PortfolioHandler")
        #strategy = portHandlerClass(self.initial_equity, self.events_queue, self.price_handler,
         #   self.position_sizer, self.risk_manager)


        # Use the ExampleCompliance component
        self.compliance = ExampleCompliance(config)
        #complianceClass = getattr(importlib.import_module("qstrader.compliance.example"), "ExampleCompliance")
        #self.compliance = complianceClass(config)

        # Use a simulated IB Execution Handler
        self.execution_handler = IBSimulatedExecutionHandler(
            self.events_queue, self.price_handler, self.compliance
        )
        #execHandlerClass = getattr(importlib.import_module("qstrader.execution_handler.ib_simulated"), "IBSimulatedExecutionHandler")
        #self.execution_handler = execHandlerClass(self.events_queue, self.price_handler, self.compliance)


        # Use the default Statistics
        self.title = [strategyDict.get('title')]
        self.statistics = TearsheetStatistics(
            config, self.portfolio_handler, self.title, benchmark
        )
        #statClass = getattr(importlib.import_module("qstrader.statistics.tearsheet"), "TearsheetStatistics")
        #strategy = statClass(config, self.portfolio_handler, self.title, benchmark)


if __name__ == "__main__":
  print "Hello"