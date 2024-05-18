from abc import abstractmethod
from IModel import ModelInterface
from NumericalSolver import EulerScheme
import multiprocessing
import subprocess
import sys
import Helper as hp
import numpy as np

class LIBORModel(ModelInterface):

    def __init__(self, maturity, scale, type = 0) -> None:
        self.type = type
        self._mg = maturity
        self._tg = hp.discretize(self._mg, scale)

    distribution = hp.stdNormal
        
    def SDE(self, curVal, step, rv, index):         #SDE according to eulers scheme
        return 0
    
    #Implementation of martingale discretization
    @abstractmethod
    def genDrift(self):
        pass

    #Implementation of martingale discretization
    @abstractmethod
    def martingaleDrift(self):
        pass

    #Fixed discrete maturity times
    @property 
    def maturityGrid(self):
        return self._mg

    @maturityGrid.setter
    def maturityGrid(self, value):
        self._mg = value

    def drift(self):
        if self.type == 1:
            return self.martingaleDrift
        else:
            return self.genDrift

        
        