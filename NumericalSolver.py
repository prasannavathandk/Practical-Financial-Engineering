import Helper as hp
from IModel import ModelInterface
import multiprocessing
import numpy as np

class Solver:
    threadPool = None
    parallel = False

    #Generate one sample path
    def SamplePath(iter, ti, forwardCurve, eta, SDE, random, matrix):  
        #print("EulerScheme.SamplePath", iter)
        if(ti == 0):
            return matrix
        for n in range(matrix.shape[0]):
            matrix[n] = SDE(forwardCurve = forwardCurve, ti = ti, n = n, rv = random[n])
        #print(matrix)
        return matrix

    def setPool(tp):
        Solver.threadPool = tp

    def setParallelism(flag):
        Solver.parallel = flag    

class SolutionScheme:

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

    def join(self):
        for res in self.result:
            res.wait()
        self.result = [res.get() for res in self.result]    

    def engine(self):
        timeGrid = self.model.timeGrid
        n = len(timeGrid)
        sde = self.SDE
        if Solver.parallel is not True:
           for i in range(self.iter):
                value = np.zeros(n) 
                N = np.random.normal(0, 1, n) 
                self.result.append(Solver.SamplePath(count=i, SDE=sde, timeGrid=timeGrid, random=N, matrix=value))
        else:   
            for i in range(self.iter):
                value = np.zeros(n) 
                N = np.random.normal(0, 1, n) 
                res = Solver.threadPool.apply_async(func=Solver.SamplePath, args=(i, sde, timeGrid, N, value,))
                self.log_results(res)
            self.join()        
        return        
           
    def execute(self):
        self.engine()
        return self.result