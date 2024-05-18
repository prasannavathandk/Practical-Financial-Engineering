import SpotMeasure
import ForwardMeasure
from NumericalSolver import EulerScheme

class LIBORSim(EulerScheme):

    def __init__(self, maturity, iter = 10, measure=0, type=0):
        if(measure == 1):
            super().__init__(ForwardMeasure.ForwardMeasure(type = 1, maturity=maturity), iter)
        else:
            super().__init__(SpotMeasure.SpotMeasure(type = 0, maturity=maturity), iter)

    def simulate(self):
        """
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as tp:
            for i in range(self.iter):
                tp.apply_async(func=self.generateSP, callback=self.log_results) 
        """
        self.execute()