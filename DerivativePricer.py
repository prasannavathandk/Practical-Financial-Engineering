from itertools import accumulate
import pandas as pd
from scipy.stats import norm as std
import numpy as np
from NumericalSolver import SolutionScheme

class DerivativePricing:

    def __init__(self, derivative, simulator: SolutionScheme):
        self._simulator = simulator
        self._derivative = derivative
        self._config = {
            'Maturity' : self._derivative['Maturity'],
            'Prices' : self._derivative['BondPricing']([100]*len(self._derivative['Maturity']), [10]*len(self._derivative['Maturity']), self._derivative['Maturity']),
            'Volatility' : [12]*(len(self._derivative['Maturity']) - 1),
            'Scale' : 1/self._derivative['Frequency']
        }
    
    @property
    def simulator(self):
        return self._simulator

    @property
    def config(self):
        return self._config

    def blackCapPrice(forward, strike, maturity, volatility, notional, riskFreeRate):
        d1 = (np.log(forward / strike) + (((volatility**2)*maturity) / 2)) / (volatility * np.sqrt(maturity))
        d2 = d1 - (volatility*np.sqrt(maturity))
        price = notional*np.exp(-riskFreeRate * maturity) * (forward*std.cdf(d1) - strike*std.cdf(d2))
        return price

    def blackSwaptionPrice(discount, forward, strike, maturity, volatility, notional, riskFreeRate, frequency):
        #print("AnalyticalPricer::blackSwaptionPrice: ",discount, forward, strike, maturity, volatility, notional, riskFreeRate, frequency)
        PVBP = notional* discount * (1 - discount) / (forward * (10 / frequency))
        d1 = (np.log(forward / strike) + (((volatility**2)*maturity) / 2)) / (volatility * np.sqrt(maturity))
        d2 = d1 - (volatility*np.sqrt(maturity))
        price = PVBP * (forward*std.cdf(d1) - strike*std.cdf(d2))
        #print("AnalyticalPricer::blackSwaptionPrice: ",PVBP, forward, d1, d2, std.cdf(d1), std.cdf(d2), price)
        return price 

    def simulatedPricing(self, volatility: np.array):   

        def micro(samplePoints: pd.Series) -> float:
            #print("DerivativePricing::micro")
            #print("DerivativePricing::micro", samplePoints)

            discountFactor = np.array(list(accumulate(
            list(samplePoints.values), 
            lambda x, y: max(x,0)*(1/(1 + max(y, 0)))
            )))
            #print("DerivativePricing::micro: ", "discountFactor: ", discountFactor)
            price = np.array([self.GPayoff(instrument=samplePoints, fixed=int(ind)) for ind in samplePoints.index][0])
            #print("DerivativePricing::micro: ", "price: ", price)
            PVPrice = np.multiply(price, discountFactor)
            #print("DerivativePricing::micro: ", "PVPrice: ", PVPrice)
            return PVPrice
        
        def meso(samplePath: pd.DataFrame) -> pd.Series:
            #print("DerivativePricing::meso")
            samplePath = samplePath.reset_index(level='iteration', drop=True)
            #print("DerivativePricing::meso: ", "samplePath: ", samplePath)
            _terRate = samplePath.apply(
                lambda x: x.iloc[int(x.name)],
                axis=0
            )
            #print("DerivativePricing::meso: ", "_terRate: ", _terRate)
            terRate = pd.Series(_terRate, index=samplePath.columns)
            terRate.name = -1
            terRate = terRate.to_frame().T
            #print("DerivativePricing::meso: ", "terFor: ", terRate)
            samplePath = pd.concat(
            objs = [samplePath, terRate]
            )
            #print("DerivativePricing::meso: ", "samplePath: ", samplePath.iloc[-1])
            price = micro(samplePoints=samplePath.iloc[-1])
            return pd.Series(price)
        
        def macro(samplePaths: pd.DataFrame) -> None:
            #print("DerivativePricing::macro")
            price = samplePaths.groupby('iteration', group_keys=False).apply(meso).mean()
            #print("DerivativePricing::macro: ", "price: ", price)
            return np.array(price.values)

        simulation = self.simulate(volatility)
        #print("DerivativePricing::simulatedPricing: ", simulation.head())
        price = macro(simulation)
        return price

    def simulate(self, volatility: np.array):
        #print("DerivativePricing::simulate")
        simulator = self.SimulatorMeta(volatility)
        forwardCurve = simulator.simulate(epoch=0).analyze()
        return forwardCurve     
