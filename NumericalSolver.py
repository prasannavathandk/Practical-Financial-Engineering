import Helper as hp
from IModel import ModelInterface
from abc import ABC, abstractmethod
import multiprocessing

class EulerScheme(ABC):

    def __init__(self, model) -> None:
        if(isinstance(model, ModelInterface)):
            self._model = model
        else:
            raise TypeError()  

    @property 
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if(isinstance(value, ModelInterface)):
            self._model = value
        else:
            raise TypeError()                 

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
        drift = self.model.drift()
        n = 10
        N = hp.stdNormal(num=n)
        return drift        
    
    #Summary from the sample paths
    def processSP(self):
        print("SamplePath.processSP")
        print(len(self.result))
        print(self.result)

    def execute(self):
        self.log_results(self.generateSP())
        self.processSP()   
