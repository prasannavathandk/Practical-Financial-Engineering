import multiprocessing
import numpy as np
import pandas as pd
from BondPricer import BondPricing
from Helper import HidePrints
from NumericalSolver import SolutionScheme
from Parameters import Parameters
from itertools import accumulate

class CapletPricing(BondPricing):

    def __init__(self, caplet : Parameters.derivatives['Swaption'], simulator : SolutionScheme):
        super().__init__(caplet, simulator)
        self._caplet = caplet

    def impliedVolatility(self) -> np.array:
        return self._caplet['Volatility']
    
    def GPayoff(self, forwardRates: pd.Series, maturity: int) -> float:
        # print("SwapPricer::GPayoff")
        print("SwapPricer::GPayoff: ", "forwardRates: ", forwardRates, "maturity: ", maturity)
        forwardRates.name = "rate"
        forwardRates = forwardRates.apply(lambda x: max(x, 0))
        forwardRates = forwardRates.reset_index(drop=False)
        # print("SwapPricer::GPayoff: ", "instrument: ", instrument)
        notional = self._caplet['Notional']
        # print("SwapPricer::GPayoff: ", "fixed: ", fixed, "notional: ", notional)
        # print("SwapPricer::GPayoff: ", "instrument: ", instrument)
        payoff = abs(self._caplet['Payoff'](forwardRates['rate'][maturity], forwardRates['rate'][maturity-1], self._caplet['Frequency']))
        # print("SwapPricer::GPayoff: ", "payoff: ", payoff)        
        return payoff*notional

    