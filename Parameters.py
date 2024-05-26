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
    bondPrices = [10,9.5,9,8.5,8,7.5,7,6.5,6,5.5]
    measure = measures['SpotMeasure']
    scheme = schemes['Simple']

    #Simulation Parameters
    epoch = 10          #Number of epochs or batches to run
    batch = 100          #Number of iterations per epoch = Number of sample paths
    scale = 7           #Number of binary divisions per time space with *maximum value = 15*
    parallel = True     #Flag to run the simulation in parallel
    

    

