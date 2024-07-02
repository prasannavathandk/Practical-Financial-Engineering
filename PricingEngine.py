import numpy as np
import math 


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
            'VanillaCouponBond': self.VanillaCouponBond
        }
        return methods


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
            Prices.append(Price)
            print('Pricing run for iteration:', k, ' finished with price:', Price)

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
        

    def VanillaSwap(self, T: float,  StartDate: float, EndDate: float, Nominal: float, FixedRate: float, FloatingRate: float, Frequency: float, iteration: int):

        # Check if Intervalls alling
        if self.intervals[0] != 1 / Frequency:
            raise ValueError("Intervalls not aligned with Frequency")
        
        # Calculate fixed leg cash flows
        fixed_cash_flows = [FixedRate * Nominal] * (EndDate - StartDate)*Frequency

        # Calculate the floatiing 
        discount_factors = [1.0]
        mask = (self.simulation.epoch == iteration) & (self.simulation.Time == T)
        discount_curve = self.simulation[mask].iloc[:, 2:].values

        for i in range(StartDate, EndDate):
            discount_factors.append(discount_factors[-1] * 1 / (1 + discount_curve[i-1] * self.intervals[i-1]))

        # Present value of the floating leg (assumed to be equal to notional value)
        pv_floating_leg = discount_factors[0] - discount_factors[-1]
        
        # Calculate the sum of discount factors for the periods
        sum_discount_factors = sum(discount_factors[i] for i in range(1, len(discount_factors)))
    
        return pv_floating_leg - sum_discount_factors
    
    
    def Swaption(self, T: float, timepoint: float, StartDate: float, EndDate: float, Nominal: float, Strike: float, FloatingRate: float, Frequency: float, iteration: int):

        # Check if Intervalls alling
        if self.intervals[0] != 1 / Frequency:
            raise ValueError("Intervalls not aligned with Frequency")
        
        if T == timepoint:
            swapPrice = self.VanillaSwap(T, StartDate, EndDate, Nominal, FixedRate=Strike, FloatingRate=FloatingRate, Frequency=Frequency, iteration=iteration)
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