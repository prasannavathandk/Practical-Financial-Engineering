from LIBORMarketModel import LIBORModel
import Helper as hp

class SpotMeasure(LIBORModel):

    def __init__(self, maturity, scale = 2, type = 0):
        super().__init__(maturity=maturity, scale = scale, type = type)
        
    #calculate drift under spot measure for a certain index, type = 0
    def genDrift(self):
        return 0.25

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        return .50

    def volatility(self):
        return 0.75