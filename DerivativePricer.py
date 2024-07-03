import pandas as pd
from scipy.stats import norm as std
import numpy as np

class DerivativePricing:

    def __init__(self, forwardCurve : pd.DataFrame):
        self.forwardCurve = forwardCurve
    
    @property
    def forwardCurve(self):
        return self._forwardCurve

    @forwardCurve.setter
    def forwardCurve(self, curve):
        self._forwardCurve = curve

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