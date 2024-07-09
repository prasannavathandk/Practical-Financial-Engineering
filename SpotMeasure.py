import numpy as np
from LIBORMarketModel import LIBORModel
import Helper as hp
from Parameters import Parameters

class SpotMeasure(LIBORModel):

    def __init__(self, maturity, prices, scale = Parameters.tradingDays, type = 0):
        super().__init__(maturity=maturity, prices=prices, scale=scale, type = type)
        
    #calculate drift under spot measure for a certain index, type = 0
    def genDrift(self, t, n, nu, forwardCurve):
        #print("SpotMeasure.genDrift", nu, forwardCurve)
        return np.sum([((self.maturityGrid[_nu+1]-self.maturityGrid[_nu])*(forwardCurve[_nu])*(np.dot(self.sigma(t-1, n), self.sigma(t-1, _nu))))/(1+((self.maturityGrid[_nu+1]-self.maturityGrid[_nu])*(forwardCurve[_nu]))) for _nu in nu])

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        return .50
    
    def nu(self, t, n):
        return np.intersect1d(self._eta[t], self._n[n])