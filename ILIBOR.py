from abc import ABC, abstractmethod

class LIBORInterface(ABC):
    #can be implemented using spot or forward measure
    @abstractmethod
    def genDrift(self):
        pass

    #Implementation of martingale discretization
    @abstractmethod
    def martingaleDrift(self):
        pass

    #can be determinstic
    @abstractmethod
    def volatility(self, type):
        pass

    #Fixed discrete maturity times
    @property 
    def maturityGrid(self):
        return self.__mg

    @maturityGrid.setter
    def maturityGrid(self, value):
        self._mg = value

    #Discrtization of time component
    @property 
    def timeGrid(self): 
        return self._tg

    @timeGrid.setter
    def timeGrid(self, value):
        self._tg = value
