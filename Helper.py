import functools
import threading
import matplotlib.pyplot as plt
import numpy as np
import time  

#a vector of standard normal variables
def stdNormal(num):
    return np.random.normal(0, 1, num)

#plot function
def plotSP(data):
    #Remove loop and implement direct plot
    for dat in data:
        plt.plot(dat)

class timer:     
    tick = 0  
    def start(self):
        self.tick = time.time()
    def stop(self):
        print("--- %s seconds ---" % (time.time() - self.tick)) 
       
#test individuals function calls from the class
def unitTest(myClass):
    pass

def discretize(arr, num):
    for i in range(num):
        arr = np.sort(np.concatenate([arr, np.add(arr,np.concatenate([np.diff(arr)/2,[0]]))]))
    return arr

def plot():
    plt.show()

def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap