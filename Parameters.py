class Parameters:

    measures = {
            'SpotMeasure': 0,
            'ForwardMeasure': 1
        }
    
    schemes = {
            'Simple': 0,
            'Martingale': 1
        }
    
    #Input Data to Simulation
    maturityDates = [1,2,3,4,5,6,7,8,9,10]
    faceValue = [100]*len(maturityDates)
    yieldRate = [10]*len(maturityDates)                 #Annual Yield in percent
    bondPrices = [(lambda n, FV, y: FV/(1 + y/100)**n)(i, fv, y) for i, fv, y in zip(range(1,len(maturityDates)+1), faceValue, yieldRate)]
    
    measure = measures['SpotMeasure']
    scheme = schemes['Simple']
    volatility = 2.52             #Annual Volatility in percent
    tradingDays = 252           #Number of trading days in a year

    #Simulation Parameters
    epoch = 10        #Number of epochs or batches to run
    batch = 10        #Number of iterations per epoch = Number of sample paths
    scale = 1           #Number of binary divisions per trading day
    parallel = True     #Flag to run the simulation in parallel
    

    

