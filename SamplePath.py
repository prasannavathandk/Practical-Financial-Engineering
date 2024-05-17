from abc import ABC, abstractmethod
import multiprocessing
import subprocess
import sys
import Helper

class SamplePath(ABC):

    def __init__(self) -> None:
        _numThreads = multiprocessing.cpu_count()
        self.threadPool = multiprocessing.Pool(processes = _numThreads)
        print("Computing parallel with", _numThreads, "processes")
        
    #can be implemented using spot or forward measure
    @abstractmethod
    def genDrift(self):
        pass

    #Implementation of martingale discretization
    @abstractmethod
    def martingaleDrift(self):
        pass

    def drift(self):
        print("SpotMeasure.drift")
        if type == 1:
            return self.martingaleDrift()
        else:
            return self.genDrift()

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

    #Entry function for simulation
    def simulate(self):
        print("SamplePath.simulate")
        result = []
        for i in range(self.iter):
            result.append(self.threadPool.apply_async(func=self.generateSP))

    #Generate the number of sample paths
    def generateSP(self):
        print("SamplePath.generateSP")
        drift = self.drift()
        self.eulerScheme(drift)

    #eulers scheme to implement a simgle sample path for the SDE
    def eulerScheme(self, drift):
        print("SamplePath.eulerScheme")
        n = 10
        N = self.stdNormal(n)
    
    #Summary from the sample paths
    def processSP(self):
        print("SamplePath.processSP")
        pass
