import numpy as np

#a vector of standard normal variables
def stdNormal(num):
    return np.random.normal(0, 1, num)

#plot function
def plotSP(data):
    print("Helper.plotSP")
    pass

#test individuals function calls from the class
def unitTest(myClass):
    print("Helper.unitTest")
    pass

def discretize(arr, num):
    for i in range(num):
        arr = np.sort(np.concatenate([arr, np.subtract(arr,np.gradient(arr)/2)]))
    return arr