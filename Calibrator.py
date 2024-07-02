import numpy as np
import Helper as hp
from scipy.optimize import minimize

from LIBORSimulator import LIBORSim
from Parameters import Parameters
from PricingEngine import PricingEngine

class Calibrator:
    def __init__(self, pricer: PricingEngine, marketPrices = Parameters.capletPrices):
        self.pricer = pricer
        self.marketPrices = marketPrices   
        Calibrator.volHist = list()

    def calibrate(self):
        vol = self.optimize()
        hp.plotNP(Calibrator.volHist, title="Volatility History", clear=False)
        return vol
    
    def objectiveFunc(volatility, pricer, marketPrices):
        Calibrator.volHist.append(volatility)
        estimates: np.array = pricer.estimate(volatility)
        grounds: np.array = marketPrices
        squared_diff = np.sum((estimates - grounds)**2)
        return squared_diff

    def optimize(self):
        initVol = Parameters.intervalVolatility
        result = minimize(fun=Calibrator.objectiveFunc, x0=initVol,
                  args=(self.pricer, self.marketPrices),
                  method='BFGS', options={'disp': True})
        return result.x
    
    
