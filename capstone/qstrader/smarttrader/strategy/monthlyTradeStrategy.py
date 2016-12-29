from environment.event import (SignalEvent, EventType)

from .base import AbstractStrategy


class Strategy(AbstractStrategy):
    """
    A testing strategy that alternates between buying and selling
    a ticker on every 5th tick. This has the effect of continuously
    "crossing the spread" and so will be loss-making strategy.

    It is used to test that the backtester/live trading system is
    behaving as expected.
    """
    def __init__(self, tickers, events_queue):
        self.tickers = tickers
        self.events_queue = events_queue
        self.ticks = 0
        self.invested = False
        self.learning_indictors = list()
        self.reward_indicators = list()

        self.learning_indictors.append("rsi_indicators.movingAverage")
        self.reward_indicators.append("rsi_indicators.RSICrossOver")
        self.learning_indictors.append("demark_indicators.TDSequential")
        self.reward_indicators.append("rsi_indicators.MonthlyValueChangeCalculator")


    def calculate_signals(self, event,agent=None):

            if event.type == EventType.BAR and event.ticker in self.tickers:
                # Add latest adjusted closing price to the
                # short and long window bars

                if self.ticks % 20 == 0:
                    print "Calling Learning : agent.update"

                    actionTobePerformed = agent.getLearningHandler().update(event,self.learning_indictors,self.reward_indicators, agent.indicator_dict, agent.portfolio_handler.portfolio)
                    signal = SignalEvent(event.ticker, actionTobePerformed)

                    if actionTobePerformed == "NONE":
                        print " No action "

                    elif actionTobePerformed == "BOT":
                        if event.ticker not in agent.portfolio_handler.portfolio.positions:
                            print "Buy Event recieved from learner. Ticker {} not in portfolio.  Adding position".format(
                                event.ticker)
                            self.events_queue.put(signal)

                    elif actionTobePerformed == "EXIT":
                        print "Exit Event received from learner. Ticker {} in portfolio.  Removing position".format(
                            event.ticker)
                        if event.ticker in agent.portfolio_handler.portfolio.positions:
                            self.events_queue.put(signal)


            self.ticks += 1
