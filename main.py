from BM import BrownianMotion
import Helper as hp
from LIBORSimulator import LIBORSim
from NumericalSolver import EulerScheme    

def main():
    print("LIBOR Market Model- Simulation")
    maturity_dates = [1,2,3,4,5,6,7,8,9,10]
    simulator = LIBORSim(measure=0, iter = 10, scale = 10, type=0, maturity=maturity_dates, test=False)
    simulator.simulate()
    hp.plot()
    print("Simulation complete")

if __name__ == "__main__":
    main()