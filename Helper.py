import matplotlib.pyplot as plt
import numpy as np

#a vector of standard normal variables
def stdNormal(_,num):
    return np.random.normal(0, 1, num)

#plot function
def plotSP(data):
    #Remove loop and implement direct plot
    for dat in data:
        plt.plot(dat)

#test individuals function calls from the class
def unitTest(myClass):
    pass

def discretize(arr, num):
    for i in range(num):
        arr = np.sort(np.concatenate([arr, np.add(arr,np.concatenate([np.diff(arr)/2,[0]]))]))
    return arr

def plot():
    plt.show()