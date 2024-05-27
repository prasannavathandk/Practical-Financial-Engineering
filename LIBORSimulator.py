import numpy as np
import pandas as pd
from BM import BrownianMotion
import SpotMeasure as SM
import ForwardMeasure as FM
from NumericalSolver import SolutionScheme, Solver
import Helper as hp

class LIBORSim(SolutionScheme):

    def __init__(self, maturity, prices, measure=0, type=0, iter = 10):
        if(measure == 1):
            model=FM.ForwardMeasure(type = type, maturity=maturity, prices=prices)
        else:    
            model=SM.SpotMeasure(type = type, maturity=maturity, prices=prices)
        super().__init__(model=model, iter=iter)
        self._sm = np.zeros((self.iter, len(model.timeGrid), len(model.maturityGrid)-1)) #depth=iteration, row=maturity, column=discretizedTime
        self._ran = model.distribution()(self._sm.shape)
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

    def initCondition(self,maturityIndex):
        return ((self.model.bondPrices[maturityIndex]-self.model.bondPrices[maturityIndex+1])/((self.model.maturityGrid[maturityIndex+1]-self.model.maturityGrid[maturityIndex])*self.model.bondPrices[maturityIndex+1]))

    def subEngine(self, iter):
        print("Processing iteration:", iter+1)
        return (iter, [Solver.SamplePath(iter=iter, ti=ti, SDE=self.model.SDE, forwardCurve=self.matrix[iter,ti-1], eta = self.model.eta, random=self.random[iter,ti], matrix=self.matrix[iter,ti]) for ti in range(self.matrix.shape[1])])
    
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
    
    def simulate(self):
        print(self.matrix.shape)
        self.matrix[:,0,:] = [self.initCondition(T) for T in range(len(self.model.maturityGrid)-1)]
        self.execute()
        print("Processing done!") 

     #Summary from the sample paths
    def analyze(self):
        self.matrix = np.mean(self.matrix, axis=0)
        avgFR = np.mean(np.nan_to_num(self.matrix), axis=1)[0:len(self.matrix):252]
        df = pd.DataFrame(self.matrix, columns=self.model.maturityGrid[:-1], index=self.model.timeGrid)
        hp.plotDF(df)
        hp.plotNP(avgFR)
        print("Post-Processing done!") 
        return df
        