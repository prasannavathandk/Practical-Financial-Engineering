
import Helper as hp
from LIBORSimulator import LIBORSim    

def main():
    print("LIBOR Market Model- Simulation")
    maturity_dates = [1,2,3,4,5,6,7,8,9,10]
    simulator = LIBORSim(measure=0, type=1, maturity=maturity_dates)
    simulator.simulate()

if __name__ == "__main__":
    main()