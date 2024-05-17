from SamplePath import SamplePath

class ForwardMeasure(SamplePath):

    def __init__(self, iter = 1000, type = 0):
        super().__init__()
        self._it = iter
        self.type = type
        pass

    #calculate drift under forward measure for a certain index, type = 0
    def genDrift(self):
        print("ForwardMeasure.drift")
        pass

    #calculate drift under martingale discretization, type = 1
    def martingaleDrift(self):
        print("ForwardMeasure.martingaleDrift")
        pass

    def volatility(self):
        print("ForwardMeasure.volatility")
        pass