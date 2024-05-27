from Parameters import Parameters

import numpy as np
from LIBORMarketModel import LIBORModel
import Helper as hp

class SpotMeasure(LIBORModel):

    def __init__(self, maturity, prices, type = 0):
        super().__init__(maturity=maturity, prices=prices, type = type)
        
    #calculate drift under spot measure for a certain index, type = 0
    def genDrift(self, eta, forwardCurve):
        #print("SpotMeasure.genDrift", eta, forwardCurve)
        return np.sum([((self.maturityGrid[_eta+1]-self.maturityGrid[_eta])*(forwardCurve[_eta])*(np.dot(self.volatility(_eta, True), self.volatility(_eta, True))))/(1+((self.maturityGrid[_eta+1]-self.maturityGrid[_eta])*(forwardCurve[_eta]))) for _eta in eta])

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        return .50