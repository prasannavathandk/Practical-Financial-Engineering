import multiprocessing
import Helper as hp
from LIBORSimulator import LIBORSim
import NumericalSolver  

def main():
    print("LIBOR Market Model- Simulation")
    timer = hp.timer()
    timer.start()
    maturityDates = [1,2,3,4,5,6,7,8,9,10]
    bondPrices = [10,9,8,7,6,5,4,3,2,1]
    simulator = LIBORSim(maturity=maturityDates, prices=bondPrices, measure=0, iter = 10, scale = 2, type=0)
    simulator.simulate()
    timer.stop()
    hp.plot()  
    timer.stop()  
    print("Simulation complete")

if __name__ == "__main__":
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as tp:
        print("number of cores", multiprocessing.cpu_count())
        NumericalSolver.Solver.setPool(tp)
        NumericalSolver.Solver.setParallelism(flag=True)
        main()