import numpy as np
from BM import BrownianMotion
import SpotMeasure as SM
import ForwardMeasure as FM
from NumericalSolver import EulerScheme, Solver
import Helper as hp

class LIBORSim(EulerScheme):

    def __init__(self, maturity, prices, iter = 10, scale = 2, measure=0, type=0):
        if(measure == 1):
            model=FM.ForwardMeasure(type = type, maturity=maturity, prices=prices, scale=scale)
        else:    
            model=SM.SpotMeasure(type = type, maturity=maturity, prices=prices, scale=scale)
        super().__init__(model=model, iter=iter)
        self._sm = np.zeros((self.iter, len(model.maturityGrid)-1, len(model.timeGrid))) #depth=iteration, row=maturity, column=discretizedTime

    @property 
    def simMatrix(self):
        return self._sm

    @simMatrix.setter
    def simMatrix(self, value):
        self._sm = value      

    def initCondition(self,maturityIndex):
        print(maturityIndex)
        return ((self.model.bondPrices[maturityIndex]-self.model.bondPrices[maturityIndex+1])/((self.model.maturityGrid[maturityIndex+1]-self.model.maturityGrid[maturityIndex])*self.model.bondPrices[maturityIndex+1]))

    def engine(self):
        if Solver.parallel is not True:
           for i in range(self.simMatrix.shape[0]):
                for j in range(self.simMatrix.shape[1]):
                    value = self.simMatrix[i,j]
                    N = self.model.distribution((0, 1, self.simMatrix.shape[2])) 
                    self.result.append(Solver.SamplePath(count=i, SDE=self.SDE, timeGrid=self.model.timeGrid, N=N, value=value))
        else:   
            for i in range(self.iter):
                for j in range(self.simMatrix.shape[1]):
                    value = self.simMatrix[i,j]
                    N = self.model.distribution((0, 1, self.simMatrix.shape[2])) 
                    res = Solver.threadPool.apply_async(func=Solver.SamplePath, args=(i, self.SDE, self.model.timeGrid, N, value,))
                    self.log_results(res)
            self.join()        
        return  
    
    def simulate(self):
        self.simMatrix[...,0] = [self.initCondition(T) for T in range(len(self.model.maturityGrid)-1)]
        result = self.execute()
        self.processSP(result)

     #Summary from the sample paths
    def processSP(self, result):
        #print(result)
        hp.plotSP(result)
        