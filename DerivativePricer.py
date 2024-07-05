import pandas as pd
from scipy.stats import norm as std
import numpy as np

from NumericalSolver import SolutionScheme

class DerivativePricing:

    def __init__(self, derivative, simulator: SolutionScheme):
        self._simulator = simulator
        self._derivative = derivative
        _Maturity = np.sort(np.concatenate([self._derivative['Maturity'], [T + self._derivative['Tenor'] for T in self._derivative['Maturity']]]))
        self._config = {
            'Maturity' : _Maturity,
            'Prices' : self._derivative['BondPricing']([100]*len(_Maturity), [10]*len(_Maturity), _Maturity),
            'Volatility' : [12]*(len(_Maturity) - 1),
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