from ILIBOR import LIBORInterface
from Numerical import NumericalEngine
import multiprocessing
import subprocess
import sys
import Helper as hp

class SamplePath(LIBORInterface):

    def __init__(self, maturity, iter = 10, grid = 2, type = 0) -> None:
        self._it = iter
        self._gr = grid
        self.type = type
        self._mg = maturity
        self._tg = hp.discretize(self._mg, self._gr)
        print(self._tg)

    def drift(self):
        print("SamplePath.drift")
        if self.type == 1:
            return self.martingaleDrift
        else:
            return self.genDrift

    #Entry function for simulation
    def simulate(self):
        print("SamplePath.simulate")  
        """
         with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as tp:
            for i in range(self.iter):
                tp.apply_async(func=self.generateSP, callback=self.log_results) 
        """
        engine = NumericalEngine(self.drift())
        engine.start()
        