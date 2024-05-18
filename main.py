import multiprocessing
import Helper as hp
from LIBORSimulator import LIBORSim
import NumericalSolver  

def main():
    print("LIBOR Market Model- Simulation")
    timer = hp.timer()
    timer.start()
    maturity_dates = [1,2,3,4,5,6,7,8,9,10]
    simulator = LIBORSim(measure=0, iter = 10, scale = 10, type=0, maturity=maturity_dates, test=True)
    simulator.simulate()
    timer.stop()
    hp.plot()  
    timer.stop()  
    print("Simulation complete")

if __name__ == "__main__":
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as tp:
        NumericalSolver.Solver.setPool(tp)
        NumericalSolver.Solver.setParallelism(flag=False)
        main()