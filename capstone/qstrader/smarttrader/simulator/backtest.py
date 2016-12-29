from __future__ import print_function

from common.compat import queue
from environment.event import EventType
from common.PropertyReader import *
from dateutil import parser
import json
import smarttrader.indicators.TopoSort as topoSort

class Simulator(object):
    def __init__(self, env, size=None, frame_delay=10, update_delay=1.0):
        self.env = env
        self.quit = False
        for agent in self.env.agent_states:
            print
            agent.color


    def run(self, n_trials=1):
        self.quit = False
        for trial in xrange(n_trials):
            print
            "Simulator.run(): Trial {}".format(trial)  # [debug]


    def render(self):
        print
        "Inside render"


    def pause(self):
        print
        "Inside pause"




class Backtest(object):
    """
    Enscapsulates the settings and components for
    carrying out an event-driven backtest.
    """

    def __init__(self, agent, price_handler=None,
        strategy=None, portfolio_handler=None,
        execution_handler=None,
        position_sizer=None, risk_manager=None,
        statistics=None, equity=None)  :

        self.filename = None

        if agent != None :

            self.agent = agent
            self.price_handler = agent.price_handler
            self.strategy = agent.strategy
            self.portfolio_handler = agent.portfolio_handler
            self.execution_handler = agent.execution_handler
            self.position_sizer = agent.position_sizer
            self.risk_manager = agent.risk_manager
            self.statistics = agent.statistics
            self.equity = agent.initial_equity
            self.events_queue = agent.price_handler.events_queue
            self.cur_time = None
            self.indicator_list = agent.indicator_list
            self.indicator_dict = agent.indicator_dict

        else :

            self.price_handler = price_handler
            self.strategy = strategy
            self.portfolio_handler = portfolio_handler
            self.execution_handler = execution_handler
            self.position_sizer = position_sizer
            self.risk_manager = risk_manager
            self.statistics = statistics
            self.equity = equity
            self.events_queue = price_handler.events_queue
            self.cur_time = None

    def _run_backtest(self):
        """
        Carries out an infinite while loop that polls the
        events queue and directs each event to either the
        strategy component of the execution handler. The
        loop continue until the event queue has been
        emptied.
        """
        print("Running Backtest...")
        while self.price_handler.continue_backtest:
            try:
                event = self.events_queue.get(False)
            except queue.Empty:
                self.price_handler.stream_next()
            else:
                if event is not None:

                    print ("----------------- Price EVENT Received from market backtest----------------------")
                    if event.type == EventType.TICK or event.type == EventType.BAR:
                        self.cur_time = event.time

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
                                print (self.indicator_dict)
                                indClass = self.indicator_dict[ind]
                                indClass.updateIndicators(event, self.agent)

                            except IndexError:
                                break

                        print("        ***** Processing signals  ----------------------")
                        self.strategy.calculate_signals(event,self.agent)
                        print("        ***** Update portfolio  ----------------------")
                        self.portfolio_handler.update_portfolio_value()
                        print("        ***** Update Stats  ----------------------")
                        self.statistics.update(event.time, self.portfolio_handler)

                    elif event.type == EventType.SIGNAL:
                        self.portfolio_handler.on_signal(event)
                    elif event.type == EventType.ORDER:
                        self.execution_handler.execute_order(event)
                    elif event.type == EventType.FILL:
                        self.portfolio_handler.on_fill(event)
                    else:
                        raise NotImplemented("Unsupported event.type '%s'" % event.type)

                    print("POS after Price Event Processing :", self.agent.portfolio_handler.portfolio.positions)

        print ("Backtest completed. Positions at the End as follows....")
        print  ("Total rewards for this trial {} is {}".format(self.filename,self.agent.getLearningHandler().getTotalRewards()))

        print ("POS:", self.agent.portfolio_handler.portfolio.positions)


    def simulate_trading(self, filename=None,testing=False):
        """
        Simulates the backtest and outputs portfolio performance.
        """
        self.filename = filename
        self._run_backtest()
        results = self.statistics.get_results()

        print (results)
        print("---------------------------------")
        print("Backtest complete.")
        print("Sharpe Ratio: %s" % results["sharpe"])
        print("Max Drawdown: %s" % results["max_drawdown"])
        print("Max Drawdown Pct: %s" % results["max_drawdown_pct"])
        if not testing:
            self.statistics.plot_results(filename)
            print("Written the result in:",filename)
        return ""
