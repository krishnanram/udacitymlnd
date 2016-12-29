from abc import ABCMeta, abstractmethod


class AbstractCompliance(object):


    __metaclass__ = ABCMeta

    @abstractmethod
    def record_trade(self, fill):

        raise NotImplementedError("Should implement record_trade()")
