from BM import BrownianMotion
import SpotMeasure as SM
import ForwardMeasure as FM
from NumericalSolver import EulerScheme
import Helper as hp

class LIBORSim(EulerScheme):

    def __init__(self, maturity, iter = 10, scale = 2, measure=0, type=0, test=False):
        if(measure == 1):
            model=FM.ForwardMeasure(type = 1, maturity=maturity, scale=scale)
        else:    
            model=SM.SpotMeasure(type = 0, maturity=maturity, scale=scale)
        if(test):
            model = BrownianMotion(timeGrid=maturity,scale=scale)
        super().__init__(model=model, iter=iter)


    def simulate(self):
        result = self.execute()
        self.processSP(result)

     #Summary from the sample paths
    def processSP(self, result):
        #print(result)
        hp.plotSP(result)
        