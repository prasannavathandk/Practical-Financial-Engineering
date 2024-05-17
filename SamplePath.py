from abc import ABC, abstractmethod
import multiprocessing
import subprocess
import sys
import Helper as hp

class SamplePath(ABC):

    def __init__(self, maturity, iter = 10, grid = 2, type = 0) -> None:
        self._it = iter
        self._gr = grid
        self.type = type
        self._mg = maturity
        self._tg = hp.discretize(self._mg, self._gr)
        print(self._tg)

    #can be implemented using spot or forward measure
    @abstractmethod
    def genDrift(self):
        pass

    #Implementation of martingale discretization
    @abstractmethod
    def martingaleDrift(self):
        pass

    def drift(self):
        print("SamplePath.drift")
        if self.type == 1:
            return self.martingaleDrift
        else:
            return self.genDrift

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

    #Number of sample paths
    @property
    def iter(self):
        return self._it
    
    @iter.setter
    def iter(self, value):
        self._it = value

    #Number of grid discritization
    @property
    def grid(self):
        return self._gr
    
    @grid.setter
    def grid(self, value):
        self._gr = value

    result = []
    def log_results(self, res):
        self.result.append(res)

    #Entry function for simulation
    def simulate(self):
        print("SamplePath.simulate")  
        """
         with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as tp:
            for i in range(self.iter):
                tp.apply_async(func=self.generateSP, callback=self.log_results) 
        """

        self.log_results(self.generateSP())
        self.processSP()
    
    #Generate the number of sample paths
    def generateSP(self):
        print("SamplePath.generateSP")
        drift = self.drift()()
        return self.eulerScheme(drift)

    #eulers scheme to implement a simgle sample path for the SDE
    def eulerScheme(self, drift):
        print("SamplePath.eulerScheme")
        n = 10
        N = hp.stdNormal(num=n)
        return drift
    
    #Summary from the sample paths
    def processSP(self):
        print("SamplePath.processSP")
        print(len(self.result))
        print(self.result)
