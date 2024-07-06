import multiprocessing
import numpy as np
import pandas as pd
from DerivativePricer import DerivativePricing
from Helper import HidePrints
from NumericalSolver import SolutionScheme
from Parameters import Parameters
from itertools import accumulate

class SwaptionPricing(DerivativePricing):

    def __init__(self, swaption : Parameters.derivatives['Swaption'], simulator : SolutionScheme):
        super().__init__(swaption, simulator)
        self._swaption = swaption

    def analyticalPricing(self):
        maturities = self._swaption['Maturity'][:-1]
        swaptionPrice = np.zeros(len(maturities))
        for i in range(len(swaptionPrice)):
            discount = self._swaption['Discount']
            forward = self._swaption['ForwardRate'][i]/100
            strike = forward
            maturity = maturities[i]
            marketVol = self._swaption['MarketData'][i]/100
            notional = self._swaption['Notional']
            riskFreeRate = self._swaption['RiskFreeRate']
            frequency = self._swaption['Frequency']
            swaptionPrice[i] = DerivativePricing.blackSwaptionPrice(discount, forward, strike, maturity, marketVol, notional, riskFreeRate, frequency)
        return swaptionPrice   
    
    def GPayoff(self, instrument: pd.Series, fixed: float) -> float:
        # print("SwapPricer::GPayoff")
        # print("SwapPricer::GPayoff: ", "instrumnet: ", instrument, "fixed: ", fixed)
        instrument.name = "rate"
        instrument = instrument.apply(lambda x: max(x, 0))
        instrument = instrument.reset_index(drop=False)
        # print("SwapPricer::GPayoff: ", "instrument: ", instrument)
        notional = self._swaption['Notional']
        # print("SwapPricer::GPayoff: ", "fixed: ", fixed, "notional: ", notional)
        # print("SwapPricer::GPayoff: ", "instrument: ", instrument)
        payoff = list(instrument["rate"].apply(
            lambda x: abs(self._swaption['Payoff'](x, fixed, self._swaption['Frequency'], 1))
        ).values)
        # print("SwapPricer::GPayoff: ", "payoff: ", payoff)        
        return sum(payoff)*notional

    def SimulatorMeta(self, volatility: np.array) -> pd.DataFrame:
        # print("SwapPricer::LIBORMeta")
        # print("SwapPricer::LIBORMeta: ", self.config)
        df = None
        with HidePrints():
            df =  self.simulator(maturity=self.config['Maturity'], prices=self.config['Prices'], volatility=volatility, scale=self.config['Scale'], measure=Parameters.measure, type=Parameters.scheme, iter = Parameters.batch(multiprocessing.cpu_count()))    
        return df