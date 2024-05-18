import Helper as hp
from IModel import ModelInterface
from abc import ABC, abstractmethod
import multiprocessing
import numpy as np

class EulerScheme(ABC):

    def __init__(self, model, iter) -> None:
        if(isinstance(model, ModelInterface)):
            self._model = model
        else:
            raise TypeError()  
        self._it = iter

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
        timeGrid = self.model.timeGrid
        sde = self.model.SDE
        n = len(timeGrid)
        value = np.zeros(n)
        N = self.model.randomness()(n)        
        for i in range(n-1):
            value[i+1] = sde(curVal=value[i], step=(timeGrid[i+1] - timeGrid[i]),rv = N[i+1], index = i+1)
        return value        
    
    #Summary from the sample paths
    def processSP(self):
        print("SamplePath.processSP")
        for res in self.result:
            print(res)
            hp.plotSP(res)
               
    def execute(self):
        for i in range(self.iter):
            self.log_results(self.generateSP())
        self.processSP()   
