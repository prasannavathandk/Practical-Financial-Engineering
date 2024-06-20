import numpy as np
from scipy.optimize import minimize

from LIBORSimulator import LIBORSim
from Parameters import Parameters
from PricingEngine import PricingEngine

class Calibrator:
    def __init__(self, pricer: PricingEngine, marketPrices = Parameters.capletPrices):
        self.pricer = pricer
        self.marketPrices = marketPrices   

    def calibrate(self):
        return self.optimize()
    
    def objectiveFunc(volatility, pricer, marketPrices):
        estimates: np.array = pricer.estimate(volatility)
        grounds: np.array = marketPrices
        squared_diff = np.sum((estimates - grounds)**2)
        return squared_diff

    def optimize(self):
        initVol = Parameters.volatility*[10]
        result = minimize(fun=Calibrator.objectiveFunc, x0=initVol,
                  args=(self.pricer, self.marketPrices),
                  method='BFGS', options={'disp': True})
        return result.x
    
    
