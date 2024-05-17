import SpotMeasure
import ForwardMeasure
import Helper as hp

def execute():  
    print("main.execute()")  
    mySM = SpotMeasure.SpotMeasure()
    SMsim = mySM.simulate(type = 0)
    hp.unitTest(mySM)
    hp.plotSP(SMsim)
    myFM = ForwardMeasure.ForwardMeasure()
    hp.unitTest(myFM)
    FMsim = myFM.simulate(type = 1)
    hp.plotSP(FMsim)

def main():
    print("LIBOR Market Model- Simulation")
    execute()

if __name__ == "__main__":
    main()

