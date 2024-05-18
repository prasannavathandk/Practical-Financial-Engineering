import numpy as np
from IModel import ModelInterface
import Helper as hp

class  BrownianMotion(ModelInterface):

    def __init__(self, timeGrid, scale = 2):
        self._tg = hp.discretize(timeGrid, scale)

    distribution = hp.stdNormal
        
    def SDE(self, curVal, step, rv, index):         #SDE according to eulers scheme
        return curVal + self.drift()*step + self.volatility()*np.sqrt(step)*rv

    def volatility(self):
        return 0.75
    
    def drift(self):
        return .1