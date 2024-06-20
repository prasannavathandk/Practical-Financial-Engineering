from abc import abstractmethod
from IModel import ModelInterface
from NumericalSolver import SolutionScheme
import multiprocessing
import subprocess
import sys
import Helper as hp
import numpy as np

from Parameters import Parameters

class LIBORModel(ModelInterface):

    def __init__(self, maturity, prices, type = 0) -> None:
        self.type = type
        self._mg = maturity
        self._bp = prices
        self._tg = hp.discretize(self._mg)
        self._dr = self.martingaleDrift if self.type == 1 else self.genDrift
        self._eta = [np.where(self.maturityGrid > t)[0] for t in self.timeGrid]
        self._n = [np.where(self.maturityGrid <= n)[0] for n in self.maturityGrid]
        self._f = [np.where(self.maturityGrid[:-1] > n)[0] for n in self.maturityGrid[:-1]]
        self._vol = Parameters.volatility

    def distribution(self):
        return hp.stdNormal

    def drift(self):
        return self._dr
          
    def _SDE(self, curVal, step, stdN, mu, sigma):         #SDE according to eulers scheme
        #print("LIBORModel._SDE", curVal, step, stdN, mu, sigma)
        return curVal + mu*curVal*step + curVal*np.sqrt(step)*np.dot(sigma, stdN) 
    
    def SDE(self, forwardCurve, ti, n, rv):
        #print("LIBORModel.SDE", forwardCurve, ti, n, rv)
        if(self.timeGrid[ti] > self.maturityGrid[n]):
            return None
        return self._SDE(forwardCurve[n], self.timeGrid[ti]-self.timeGrid[ti-1], rv, self.drift()(self.nu(ti-1, n), forwardCurve), self.sigma(ti))
    
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
         
    @property
    def volatility(self):
        return self._vol

    @volatility.setter
    def volatility(self, value):
        self._vol = value

    def sigma(self, t, maturity = False):
        return self.timeGrid[t]*(self.volatility/100) if maturity is False else self.maturityGrid[t]*(self.volatility/100)

    #Implementation of general drift
    @abstractmethod
    def genDrift(self):
        pass

    #Implementation of martingale drift
    @abstractmethod
    def martingaleDrift(self):
        pass
    

        
        