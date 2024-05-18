from abc import ABC, abstractmethod

class ModelInterface(ABC):
    #can be implemented using spot or forward measure
    @abstractmethod
    def drift(self):
        pass    

    #can be determinstic
    @abstractmethod
    def volatility(self, type):
        pass

    #can be determinstic
    @abstractmethod
    def distribution(self, type):
        pass

    #can be determinstic
    @abstractmethod
    def SDE(self, curVal, mu, sigma, step, rv):
        pass

    #Discrtization of time component
    @property 
    def timeGrid(self): 
        return self._tg

    @timeGrid.setter
    def timeGrid(self, value):
        self._tg = value 
