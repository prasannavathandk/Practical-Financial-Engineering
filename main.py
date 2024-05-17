import SpotMeasure
import ForwardMeasure
import Helper as hp

def execute():  
    print("main.execute()")  
    mySM = SpotMeasure.SpotMeasure(type = 0)
    SMsim = mySM.simulate()
    hp.unitTest(mySM)
    hp.plotSP(SMsim)
    myFM = ForwardMeasure.ForwardMeasure(type = 1)
    hp.unitTest(myFM)
    FMsim = myFM.simulate()
    hp.plotSP(FMsim)

def main():
    print("LIBOR Market Model- Simulation")
    execute()

if __name__ == "__main__":
    main()

