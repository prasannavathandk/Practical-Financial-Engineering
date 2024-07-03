import numpy as np
from LIBORMarketModel import LIBORModel
from SpotMeasure import SpotMeasure

class ForwardMeasure(LIBORModel):

    def __init__(self, maturity, prices, type = 0):
        super().__init__(maturity=maturity, prices=prices, type = type)

    #calculate drift under forward measure for a certain index, type = 0
    def genDrift(self, t, n, nu, forwardCurve):
        #print("ForwardMeasure.genDrift", nu, forwardCurve)
        return -1*np.sum([((self.maturityGrid[_nu]-self.maturityGrid[_nu - 1])*(forwardCurve[_nu])*(np.dot(self.sigma(t, n), self.sigma(t, _nu))))/(1+((self.maturityGrid[_nu]-self.maturityGrid[_nu-1])*(forwardCurve[_nu]))) for _nu in nu])

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        return 0.50
    
    def nu(self, t, n):
        return self._f[n]