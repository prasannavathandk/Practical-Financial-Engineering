import numpy as np
from LIBORMarketModel import LIBORModel
import Helper as hp

class SpotMeasure(LIBORModel):

    def __init__(self, maturity, prices, type = 0):
        super().__init__(maturity=maturity, prices=prices, type = type)
        
    #calculate drift under spot measure for a certain index, type = 0
    def genDrift(self, nu, forwardCurve):
        #print("SpotMeasure.genDrift", nu, forwardCurve)
        return np.sum([((self.maturityGrid[_nu+1]-self.maturityGrid[_nu])*(forwardCurve[_nu])*(np.dot(self.sigma(_nu, True), self.sigma(_nu, True))))/(1+((self.maturityGrid[_nu+1]-self.maturityGrid[_nu])*(forwardCurve[_nu]))) for _nu in nu])

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        return .50
    
    def nu(self, t, n):
        return np.intersect1d(self._eta[t], self._n[n])