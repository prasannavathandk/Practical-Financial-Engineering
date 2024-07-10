import contextlib
import functools
import math
import os
import sys
import threading
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time, datetime
from Parameters import Parameters 
from scipy.stats import norm

#a vector of standard normal variables
def stdNormal(shape):
    return np.random.default_rng().standard_normal(size=shape)

def plotDF(df, title, clear=True):
    df.plot(figsize = (24,12), legend=True)
    plt.title("LIBOR Forward Rate Curve, " + title)
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

def discretize(arr, scale=1):
    arr = np.concatenate([[0], np.sort(arr)])
    arr = [i*(1/scale) for i in range(int(arr[-1]*scale + 1))]
    return arr

# Mapping function to convert maturity to years
def maturity_to_years(maturity):
    if 'month' in maturity:
        return int(maturity.split()[0]) / 12
    elif 'year' in maturity:
        return int(maturity.split()[0])
    return None

@contextlib.contextmanager
def HidePrints():
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        yield 

def initCondition(bondPrices, maturities):
    def initCond(maturityIndex):
        return ((bondPrices[maturityIndex]-bondPrices[maturityIndex+1])/((maturities[maturityIndex+1]-maturities[maturityIndex])*bondPrices[maturityIndex+1]))
    return np.array([initCond(T) for T in range(len(maturities)-1)])

def BC(F, sigma, T, K, b):

    # calculate d1 and d2
    d1 = math.log(F/K) + (T/2) * sigma**2
    d1 = d1 / (sigma * math.sqrt(T))

    d2 = math.log(F/K) - (T/2) * sigma**2
    d2 = d2 / (sigma * math.sqrt(T))

    return b * (F* norm.cdf(d1) - K*norm.cdf(d2))               
