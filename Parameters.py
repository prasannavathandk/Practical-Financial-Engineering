class Parameters:
    maturityDates = [1,2,3,4,5,6,7,8,9,10]
    bondPrices = [10,9,8,7,6,5,4,3,2,1]
    epoch = 2           #Number of epochs or batches to run
    batch = 10          #Number of iterations per epoch = Number of sample paths
    scale = 13          #Number of binary divisions per time space with *maximum value = 15*
    parallel = True    #Flag to run the simulation in parallel