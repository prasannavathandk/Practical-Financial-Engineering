import numpy as np
import pandas as pd
import math 


# Vol Calibration ------------------------------------------------------------------------------------------------
def volCalibration(capletVolatility):

    # construct output object
    M = len(capletVolatility)
    volMatrix = np.zeros((M, M))
    period_volatility = []

    for i in range(M):

        if i == 0: # One period vol can be backed out from one period caplet
            cv = capletVolatility[i]
            period_volatility.append(cv)

        else: # Iteratively solve the equations for n-period vol 
            cv = capletVolatility[i]
            T_i = i+1
            cvs = (np.array(period_volatility)**2)
            
            new_cv = (T_i*(cv**2) - sum(cvs))**(0.5)
            period_volatility.append(new_cv)

        print(period_volatility)
        volMatrix[i, :len(period_volatility)] = list(reversed(period_volatility))
    return volMatrix

# Bond Calibration -------------------------------------------------------------------------------------------------
from PyCurve.nelson_siegel import NelsonSiegel
from PyCurve.curve import Curve

import Helper as hp
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd

class BondScraper:
    
    def __init__(self, country):
        self.country = country
        self.url = f'https://www.worldgovernmentbonds.com/country/{country}/'
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        
    def fetch_data(self):
        # Fetch the webpage content
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text
    
    def parse_data(self, html):
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')

        # Find the table
        table = soup.find('table', {'class': 'w3-table money pd22 -f14'})

        # Extract table headers
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text.strip())
        headers = [item for item in headers if item]

        # Extract table rows
        rows = []
        for tr in table.find_all('tr')[2:]:  # Skip the header rows
            cells = tr.find_all('td')
            if cells:  # Only process rows with data
                row = [cell.text.strip() for cell in cells]
                rows.append(row)

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=headers)
        df = df.dropna(how='all')  # Drop rows that are completely empty
        return df

    def scrape_yield_table(self):
        html = self.fetch_data()
        df = self.parse_data(html)
        return df


def getInitialCurve(Maturities):

    # Initilaize oject
    bs = BondScraper(country = 'united-states')

    # scrape data
    yield_data = bs.scrape_yield_table()

    # Process data
    data = yield_data.iloc[:, 1:3].copy()
    data.columns = ['Maturity', 'Yield']
    data.dropna(inplace=True)
    data['Maturity'] = data['Maturity'].apply(hp.maturity_to_years)
    data['Yield'] = data['Yield'].apply(lambda x: float(x.replace('%', ''))/100)

    # initialize curve model
    time = np.array(data.Maturity.tolist())
    rate = np.array(data.Yield.tolist())
    curve = Curve(rt=rate,t=time)

    # initilize nelson siegel model
    ns = NelsonSiegel(0.3,0.4,12,1)
    ns.calibrate(curve)

bondPrices =  ns.df_t([1,2])