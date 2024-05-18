import Helper as hp
from IModel import ModelInterface
import multiprocessing
import numpy as np

class EulerScheme:

    def __init__(self, model, iter) -> None:
        if(isinstance(model, ModelInterface)):
            self._model = model
        else:
            raise TypeError()  
        self._it = iter
        self._sde = model.SDE
        self._dist = model.distribution

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

    @property
    def distribution(self):
        return self._dist
    
    @distribution.setter
    def distribution(self, value):
        self._dist = value

    @property
    def SDE(self):
        return self._sde
    
    @SDE.setter
    def SDE(self, value):
        self._sde = value        

    #Number of grid discritization
    @property
    def grid(self):
        return self._gr
    
    @grid.setter
    def grid(self, value):
        self._gr = value

    result = []         #change data type
    def log_results(self, res):
        self.result.append(res)

    #Generate the number of sample paths
    def SamplePath(self):
        timeGrid = self.model.timeGrid
        n = len(timeGrid)
        value = np.zeros(n)
        N = self.distribution(n)
        #avoid loop and implement cholesky factorization?        
        for i in range(n-1):
            value[i+1] = self.SDE(curVal=value[i], step=(timeGrid[i+1] - timeGrid[i]),rv = N[i+1], index = i+1)
        self.log_results(value)
               
    def engine(self):
        """
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as tp:
            for i in range(self.iter):
                tp.apply_async(func=self.SamplePath, callback=self.log_results) 
        """
        #Parallelize loop to speed up
        for i in range(self.iter):
            self.SamplePath()
           
    def execute(self):
        self.engine()
        return self.result