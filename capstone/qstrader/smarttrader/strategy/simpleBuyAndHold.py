from environment.event import (SignalEvent, EventType)

from .base import AbstractStrategy


class Strategy(AbstractStrategy):
    """
    A testing strategy that simply purchases (longs) a set of
    assets upon first receipt of the relevant bar event and
    then holds until the completion of a backtest.
    """
    def __init__(self, tickers, events_queue):

        self.tickers = tickers
        self.events_queue = events_queue
        self.ticks = 0
        self.invested = False
        self.learning_indictors = list()

    def calculate_signals(self, event,agent=None):

        if event.type in [EventType.BAR, EventType.TICK] and event.ticker in self.tickers:

            if event.ticker not in agent.portfolio_handler.portfolio.positions:

                signal = SignalEvent(event.ticker, "BOT")
                self.events_queue.put(signal)
                self.invested = True
                self.ticks += 1
