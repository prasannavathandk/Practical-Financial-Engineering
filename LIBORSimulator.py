import numpy as np
from BM import BrownianMotion
import SpotMeasure as SM
import ForwardMeasure as FM
from NumericalSolver import EulerScheme, Solver
import Helper as hp

class LIBORSim(EulerScheme):

    def __init__(self, maturity, prices, measure=0, type=0, iter = 10, scale = 2):
        if(measure == 1):
            model=FM.ForwardMeasure(type = type, maturity=maturity, prices=prices, scale=scale)
        else:    
            model=SM.SpotMeasure(type = type, maturity=maturity, prices=prices, scale=scale)
        super().__init__(model=model, iter=iter)
        self._sm = np.zeros((self.iter, len(model.maturityGrid)-1, len(model.timeGrid))) #depth=iteration, row=maturity, column=discretizedTime
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

    def subEngine(self, i):
        print("Processing iteration:", i+1)
        return (i, [Solver.SamplePath(iter=i, row=j, SDE=self.model.SDE, random=self.random[i,j], matrix=self.matrix[i,j]) for j in range(self.matrix.shape[1])])
    
    def engine(self):
        if Solver.parallel is not True:
           for i in range(self.matrix.shape[0]):
                print("Processing iteration:", i+1)
                for j in range(self.matrix.shape[1]):
                    Solver.SamplePath(iter=i, row=j, SDE=self.model.SDE, random=self.random[i,j], matrix=self.matrix[i,j])
        else:
            asyncRes = [Solver.threadPool.apply_async(func = self.subEngine, args=(i,), callback = self.popMatrix) for i in range(self.matrix.shape[0])]
            for ares in asyncRes:
                ares.wait()    
        return  
    
    def simulate(self):
        print(self.matrix.shape)
        self.matrix[...,0] = [self.initCondition(T) for T in range(len(self.model.maturityGrid)-1)]
        self.execute()
        print("Processing done!") 

     #Summary from the sample paths
    def processSP(self):
        #print(self.matrix)
        self.matrix = np.mean(self.matrix, axis=0)
        hp.plotSP(self.matrix)
        print("Post-Processing done!") 
        return self.matrix
        