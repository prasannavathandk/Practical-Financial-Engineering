import multiprocessing

import numpy as np
import Helper as hp
from LIBORSimulator import LIBORSim
import NumericalSolver  

def main():
    print("LIBOR Market Model- Simulation")
    timer = hp.timer()
    timer.start()
    maturityDates = [1,2,3,4,5,6,7,8,9,10]
    bondPrices = [10,9,8,7,6,5,4,3,2,1]
    simulator = LIBORSim(maturity=maturityDates, prices=bondPrices, measure=0, iter = 15, scale = 12, type=0)
    simulator.simulate()
    timer.stop()
    simulator.processSP()  
    timer.stop()  
    print("Simulation complete")

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        NumericalSolver.Solver.manager = manager
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            print("number of cores", multiprocessing.cpu_count())
            NumericalSolver.Solver.setPool(pool)
            NumericalSolver.Solver.setParallelism(flag=False)
            main()