from LIBORMarketModel import LIBORModel

class ForwardMeasure(LIBORModel):

    def __init__(self, maturity, prices, scale = 2, type = 0):
        super().__init__(maturity=maturity, prices=prices, scale = scale, type = type)

    #calculate drift under forward measure for a certain index, type = 0
    def genDrift(self):
        return 0.25

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        return 0.50

    def volatility(self):
        return 0.75