from SamplePath import SamplePath

class SpotMeasure(SamplePath):

    def __init__(self, iter = 1000):
        self._it = iter
        pass

    #calculate drift under spot measure for a certain index
    def drift(self):
        print("SpotMeasure.drift")
        pass

    #calculate drift under martingale discretization
    def martingaleDrift(self):
        print("SpotMeasure.martingaleDrift")
        pass

    def volatility(self):
        print("SpotMeasure.volatility")
        pass

    #Entry point to class
    def simulate(self, type):
        print("SpotMeasure.simulate")
        super().simulate(type)