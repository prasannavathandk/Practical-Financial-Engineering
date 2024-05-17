from SamplePath import SamplePath

class ForwardMeasure(SamplePath):

    def __init__(self, iter = 1000):
        self._it = iter
        pass

    #calculate drift under forward measure for a certain index
    def drift(self):
        print("ForwardMeasure.drift")
        pass

    #calculate drift under martingale discretization
    def martingaleDrift(self):
        print("ForwardMeasure.martingaleDrift")
        pass

    def volatility(self):
        print("ForwardMeasure.volatility")
        pass

    #Entry point to class
    def simulate(self, type):
        print("ForwardMeasure.simulate")
        super().simulate(type)