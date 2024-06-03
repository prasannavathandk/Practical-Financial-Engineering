from PyCurve.curve import Curve
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
