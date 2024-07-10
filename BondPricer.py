import multiprocessing
import numpy as np
import pandas as pd
from DerivativePricer import DerivativePricing
from Helper import HidePrints
from NumericalSolver import SolutionScheme
from Parameters import Parameters


class BondPricing(DerivativePricing):
    def __init__(self, derivative, simulator: SolutionScheme):
        super().__init__(derivative=derivative, simulator=simulator)
        self.derivative = derivative

    def SimulatorMeta(self, volatility: np.array) -> pd.DataFrame:
        # print("SwapPricer::LIBORMeta")
        # print("SwapPricer::LIBORMeta: ", self.config)
        df = None
        with HidePrints():
            df =  self.simulator(maturity=self.config['Maturity'], prices=self.config['Prices'], volatility=volatility, scale=self.config['Scale'], measure=Parameters.measure, type=Parameters.scheme, iter = Parameters.batch(multiprocessing.cpu_count()))    
        return df
        