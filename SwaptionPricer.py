import numpy as np
import pandas as pd
from DerivativePricer import DerivativePricing
from LIBORSimulator import LIBORMeta
from Parameters import Parameters

class SwaptionPricing(DerivativePricing):

    def __init__(self, swaption : Parameters.derivatives['Swaption'], forwardCurve : pd.DataFrame):
        super().__init__(forwardCurve)
        self._swaption = swaption
        self._exercise = swaption['Exercise']
        self._type = swaption['Type']
        self._frequency = swaption['Frequency']
        self._discount = swaption['Discount']
        self._notional = swaption['Notional']
        self._strikeType = swaption['StrikeType']
        self._strike = swaption['Strike']
        self._tenor = swaption['Tenor']
        self._maturity = swaption['Maturity']
        self._volatility = swaption['Volatility']
        self._forwardRate = swaption['ForwardRate']
        self._riskFreeRate = swaption['RiskFreeRate']
        self._analyticalPrice = swaption['Price']
        self._payoff = swaption['Payoff']
        self._marketPrice = swaption['Price']
        self._analyticalPrice = self.analyticalPricing()
        self._marketPrice = self._analyticalPrice
        self._simulatedPrice = None

    @property
    def price(self):
        return self._marketPrice

    @price.setter
    def price(self, value):
        self._marketPrice = value

    @property
    def analyticalPrice(self):
        return self._analyticalPrice

    @analyticalPrice.setter
    def analyticalPrice(self, price):
        self._analyticalPrice = price

    @property
    def simulatedPrice(self):
        return self._simulatedPrice

    @simulatedPrice.setter
    def simulatedPrice(self, price):
        self._simulatedPrice = price
        

    def analyticalPricing(self):
        maturities = self._maturity
        swaptionPrice = np.zeros(len(maturities))
        for i in range(len(swaptionPrice)):
            discount = self._discount
            forward = self._forwardRate[i]/100
            strike = forward
            maturity = maturities[i]
            volatility = self._volatility[i]/100
            notional = self._notional
            riskFreeRate = self._riskFreeRate
            frequency = self._frequency
            swaptionPrice[i] = DerivativePricing.blackSwaptionPrice(discount, forward, strike, maturity, volatility, notional, riskFreeRate, frequency)
        return swaptionPrice   

    def simulatedPrice(self):
        pass

    def estimate(self, volatility: np.array):
        simulator = LIBORMeta(volatility)
        df = simulator.simulate(epoch=0).analyze()
        print(df.head())
        return self.analyticalPrice 

    # def swaptionPricerMicro(self, forwardCurve): #Pricer for one sample path and one maturity
    #     def discountFactor(forwardCurve):
    #         for i in range(numTimeSteps):
    #             discountFactors[:, i + 1] = discountFactors[:, i] / (1 + forwardRates[:, i] * timeSteps[i])

    # def swaptionPricerMeso(self, forwardCurve): #Pricer for one sample path and all maturities
    #     for t in self.derivative['Maturity']:
    #         paymentTimes = np.arange(t, t+self.derivative['Tenor'], step=0.25) 
    #         print(paymentTimes)   

    # def swaptionPricerMacro(self, forwardCurve): #Pricer for all sample paths and all maturities
    #     pass
