import multiprocessing
import numpy as np
import pandas as pd
from DerivativePricer import DerivativePricing
from NumericalSolver import SolutionScheme
from Parameters import Parameters
from itertools import accumulate

class SwaptionPricing(DerivativePricing):

    def __init__(self, swaption : Parameters.derivatives['Swaption'], simulator : SolutionScheme):
        super().__init__(swaption, simulator)
        self._swaption = swaption

    def analyticalPricing(self):
        maturities = self._swaption['Maturity']
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
    
    def GPayoff(self, instrument: pd.Series, T: float) -> float:
        # print("SwapPricer::GPayoff")
        # print("SwapPricer::GPayoff: ", "instrumnet: ", instrument, "T: ", T)
        instrument.name = "rate"
        instrument = instrument.apply(lambda x: max(x, 0))
        instrument = instrument.reset_index(drop=False)
        # print("SwapPricer::GPayoff: ", "instrument: ", instrument)
        notional = self._swaption['Notional']
        fixed = instrument[instrument['index'] == T]['rate'].values[0]
        # print("SwapPricer::GPayoff: ", "fixed: ", fixed, "notional: ", notional)
        instrument = instrument[instrument['index'] > T]
        instrument = instrument[instrument['index'] <= self._swaption['Tenor'] + T]
        # print("SwapPricer::GPayoff: ", "instrument: ", instrument)
        payoff = list(instrument["rate"].apply(
            lambda x: self._swaption['Payoff'](x, fixed, self._swaption['Frequency'], notional)
        ).values)
        # print("SwapPricer::GPayoff: ", "payoff: ", payoff)
        period = list(instrument['index'].apply(
             lambda x: (x - T)
        ).values)
        # print("SwapPricer::GPayoff: ", "period: ", period)
        value = [(payoff)*(1/(1 + period*rate)) for payoff, period, rate in zip(payoff, period, list(instrument['rate'].values))]
        # print("SwapPricer::GPayoff: ", "value: ", value, "sum: ", np.sum(value))
        return np.sum(value)

    def simulatedPricing(self, volatility: np.array):   

        def micro(samplePoints: pd.Series) -> float:
            # print("SwapPricer::micro")
            # print("SwapPricer::micro", samplePoints)

            discountFactor = np.array(list(accumulate(
                list(samplePoints.values), 
                lambda x, y: (1/(1+x))*(1/(1+y))
            )))
            # print("SwapPricer::micro: ", "discountFactor: ", discountFactor)
            price = np.array([self.GPayoff(instrument=samplePoints, T=int(ind)) for ind in samplePoints.index][0])
            # print("SwapPricer::micro: ", "price: ", price)
            PVPrice = np.multiply(price, discountFactor)
            # print("SwapPricer::micro: ", "PVPrice: ", PVPrice)
            return PVPrice
        
        def meso(samplePath: pd.DataFrame) -> pd.Series:
            # print("SwapPricer::meso")
            samplePath = samplePath.reset_index(level='iteration', drop=True)
            # print("SwapPricer::meso: ", "samplePath: ", samplePath)
            _terRate = samplePath.apply(
                    lambda x: x.iloc[int(x.name)],
                    axis=0
                )
            # print("SwapPricer::meso: ", "_terRate: ", _terRate)
            terRate = pd.Series(_terRate, index=samplePath.columns)
            terRate.name = -1
            terRate = terRate.to_frame().T
            # print("SwapPricer::meso: ", "terFor: ", terRate)
            samplePath = pd.concat(
                objs = [samplePath, terRate]
            )
            # print("SwapPricer::meso: ", "samplePath: ", samplePath.iloc[-1])
            price = micro(samplePoints=samplePath.iloc[-1])
            return pd.Series(price)
        
        def macro(samplePaths: pd.DataFrame) -> None:
            # print("SwapPricer::macro")
            price = samplePaths.groupby('iteration', group_keys=False).apply(meso).mean()
            # print("SwapPricer::macro: ", "price: ", price)
            return np.array(price.values)[self._swaption['Maturity']]

        simulation = self.simulate(volatility)
        # print("SwapPricer::simulatedPricing: ", simulation.head())
        macro(simulation)
        return None #

    def simulate(self, volatility: np.array):
        # print("SwapPricer::simulate")
        simulator = self.SimulatorMeta(volatility)
        forwardCurve = simulator.simulate(epoch=0).analyze()
        return forwardCurve    

    def SimulatorMeta(self, volatility):
        # print("SwapPricer::LIBORMeta")
        print("SwapPricer::LIBORMeta: ", self.config)
        return self.simulator(maturity=self.config['Maturity'], prices=self.config['Prices'], volatility=self.config['Volatility'], scale=self.config['Scale'], measure=Parameters.measure, type=Parameters.scheme, iter = Parameters.batch(multiprocessing.cpu_count()))    
