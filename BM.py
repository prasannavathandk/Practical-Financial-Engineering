import multiprocessing
import numpy as np
from IModel import ModelInterface
import Helper as hp

class  BrownianMotion(ModelInterface):

    lock = multiprocessing.Lock()

    def __init__(self, timeGrid, scale = 2):
        self._tg = hp.discretize(timeGrid, scale)

    def distribution(self):
        with BrownianMotion.lock:
            return hp.stdNormal
  
    def SDE(self, curVal, step, rv, index):
        #SDE according to eulers scheme
        #print("SDE", curVal + self.drift()*step + self.volatility()*np.sqrt(step)*rv) 
        return curVal + self.drift()*step + self.volatility()*np.sqrt(step)*rv

    def volatility(self):
            return 0.75
    
    def drift(self):
            return 0.1