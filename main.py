import multiprocessing
from Parameters import Parameters 
import numpy as np
import Helper as hp
from LIBORSimulator import LIBORSim
import NumericalSolver

def main():
    print("LIBOR Market Model")
    timer = hp.timer()
    print("Simulation initiate...", timer.tick)    
    timer.start()
    
    for ep in range(Parameters.epoch):
        print("Epoch started...", ep+1) 
        simulator = LIBORSim(maturity=Parameters.maturityDates, prices=Parameters.bondPrices, measure=0, iter = Parameters.batch, scale = Parameters.scale, type=0)
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
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            print("number of cores", multiprocessing.cpu_count())
            NumericalSolver.Solver.setPool(pool)
            NumericalSolver.Solver.setParallelism(flag=True)
            main()