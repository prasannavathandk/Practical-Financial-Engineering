import pandas as pd
from DerivativePricer import DerivativePricing
from Parameters import Parameters


class BondPricing(DerivativePricing):
    def __init__(self, bond: Parameters.derivatives['ZeroCouponBond'], forwardCurve: pd.DataFrame):
        super().__init__(forwardCurve=forwardCurve)
        self._bond = bond
        self._maturity = bond['Maturity']
        self._faceValue = bond['Notional']
        self._price = bond['Price']
        self._yieldRate = bond['YieldRate']
        self._couponRate = bond['CouponRate']
        self._riskFreeRate = bond['RiskFreeRate']
        self._payoff = bond['Payoff']
        
    def analyticalPricing(self):
        pass

    def simulatedPrice(self):
        pass
        