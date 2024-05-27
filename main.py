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

    maturityDates = np.array(Parameters.maturityDates)
    bondPrices = np.array([(lambda n: 100/(1+0.1)**n)(i) for i in range(1,11)]) #np.array(Parameters.bondPrices)
    
    for ep in range(Parameters.epoch):
        print("---Epoch %i started---" %(ep+1)) 
        simulator = LIBORSim(maturity=maturityDates, prices=bondPrices, measure=Parameters.measure, type=Parameters.scheme, iter = Parameters.batch)
        simulator.simulate() 
        timer.stop()
        simulator.processSP()  
        timer.stop() 
        del simulator 
        print("---Epoch %i done---"% (ep+1)) 
    print("Simulation complete :) ...", timer.tock)

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        NumericalSolver.Solver.manager = manager
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            print("number of cores", multiprocessing.cpu_count())
            NumericalSolver.Solver.setPool(pool)
            NumericalSolver.Solver.setParallelism(flag=Parameters.parallel)
            main()