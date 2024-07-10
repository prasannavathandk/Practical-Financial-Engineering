import numpy as np
from BondPricer import BondPricing
import Helper as hp
from scipy.optimize import minimize

class Calibrator:
    def __init__(self, pricer : BondPricing):
        print("Calibrator::init")
        self.pricer = pricer  
        Calibrator.volHist = list()

    @property
    def pricer(self):
        return self._pricer

    @pricer.setter
    def pricer(self, value:  BondPricing):
        self._pricer = value

    def calibrate(self):
        print("Calibrator::calibrate")
        vol = self.optimize()
        #hp.plotNP(Calibrator.volHist, title="Volatility History", clear=False)
        print("Calibrator::calibrate: RESULT", vol)
        return vol
    
    def objectiveFunc(volatility, pricer):                                                                     
        print("Calibrator::objectiveFunc", volatility, pricer)
        Calibrator.volHist.append(volatility)        
        estimates: np.array = pricer.simulatedPricing(volatility)                                                                                                                           
        grounds: np.array = pricer.analyticalPricing()
        print("Calibrator::objectiveFunc: ", "est: ", estimates, "gr: ", grounds)
        squared_diff = np.sum((estimates - grounds)**2)
        print("Calibrator::objectiveFunc: ", "squared_diff: ", squared_diff)
        return squared_diff

    def optimize(self):
        print("Calibrator::optimize")
        initVol = self.pricer.config['Volatility']
        result = minimize(fun=Calibrator.objectiveFunc, x0=initVol,
                  args=(self.pricer),
                  method='BFGS', options={'disp': True})
        return result.x

    def volCalibration(self, capletVolatility):

        # construct output object
        M = len(capletVolatility)
        volMatrix = np.zeros((M, M))
        period_volatility = []

        for i in range(M):

            if i == 0: # One period vol can be backed out from one period caplet
                cv = capletVolatility[i]
                period_volatility.append(cv)

            else: # Iteratively solve the equations for n-period vol 
                cv = capletVolatility[i]
                T_i = i+1
                cvs = (np.array(period_volatility)**2)
                
                new_cv = (T_i*(cv**2) - sum(cvs))**(0.5)
                period_volatility.append(new_cv)

            print(period_volatility)
            volMatrix[i, :len(period_volatility)] = list(reversed(period_volatility))
        return volMatrix    
    
    
