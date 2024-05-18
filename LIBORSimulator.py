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
        super().__init__(model=model, iter=iter, distribution=model.distribution, sde=model.SDE)    

    def simulate(self):
        """
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as tp:
            for i in range(self.iter):
                tp.apply_async(func=self.generateSP, callback=self.log_results) 
        """
        result = self.execute()
        self.processSP(result)

     #Summary from the sample paths
    def processSP(self, result):
        hp.plotSP(result)    