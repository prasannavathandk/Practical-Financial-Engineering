import numpy as np
import pandas as pd
import multiprocessing
from Parameters import Parameters
from BM import BrownianMotion
import SpotMeasure as SM
import ForwardMeasure as FM
from NumericalSolver import SolutionScheme, Solver
import Helper as hp

class LIBORSim(SolutionScheme):

    def __init__(self, maturity, prices, volatility: np.array, scale = Parameters.tradingDays, measure=0, type=0, iter = 10):
        if(measure == 1):
            model=FM.ForwardMeasure(type = type, maturity=maturity, prices=prices, scale=scale)
        else:    
            model=SM.SpotMeasure(type = type, maturity=maturity, prices=prices, scale=scale)
        super().__init__(model=model, iter=iter)
        model.volatility = np.array(volatility).reshape(len(model.maturityGrid)-1, len(model.maturityGrid)-1)
        self._sm = np.zeros((self.iter, len(model.timeGrid), len(model.maturityGrid)-1)) #depth=iteration, column=discretizedTime, row=maturity
        self._ran = model.distribution()(self._sm.shape)
        self.epoch = 0
        print("Pre-Processing done!") 

    @property 
    def matrix(self):
        return self._sm

    @matrix.setter
    def matrix(self, value):
        self._sm = value  

    @property 
    def random(self):
        return self._ran

    @random.setter
    def random(self, value):
        self._ran = value  
         
    def popMatrix(self, result):
        self.matrix[result[0]] = result[1] 

    def subEngine(self, iter):
        print("Processing iteration:", self.epoch*Parameters.batch(multiprocessing.cpu_count()) + iter + 1)
        return (iter, [Solver.SamplePath(iter=iter, ti=ti, SDE=self.model.SDE, forwardCurve=self.matrix[iter,ti-1], random=self.random[iter,ti], matrix=self.matrix[iter,ti]) for ti in range(self.matrix.shape[1])])
    
    def engine(self):
        if Solver.parallel is not True:
           for i in range(self.matrix.shape[0]):
                print("Processing iteration:", i+1)
                for j in range(self.matrix.shape[1]):
                    Solver.SamplePath(iter=i, ti=j, SDE=self.model.SDE, random=self.random[i,j], matrix=self.matrix[i,j])
        else:
            asyncRes = [Solver.threadPool.apply_async(func = self.subEngine, args=(iter,), callback = self.popMatrix) for iter in range(self.matrix.shape[0])]
            for ares in asyncRes:
                ares.wait()    
        return  
    
    def simulate(self, epoch = 0):
        print(self.matrix.shape)
        self.epoch = epoch
        self.matrix[:,0,:] = hp.initCondition(self.model.bondPrices, self.model.maturityGrid).flatten() #[self.initCondition(T) for T in range(len(self.model.maturityGrid)-1)]
        self.execute()
        print("Processing done!") 
        return self

     #Summary from the sample paths
    def analyze(self, epoch = 0):
        self.epoch = epoch
        matrix = np.reshape(self.matrix, (-1, self.matrix.shape[-1]))
        tuples = [(i, j) for j in self.model.timeGrid for i in range(1, self.iter + 1)]
        index = pd.MultiIndex.from_tuples(tuples, names=['iteration', 'time'])
        df = pd.DataFrame(matrix, columns=self.model.maturityGrid[:-1], index=index.sortlevel(level='iteration')[0])
        print("Post-Processing done!")
        return df