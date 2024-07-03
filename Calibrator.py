import numpy as np
import Helper as hp
from scipy.optimize import minimize

from LIBORSimulator import LIBORSim
from Parameters import Parameters
from PricingEngine import PricingEngine

class Calibrator:
    def __init__(self, derivative: Parameters.derivatives['Prototype']):
        print("Calibrator::init")
        self.derivative = derivative
        self.pricer = PricingEngine(derivative)   
        Calibrator.volHist = list()

    @property
    def pricer(self):
        return self._pricer

    @pricer.setter
    def pricer(self, value:  PricingEngine):
        self._pricer = value

    @property
    def derivative(self):
        return self._derivative

    @derivative.setter
    def derivative(self, value: Parameters.derivatives['Prototype']):
        self._derivative = value

    def calibrate(self):
        print("Calibrator::calibrate")
        vol = self.optimize()
        hp.plotNP(Calibrator.volHist, title="Volatility History", clear=False)
        return vol
    
    def objectiveFunc(volatility, prices, pricer):
        print("Calibrator::objectiveFunc", volatility, prices, pricer)
        Calibrator.volHist.append(volatility)
        estimates: np.array = pricer.estimate(volatility)
        grounds: np.array = prices
        squared_diff = np.sum((estimates - grounds)**2)
        return squared_diff

    def optimize(self):
        print("Calibrator::optimize")
        initVol = Parameters.intervalVolatility
        result = minimize(fun=Calibrator.objectiveFunc, x0=initVol,
                  args=(self.derivative['Price'], self.pricer),
                  method='BFGS', options={'disp': True})
        return result.x
    
    
