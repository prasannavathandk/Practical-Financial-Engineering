from scipy.stats import norm as std
import numpy as np
from Parameters import Parameters

class Swaptions:

    def __init__(self, swaption : Parameters.derivatives['Prototype']):
        self.swaption = swaption

    def price(self):
        maturity = self.swaption['Maturity']
        swaptionPrice = np.zeros(len(maturity))
        for i in range(len(swaptionPrice)):
            discount = self.swaption['Discount']
            forward = self.swaption['ForwardRate'][i]/100
            strike = forward
            maturity = self.swaption['Maturity'][i]
            volatility = self.swaption['Midrate'][i]/100
            notional = self.swaption['Notional']
            riskFreeRate = self.swaption['RiskFreeRate']
            frequency = self.swaption['Frequency']
            #print("AnalyticalPricer::price: ",discount, forward, strike, maturity, volatility, notional, riskFreeRate, frequency)
            swaptionPrice[i] = PricingFormulae.blackSwaptionPrice(discount, forward, strike, maturity, volatility, notional, riskFreeRate, frequency)
        
        return swaptionPrice
    
class PricingFormulae:

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