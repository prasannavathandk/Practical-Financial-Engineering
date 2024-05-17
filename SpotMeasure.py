from SamplePath import SamplePath

class SpotMeasure(SamplePath):

    def __init__(self, iter = 1000, type = 0):
        super().__init__()
        self._it = iter
        self.type = type
        pass

    #calculate drift under spot measure for a certain index, type = 0
    def genDrift(self):
        print("SpotMeasure.genDrift")
        pass

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        print("SpotMeasure.martingaleDrift")
        pass

    def volatility(self):
        print("SpotMeasure.volatility")
        pass