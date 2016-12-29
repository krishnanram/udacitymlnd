from environment.event import (SignalEvent, EventType)

from smarttrader.strategy.base import AbstractStrategy


class Strategy(AbstractStrategy):

    def __init__(self, tickers, events_queue):

        self.tickers = tickers
        self.events_queue = events_queue
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, event,agent=None):

        print "Inside calculate_signals :", event.ticker, self.invested, self.ticks

        if event.type in [EventType.BAR, EventType.TICK] and event.ticker in self.tickers:

            print "Calling Learning : agent.update"

            actionTobePerformed = agent.getLearningHandler().update(event, agent.indicator_dict,  agent.portfolio_handler.portfolio)
            signal = SignalEvent(event.ticker, actionTobePerformed)

            if actionTobePerformed == "NONE":
                print " No action "

            elif actionTobePerformed == "BUY" :
                if event.ticker not in agent.portfolio_handler.portfolio.positions :
                    print "Buy Event recieved from learner. Ticker {} not in portfolio.  Adding position".format(event.ticker)
                    self.events_queue.put(signal)

            elif actionTobePerformed == "SELL" :
                print "Exit Event received from learner. Ticker {} in portfolio.  Removing position".format(event.ticker)
                if event.ticker  in agent.portfolio_handler.portfolio.positions:
                    self.events_queue.put(signal)

            self.ticks += 1
