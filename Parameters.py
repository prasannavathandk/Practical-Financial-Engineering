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
    bondPrices = None
    measure = measures['SpotMeasure']
    scheme = schemes['Simple']
    volatility = 2.52             #Annual Volatility in percent
    tradingDays = 252           #Number of trading days in a year

    #Simulation Parameters
    epoch = 1         #Number of epochs or batches to run
    batch = 100         #Number of iterations per epoch = Number of sample paths
    scale = 1           #Number of binary divisions per trading day
    parallel = True     #Flag to run the simulation in parallel
    

    

