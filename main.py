import SpotMeasure
import ForwardMeasure
import Helper as hp

def execute():  
    print("main.execute()")  

    maturity_dates = [1,2,3,4,5,6,7,8,9,10]

    mySM = SpotMeasure.SpotMeasure(type = 0, maturity=maturity_dates)
    SMsim = mySM.simulate()
    hp.unitTest(mySM)
    hp.plotSP(SMsim)
    myFM = ForwardMeasure.ForwardMeasure(type = 1, maturity=maturity_dates)
    hp.unitTest(myFM)
    FMsim = myFM.simulate()
    hp.plotSP(FMsim)

def main():
    print("LIBOR Market Model- Simulation")
    execute()

if __name__ == "__main__":
    main()

