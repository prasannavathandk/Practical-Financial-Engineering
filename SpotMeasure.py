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
        return 0.25

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        print("SpotMeasure.martingaleDrift")
        return .50

    def volatility(self):
        print("SpotMeasure.volatility")
        return 0.75