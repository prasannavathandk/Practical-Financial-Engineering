import numpy as np
import pandas as pd
from DerivativePricer import DerivativePricing
from LIBORSimulator import LIBORMetaSwaption
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
    
    def simulate(self, volatility: np.array):
        simulator = LIBORMetaSwaption(volatility, maturity= self._maturity, tenor=self._tenor, scale=1)
        forwardCurve = simulator.simulate(epoch=0).analyze()
        forwardCurve = forwardCurve.reset_index(level='time', drop=False)
        return forwardCurve

    def GPayoff(self, samplePath: pd.DataFrame, T: float) -> float:
            #print("SwapPricer::GPayoff")
            maturity = self._maturity
            index = maturity.index(T)
            notional = self._notional
            fixed = samplePath['T' + str(T)][samplePath['time'] == T].values[0]
            samplePath = samplePath[samplePath['time'] > T]
            samplePath['payoff'] = samplePath.apply(
                lambda x: self._payoff(x['T' + str(T)], fixed, self._frequency, notional), 
                axis=1
            )
            samplePath['discountFactor'] = samplePath[['time', 'T' + str(T)]].apply(
                 lambda x: 1/(1 + x[1])**(x[0] - T),
                 axis=1
            )
            discountedPayoff = samplePath['payoff'] * samplePath['discountFactor']
            print("SwapPricer::GPayoff: ", "discountedPayoff: ", discountedPayoff)
            return discountedPayoff.sum()

    def simulatedPricing(self, volatility: np.array): 

        maturity = self._maturity       

        def micro(samplePath: pd.DataFrame, T: float) -> float:
            #print("SwapPricer::micro")
            index = maturity.index(T)
            optionPeriod = np.concatenate([[0], np.array(maturity[0:index])])
            interval = np.diff(optionPeriod)
            #print(optionPeriod, interval)            
            #print("SwapPricer::micro: ", "payoff: ", payoff)
            discount = 1
            for n, Tn in enumerate(optionPeriod[1:]):
                #print("deflatedPayoff", n, Tn, interval[n], samplePath['T' + str(Tn)][samplePath['time'] == Tn].values)
                discount *= 1/(1 + interval[n] * samplePath['T' + str(Tn)][samplePath['time'] == Tn].values[0])
            #print("SwapPricer::micro: ", "price: ", payoff * discount) 
            payoff = self.GPayoff(samplePath=samplePath, T=T) 
            print("SwapPricer::micro: ", "payoff: ", payoff, "discount: ", discount, "price: ", payoff * discount)  
            return payoff*discount
        
        def meso(samplePath: pd.DataFrame) -> pd.Series:
            #print("SwapPricer::meso")
            price = np.zeros(len(maturity))
            for n, T in enumerate(maturity):
                price[n] = micro(samplePath, T)
            print("SwapPricer::meso: ", "price: ", price)
            return pd.Series(price, index=maturity)
        
        def macro(samplePaths: pd.DataFrame) -> None:
            #print("SwapPricer::macro")
            price = samplePaths.groupby('iteration', group_keys=False).apply(meso).mean()
            #print("SwapPricer::macro: ", "price: ", price)
            self.simulatedPrice = np.array(price.values)
            print("SwapPricer::macro: ", "price: ", self.simulatedPrice)
            return True

        samplePaths = self.simulate(volatility)
        return macro(samplePaths)

    def estimate(self, volatility: np.array):
        self.simulatedPricing(volatility)
    
