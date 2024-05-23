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
        self._ran = model.distribution()(self._sm.shape)
        print("Pre-Processing done!") 

    @property 
    def matrix(self):
        return self._sm

    @matrix.setter
    def matrix(self, value):
        self._sm = value  

    @property 
    def sharedMatrix(self):
        return self._sh_sm

    @sharedMatrix.setter
    def sharedMatrix(self, value):
        self._sh_sm = value 

    @property 
    def random(self):
        return self._ran

    @random.setter
    def random(self, value):
        self._ran = value  

    @property 
    def sharedRandom(self):
        return self._sh_ran

    @sharedRandom.setter
    def sharedRandom(self, value):
        self._sh_ran = value           

    def join(self):
        for res in self.result:
            res.wait()    
        self.result = [res.get() for res in self.result]  
        #print(self.result)
        self.matrix = np.array(self.sharedMatrix).reshape(self.matrix.shape)   

    def initCondition(self,maturityIndex):
        #print(maturityIndex)
        return ((self.model.bondPrices[maturityIndex]-self.model.bondPrices[maturityIndex+1])/((self.model.maturityGrid[maturityIndex+1]-self.model.maturityGrid[maturityIndex])*self.model.bondPrices[maturityIndex+1]))

    def subEngine(self, i):
        print("Processing iteration:", i)
        return [(i, j, Solver.SamplePath(iter=i, row=j, start=0, SDE=self.model.SDE, timeGrid=self.model.timeGrid, random=self.random[i,j], matrix=self.matrix[i,j])) for j in range(self.matrix.shape[1])]
    
    def engine(self):
        if Solver.parallel is not True:
           for i in range(self.matrix.shape[0]):
                print("Processing iteration:", i)
                for j in range(self.matrix.shape[1]):
                    Solver.SamplePath(iter=i, row=j, start=0, SDE=self.model.SDE, timeGrid=self.model.timeGrid, random=self.random[i,j], matrix=self.matrix[i,j])
        else:
            asyncRes = [Solver.threadPool.apply_async(func = self.subEngine, args=(i,)) for i in range(self.matrix.shape[0])]
            for ares in asyncRes:
                for elem in ares.get():
                    self.matrix[elem[0], elem[1]] = elem[2]      
        return  
    
    def simulate(self):
        print(self.matrix.shape)
        self.matrix[...,0] = [self.initCondition(T) for T in range(len(self.model.maturityGrid)-1)]
        self.execute()
        print("Processing done!") 

     #Summary from the sample paths
    def processSP(self):
        #print(self.matrix)
        hp.plotSP(self.matrix[0])
        hp.plot()
        print("Post-Processing done!") 
        return self.matrix
        