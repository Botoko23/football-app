
import os
import datetime

import ssl
import urllib.request
import pandas as pd
import certifi


class Scraper:
    def __init__(self, comp_code: str, comp: str, season:str) -> pd.DataFrame:
        self.comp_code = comp_code
        self.comp = comp
        self.season = season
    
    @property
    def season_code(self) -> int:
        today = datetime.datetime.now()
        year = int(self.season.split("-")[-1])
        if year < today.year:
            # previous season
            return 0
        elif year == today.year:
            # current season
            return 1     
    
    def get_fixtures(self) -> None:
        url = f"https://fbref.com/en/comps/{self.comp_code}/{self.season}/schedule/{self.season}-{self.comp}-Scores-and-Fixtures"
        if self.season_code:
            url = f"https://fbref.com/en/comps/{self.comp_code}/schedule/{self.comp}-Scores-and-Fixtures"
           
        # Get DataFrame from HTML table
        # Specify the path to the certificate bundle (certifi.where() provides the default bundle path)
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Use the ssl_context in your HTTPS request
        response = urllib.request.urlopen(url, context=ssl_context)
        result = pd.read_html(response.read())[0]
        df = pd.DataFrame(result)

        # Extract relevant columns and drop duplicates and rows with missing values
        df = df.loc[:, ["Wk", "Date", "Home", "Away", "Score"]]  # Select relevant columns
        df = df[df.isnull().any(axis=1) == False]  # Drop rows with missing values
        df.to_csv("/tmp/FixtureDates.csv", index=False)
        return df['Home'].unique()


if __name__=="__main__":
    pass
    # scraper = Scraper("9", "Premier-League", "2022-2023")
    # clubs, dates = scraper.get_fixtures()
    # print(clubs)
