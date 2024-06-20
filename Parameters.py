import math

class Parameters:

    measures = {
            'SpotMeasure': 0,
            'ForwardMeasure': 1
        }
    
    schemes = {
            'General': 0,
            'Martingale': 1
        }
    
    #Input Data to Simulation
    maturityDates = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]    #Maturity Dates in years
    resetPeriod = 0.25        #Reset Period of 3 months
    faceValue = [100]*len(maturityDates)
    yieldRate = [5 for t in maturityDates]                 #Yield Curve
    bondPrices = [fv/(1 + y/100)**n for n, fv, y in zip(range(1,len(maturityDates)+1), faceValue, yieldRate)]
    capletPrices = [1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]  #Caplet Prices
    riskFreeRate = 3            #Risk Free Rate in percent

    measure = measures['SpotMeasure']
    scheme = schemes['General']
    volatility = 2.52             #Annual Volatility in percent
    tradingDays = 252           #Number of trading days in a year

    #Simulation Parameters
    epoch = 2        #Number of epochs or batches to run
    batch = lambda core: 5*core        #Number of iterations per epoch = Number of sample paths
    scale = 1           #Number of binary divisions per trading day
    parallel = True     #Flag to run the simulation in parallel
    

    

