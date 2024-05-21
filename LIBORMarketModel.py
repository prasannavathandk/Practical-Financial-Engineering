from abc import abstractmethod
from IModel import ModelInterface
from NumericalSolver import EulerScheme
import multiprocessing
import subprocess
import sys
import Helper as hp
import numpy as np

class LIBORModel(ModelInterface):

    def __init__(self, maturity, prices, scale, type = 0) -> None:
        self.type = type
        self._mg = maturity
        self._bp = prices
        self._tg = hp.discretize(self._mg, scale)

    distribution = hp.stdNormal

    def drift(self):
        if self.type == 1:
            return self.martingaleDrift
        else:
            return self.genDrift
          
    def SDE(self, curVal, step, rv, index):         #SDE according to eulers scheme
        mu = self.drift()
        sigma = self.volatility()
        return curVal + sigma*curVal*step + curVal*np.sqrt(step)*np.dot(sigma, rv) 
    
    def choleskyFactor(self):
         pass 
    
    #Fixed discrete maturity times
    @property 
    def maturityGrid(self):
        return self._mg

    @maturityGrid.setter
    def maturityGrid(self, value):
        self._mg = value

    @property 
    def bondPrices(self):
        return self._bp

    @bondPrices.setter
    def bondPrices(self, value):
        self._bp = value    

     #Implementation of martingale discretization
    @abstractmethod
    def genDrift(self):
        pass

    #Implementation of martingale discretization
    @abstractmethod
    def martingaleDrift(self):
        pass
    

        
        