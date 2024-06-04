import functools
import threading
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time, datetime
from Parameters import Parameters 

#a vector of standard normal variables
def stdNormal(shape):
    return np.random.default_rng().standard_normal(size=shape)

def plotDF(df, title, clear=True):
    df.plot(figsize = (24,12), legend=True)
    plt.title("(Sexy-) LIBOR Curves, " + title)
    plt.xlabel("Time Axis")
    plt.ylabel("Forward Rate")
    plt.legend(loc="lower right")
    plt.figtext(0.5, 0.01, "Maturity Dates = " + str(Parameters.maturityDates) + ", Bond Prices = " + str(Parameters.bondPrices), va="bottom", ha="center")
    plt.savefig(title + ".png") 
    if clear: plt.close()

def plotNP(data, title, clear=True):
    plt.bar(range(1, len(data) + 1), data)
    plt.title("Maturity Averaged Forward Rates" + title)
    plt.xlabel("Time Axis")
    plt.ylabel("Forward Rate")
    plt.savefig(title + ".png") 
    if clear: plt.close()     

def showPLot():
    plt.show()       

class timer:     
    tick = datetime.datetime.now()
    tock = datetime.datetime.now()
    def start(self):
        self.tick = time.time()
    def stop(self):
        self.tock = datetime.datetime.now()
        print("--- %s seconds ---" % (time.time() - self.tick)) 
       
#test individuals function calls from the class
def unitTest(myClass):
    pass

def discretize(arr):
    arr = np.concatenate([[0], np.sort(arr)])
    arr = [i*(1/Parameters.tradingDays) for i in range(arr[-1]*Parameters.tradingDays + 1)]
    for _ in range(Parameters.scale-1):
        arr = np.sort(np.concatenate([arr,np.add(arr[:-1],np.diff(arr)/2)]))
    return arr

# Mapping function to convert maturity to years
def maturity_to_years(maturity):
    if 'month' in maturity:
        return int(maturity.split()[0]) / 12
    elif 'year' in maturity:
        return int(maturity.split()[0])
    return None