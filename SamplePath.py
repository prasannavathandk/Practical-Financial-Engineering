from abc import ABC, abstractmethod
import Helper

class SamplePath(ABC):

    #can be implemented using spot or forward measure
    @abstractmethod
    def drift(self):
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

    #Number of sample paths
    @property
    def iter(self):
        return self._it
    
    @iter.setter
    def iter(self, value):
        self._it = value

    #Entry function for simulation
    @abstractmethod
    def simulate(self, type):
        print("SamplePath.simulate")
        if type == 0:
            return self.generateSP
        elif type == 1:
            return self.generateSPmartingale

    #Generate the number of sample paths
    def generateSP(self):
        print("SamplePath.generateSP")
        for i in range(iter):
            drift = self.drift()
            self.eulerScheme(drift)
    
    def generateSPmartingale(self):
        print("SamplePath.generateSPmartingale")
        for i in range(iter):
            drift = self.martingaleDrift()
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
