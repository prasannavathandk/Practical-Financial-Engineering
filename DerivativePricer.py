from abc import abstractmethod
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

    def blackCapPrice(forward, strike, maturity, volatility, notional, b):
        d1 = (np.log(forward / strike) + (((volatility**2)*maturity) / 2)) / (volatility * np.sqrt(maturity))
        d2 = d1 - (volatility*np.sqrt(maturity))
        price = notional * b * (forward*std.cdf(d1) - strike*std.cdf(d2))
        return price

    # def blackSwaptionPrice(discount, forward, strike, maturity, volatility, notional, riskFreeRate, frequency):
    #     #print("AnalyticalPricer::blackSwaptionPrice: ",discount, forward, strike, maturity, volatility, notional, riskFreeRate, frequency)
    #     PVBP = notional * discount
    #     d1 = (np.log(forward / strike) + (((volatility**2)*maturity) / 2)) / (volatility * np.sqrt(maturity))
    #     d2 = d1 - (volatility*np.sqrt(maturity))
    #     price = PVBP * (forward*std.cdf(d1) - strike*std.cdf(d2))
    #     print("AnalyticalPricer::blackSwaptionPrice: ",PVBP, forward, d1, d2, std.cdf(d1), std.cdf(d2), price)
    #     return price 

    @abstractmethod
    def GPayoff(self):
        pass

    @abstractmethod
    def SimulatorMeta(self, volatility: np.array) -> pd.DataFrame:
        pass
    
    def discountFactor(self, rate, maturity = None) -> np.array:
        rate = np.array(rate)/100
        rate = np.concatenate(([1], rate))
        return np.array(list(accumulate(
                rate, 
                lambda x, y: x*(1/(1 + max(y, 0)))
            )))[1:]
    
    def simulatedPricing(self, volatility: np.array):   

        def micro(samplePoints: pd.Series) -> float:
            #print("DerivativePricing::micro")
            print("DerivativePricing::micro", samplePoints.head())
            termValues = samplePoints.iloc[-1]
            discountFactor = self.discountFactor(list(termValues.values), None)
            print("DerivativePricing::micro: ", "discountFactor: ", discountFactor)
            price = np.array([self.GPayoff(forwardRates=pd.concat([pd.Series([samplePoints.iloc[0][ind]]), termValues]), maturity=int(ind)) for ind in termValues.index])
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
            price = micro(samplePoints=samplePath)
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
        print(forwardCurve.head())
        return forwardCurve     
