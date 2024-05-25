import multiprocessing

import numpy as np
import Helper as hp
from LIBORSimulator import LIBORSim
import NumericalSolver  

def main():
    print("LIBOR Market Model")
    timer = hp.timer()
    print("Simulation initiate...", timer.tick)    
    timer.start()
    maturityDates = [1,2,3,4,5,6,7,8,9,10]
    bondPrices = [10,9,8,7,6,5,4,3,2,1]
    epoch = 10
    batch = 10
    scale = 10
    for ep in range(epoch):
        print("Epoch started...", ep+1) 
        simulator = LIBORSim(maturity=maturityDates, prices=bondPrices, measure=0, iter = batch, scale = scale, type=0)
        simulator.simulate() 
        timer.stop()
        simulator.processSP()  
        timer.stop() 
        del simulator 
        print("Epoch complete...", ep+1) 
    print("Simulation complete :) ...", timer.tock)

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        NumericalSolver.Solver.manager = manager
        with multiprocessing.Pool(processes=multiprocessing.cpu_count(), maxtasksperchild=25) as pool:
            print("number of cores", multiprocessing.cpu_count())
            NumericalSolver.Solver.setPool(pool)
            NumericalSolver.Solver.setParallelism(flag=True)
            main()