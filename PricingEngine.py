import numpy as np
import pandas as pd
import math 
from scipy.stats import norm


# black formular for caplet
def BC(F, sigma, T, K, b):

    # calculate d1 and d2
    d1 = math.log(F/K) + (T/2) * sigma**2
    d1 = d1 / (sigma * math.sqrt(T))

    d2 = math.log(F/K) - (T/2) * sigma**2
    d2 = d2 / (sigma * math.sqrt(T))

    return b * (F* norm.cdf(d1) - K*norm.cdf(d2))


def volCalibration(capletVolatility, forwardCurve = None):

    # construct output object
    M = len(capletVolatility)
    volMatrix = np.zeros((M, M))

    # Objects to catch calculated values
    period_volatility = []
    
    # Get bond prices for caplet pricing
    if forwardCurve is None:
        forwardCurve = [0.05]*M
    bondPrices = (1 / (np.array(forwardCurve) + 1).cumprod()).tolist()

    for i in range(M):
        caplet_prices = [BC(F=forwardCurve[i], K=forwardCurve[i], T=(i+1), b=bondPrices[i], sigma=capletVolatility[i]) for i in range(M)]


    # Calibrate the volatility 
    for i in range(M):

        if i == 0: # One period vol can be backed out from one period caplet
            cv = capletVolatility[i]
            period_volatility.append(cv)

        else: # Iteratively solve the equations for n-period vol 
            cv = capletVolatility[i]
            T_i = i+1
            cvs = (np.array(period_volatility)**2)
            
            new_cv = (T_i*(cv**2) - sum(cvs))**(0.5)
            period_volatility.append(new_cv)

        print(period_volatility)
        volMatrix[i, :len(period_volatility)] = list(reversed(period_volatility))

    return (volMatrix, caplet_prices)

class PricingEngine:

    '''
    '''
    def __init__(self, simulation, initial_curve, intervals) -> None:
        self.simulation = simulation
        self.initial_curve = initial_curve
        self.intervals = intervals
        self.iterations = int(simulation.epoch.max())

    def PricingMethods(self):
        methods = {
            'ZeroCouponBond': self.ZerocCouponBond,
            'VanillaCouponBond': self.VanillaCouponBond,
            'Swaption': self.Swaption,
        }
        return methods

    # Main Function to price the asset ------------------------------------------------------------------------------
    def pricing_routine(self, asset, pricing_parameter = None, time_precision = 1):

        M = len(self.initial_curve)
        Prices = []

        for k in range(1,self.iterations + 1):
            DiscountFactor = 1
            Price = 0
            pricing_parameter['timepoint'] = 0
            pricing_parameter['iteration'] = k

            for i in range(M):
                DiscountFactor = DiscountFactor * 1 / (1 + self.initial_curve[0] * self.intervals[i])
                pricing_parameter['timepoint'] = pricing_parameter['timepoint'] + float(self.intervals[i])
                pricing_parameter['timepoint'] = round(pricing_parameter['timepoint'], time_precision)

                CashFlow = self.PricingMethods()[asset](**pricing_parameter)
          
        
                Price = Price + DiscountFactor * CashFlow
                print(Price)
            Prices.append(Price)
            #print('Pricing run for iteration:', k, ' finished with price:', Price)

        Price = np.array(Prices).mean()

        return Price
    
    def ZerocCouponBond(self, T: float, Nominal: float, timepoint: float, iteration: int):

        # Check if Maturity date is in timepoints
        if T not in self.intervals.cumsum():
            raise ValueError("Intervalls not aligned with Maturity Date")

        if T == timepoint:
            return Nominal
        else:
            return 0
    
    def VanillaCouponBond(self, T: float, Nominal: float, timepoint: float, CouponRate: float, Frequency: float, iteration: int):
        
        # Check if Intervalls alling
        if self.intervals[0] != 1 / Frequency:
            raise ValueError("Intervalls not aligned with Frequency")
        
        # Check if Maturity date is in timepoints
        if T not in self.intervals.cumsum():
            raise ValueError("Intervalls not aligned with Maturity Date")

        # Check for coupon payment
        coupon_dates = np.arange(Frequency, T, Frequency)

        if T == timepoint:
            return Nominal + Nominal * CouponRate
        elif timepoint in coupon_dates:
            return Nominal * CouponRate
        else:
            return 0
        

    def VanillaSwap(self, T: float,  StartDate: float, EndDate: float, Nominal: float, FixedRate: float, Frequency: float, iteration: int):

        # Check if Intervalls alling
        if self.intervals[0] != 1 / Frequency:
            raise ValueError("Intervalls not aligned with Frequency")
        
        # Calculate fixed leg cash flows
        fixed_cash_flows = [FixedRate * Nominal] * (EndDate - StartDate)*Frequency

        # Calculate the floatiing 
        discount_factors = [1.0]
        mask = (self.simulation.epoch == iteration) & (self.simulation.Time == T)
        discount_curve = self.simulation[mask].iloc[:, 2:].values[0]
        new_discount_curve = []
        #print(discount_curve)
        for i in range(StartDate+1, EndDate+1):
            new_discount_curve.append(discount_curve[i])
            discount_factors.append(discount_factors[-1]  / (1 + discount_curve[i-1] * self.intervals[i-1]))

        discount_curve = discount_curve[1:]

        # Present value of the floating leg (assumed to be equal to notional value)
        pv_floating_leg = sum(discount_factors[i] * discount_curve[i] * Nominal  for i in range(1, len(discount_factors)))
        
        # Calculate the sum of discount factors for the periods
        pv_fixed_leg = sum(discount_factors[i] * FixedRate * Nominal  for i in range(1, len(discount_factors)))

        #print(pv_floating_leg)
        #print(pv_fixed_leg)
    
        return pv_floating_leg - pv_fixed_leg
    

    def Swaption(self, T: float, timepoint: float, StartDate: float, EndDate: float, Nominal: float, Strike: float, Frequency: float, iteration: int):

        # Check if Intervalls alling
        if self.intervals[0] != 1 / Frequency:
            raise ValueError("Intervalls not aligned with Frequency")
        
        if T == timepoint:
            swapPrice = self.VanillaSwap(T, StartDate, EndDate, Nominal, FixedRate=Strike, Frequency=Frequency, iteration=iteration)
            if swapPrice < 0:
                swapPrice = 0
            return swapPrice
        else:
            return 0

    def SwapRate(self, StartDate: float, EndDate: float, Frequency: float):

        # Check if Intervalls alling
        if self.intervals[0] != 1 / Frequency:
            raise ValueError("Intervalls not aligned with Frequency")
        
        # Calculate Discount Factor
        discount_factors = [1.0]
        for i in range(StartDate, EndDate):
            discount_factors.append(discount_factors[-1] * 1 / (1 + self.initial_curve[i-1] * self.intervals[i-1]))

        # Present value of the floating leg (assumed to be equal to notional value)
        pv_floating_leg = discount_factors[0] - discount_factors[-1]
        
        # Calculate the sum of discount factors for the periods
        sum_discount_factors = sum(discount_factors[i] for i in range(1, len(discount_factors)))
    
        # The swap rate is the rate that equates the present value of the fixed leg to the floating leg
        swap_rate = pv_floating_leg / sum_discount_factors
        
        return swap_rate