import math

class Parameters:

    measures = {
            'SpotMeasure': 0,
            'ForwardMeasure': 1
        }
    
    schemes = {
            'General': 0,
            'Martingale': 1
        }

    derivatives = {
        'Prototype': {
            'Exercise': 'European',
            'type': 'Payer',
            'Frequency': None,  # Quarterly
            'Discount': None,  # Discount Factor
            'Notional': None,
            'StrikeType': 'ATM',  # Same as the forward rate at that time
            'Strike': None,  # Swap/Fixed Rate
            'Tenor': None,  # Interest Rate Swap Tenor
            'Maturity': None,  # Option maturity (exercies) dates in years
            'Midrate': None,
            'ForwardRate': None,  # Forward Rate at time of exercise
            'RiskFreeRate': None,
            'Price': None
        },
        'ZeroCouponBond': {

        },
        'VanillaCouponBond': {

        },
        'Caplet': {

        },
        'Swaption': {
            'Exercise': 'European',
            'type': 'Payer',
            'Frequency': 0.25,  # Quarterly
            'Discount': 0.95,  # Discount Factor
            'Notional': 10**6,
            'StrikeType': 'ATM',  # Same as the forward rate at that time
            'Strike': None,  # Swap/Fixed Rate
            'Tenor': 10,  # Interest Rate Swap Tenor
            'Maturity': [1, 2, 3, 4, 5, 6, 7, 8, 9],  # Option maturity (exercies) dates in years
            'Midrate': [31.15, 30.77, 29.98, 29.51, 29.12, 29.09, 29.21, 29.35, 29.57],
            'ForwardRate': [0.29067, 0.69631, 1.307513, 2.339118, 2.293654, 0.267757, 0.130832, 2.610498, 5.584448],  # Forward Rate at time of exercise
            'RiskFreeRate': 3,
            'Price': None
        }
    }
    
    #Input Data to Simulation
    maturityDates = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]    #Maturity Dates in years
    resetPeriod = 0.25        #Reset Period of 3 months
    faceValue = [100]*len(maturityDates)
    yieldRate = [5 for t in maturityDates]                 #Yield Curve
    volatility = 12.60             #Annual Volatility in percent
    intervalVolatility = [volatility]*len(maturityDates[:-1])
    bondPrices = [fv/(1 + y/100)**n for n, fv, y in zip(range(1,len(maturityDates)+1), faceValue, yieldRate)]
    capletPrices = [1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]  #Caplet Prices
    riskFreeRate = 3            #Risk Free Rate in percent
    tradingDays = 252           #Number of trading days in a year

    measure = measures['ForwardMeasure']
    scheme = schemes['General'] 
    derivative = derivatives['Swaption']
        
    #Simulation Parameters
    epoch = 2        #Number of epochs or batches to run
    batch = lambda core: 5*core        #Number of iterations per epoch = Number of sample paths
    scale = 1           #Number of binary divisions per trading day
    parallel = True     #Flag to run the simulation in parallel
    

    

