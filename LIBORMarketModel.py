from abc import abstractmethod
from IModel import ModelInterface
from NumericalSolver import EulerScheme
import multiprocessing
import subprocess
import sys
import Helper as hp

class LIBORModel(ModelInterface):

    def __init__(self, maturity, iter = 10, grid = 2, type = 0) -> None:
        self._it = iter
        self._gr = grid
        self.type = type
        self._mg = maturity
        self._tg = hp.discretize(self._mg, self._gr)
        print(self._tg)

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
        print("SamplePath.drift")
        if self.type == 1:
            return self.martingaleDrift
        else:
            return self.genDrift
        
        