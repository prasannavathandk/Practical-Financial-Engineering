from SamplePath import SamplePath

class ForwardMeasure(SamplePath):

    def __init__(self, iter = 2, type = 0):
        super().__init__()
        self._it = iter
        self.type = type
        pass

    #calculate drift under forward measure for a certain index, type = 0
    def genDrift(self):
        print("ForwardMeasure.genDrift")
        return 0.25

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        print("ForwardMeasure.martingaleDrift")
        return 0.50

    def volatility(self):
        print("ForwardMeasure.volatility")
        return 0.75