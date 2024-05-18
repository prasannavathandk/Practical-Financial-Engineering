import Helper as hp
import multiprocessing

class NumericalEngine:

    def __init__(self, drift):
        self.drift = drift

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

    #Generate the number of sample paths
    def generateSP(self):
        print("SamplePath.generateSP")
        drift = self.drift()
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

    def start(self):
        self.log_results(self.generateSP())
        self.processSP()   
