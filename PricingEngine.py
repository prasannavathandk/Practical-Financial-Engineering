import numpy as np
import math 


class PricingEngine:

    '''
    '''
    def __init__(self, initial_curve, intervals, simulation) -> None:
        self.initial_curve = initial_curve
        self.intervals = intervals
        self.simulation = simulation

    def PricingMethods(self):
        methods = {
            'ZeroCouponBond': self.ZerocCouponBond,
            'CouponBond': self.CouponBond
        }
        return methods


    def pricing_routine(self, asset):
        D = 1
        P = 1
        C = 0
        M = len(self.initial_curve)
        for i in range(M-2):
            D = D * math.exp(- self.initial_curve[0] * self.intervals[i])

            '''
            evaluate sj (k), j = 1,...,M − i, k = 1,...,d
                (recall that sj (k)=ˆσk(ti−1, ti+j−1))
                generate Z1,...,Zd ∼ N(0, 1)
            evaluate m1,...,mM−i using Fig
            '''
            for j in range(M-2):
                S = 0
            
            P = self.PricingMethods[asset](self, self.intervals[i], self.intervals[i+1])
            C = C + D * P

        return C
    
    def ZerocCouponBond(self, t, T):
        if T == t:
            return 1
        else:
            return 0
    
    def CouponBond(self, t, T, coupon_rate, coupon_dates):
        if T == t:
            return 1 + coupon_rate
        elif t in coupon_dates:
            return coupon_rate
        else:
            return 0