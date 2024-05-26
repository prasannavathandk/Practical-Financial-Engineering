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

    def distribution(self):
        return hp.stdNormal

    def drift(self):
        if self.type == 1:
            return self.martingaleDrift
        else:
            return self.genDrift
          
    def SDE(self, curVal, i1, i2, rv, row):         #SDE according to eulers scheme
        #print("SDE", curVal, i1, i2, rv, row)
        if(self.timeGrid[i2] > self.maturityGrid[row]):
            return None
        mu = self.drift()()
        sigma = self.volatility()
        #print(mu, sigma)
        return curVal + mu*curVal*(self.timeGrid[i2] - self.timeGrid[i1]) + curVal*np.sqrt((self.timeGrid[i2] - self.timeGrid[i1]))*np.dot(sigma, rv) 
    
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
    

        
        