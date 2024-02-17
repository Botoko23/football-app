import pandas as pd
import numpy as np



class MethodNotCalledError(Exception):
    pass

class StatsExtractor:
    def __init__(self, club:str):
        self._df  = pd.read_csv("/tmp/FixtureDates.csv") # Read the CSV file
        self._club = club # Store the club name

        self._df_unique_date = self._df.drop_duplicates('Date', inplace=False)[['Date', 'Wk']].set_index('Date')
    
    @property
    def is_prepare_df_called(self) -> bool:
        if'IsHome' in self._df.columns and 'Home_Goals' in self._df.columns and 'Away_Goals' in self._df.columns:
            return True
        return False   
    
    @property
    def is_calculate_gd_and_points_called(self) -> bool:
        if 'GD' in self._df.columns and 'Points' in self._df.columns:
            return True
        return False   

    #spread the stats over all unqiue dates after get df of goals, pts or gds
    def _join_helper(self, *stats,  df:pd.DataFrame):
        result = []
        for stat in stats:
            result.append(self._df_unique_date.join(df.set_index("Date"), how='outer').groupby('Wk').sum()[stat])
            # result.append(np.nan_to_num(self._df_unique_date.join(df.set_index("Date"), how='outer')[stat]))
        return result
    
    def prepare_df(self):
        # Filter the dataframe to include only matches where the club is playing
        self._df = self._df[(self._df['Home'] == self._club) | (self._df['Away'] == self._club)]
        # Add a column to indicate whether the club is playing at home or away
        self._df['IsHome'] = np.where(self._df['Home'] == self._club, 1, -1)
        # Split the Score column into Home Goals and Away Goals columns
        self._df[['Home_Goals', 'Away_Goals']] = self._df['Score'].str.split('–', expand=True).astype(int)

    def calculate_gd_and_points(self) -> list:  
        #check if prepare_df is already called
        if not self.is_prepare_df_called:
            raise MethodNotCalledError("You should call method prepare_df beforehand")
        elif self.is_prepare_df_called:
            # Calculate the goal difference for each match and store it in a new column
            self._df['GD'] = self._df['Home_Goals'] - self._df['Away_Goals']
            self._df['GD'] = self._df['GD'] * self._df['IsHome']
            # Calculate the number of points earned by the club in each match based on the goal difference
            self._df['Points'] = np.select(
                [self._df['GD'] > 0, self._df['GD'] == 0, self._df['GD'] < 0],
                [3, 1, 0],
                default=np.nan
            )
            gd_pts_df =  self._df.loc[:, ["Date", "GD", "Points"]]
            gd, pts = self._join_helper('GD', 'Points', df=gd_pts_df)
            # pts = self._join_helper(df=gd_pts_df, stats="Points")
            return gd, pts      

    def get_all_goals(self) -> list:
        #check if prepare_df is already called
        if not self.is_prepare_df_called and not self.is_calculate_gd_and_points_called:
            raise MethodNotCalledError("You should call both prepare_df and calculate_gd_and_points beforehand")
        elif self.is_prepare_df_called:
            # Return a dataframe of all goals scored by the club, sorted by date
            home_goals = self._df.loc[self._df['IsHome'] == 1, ['Home_Goals', 'Date']].rename(columns={'Home_Goals': 'Goals'})
            away_goals = self._df.loc[self._df['IsHome'] == -1, ['Away_Goals', 'Date']].rename(columns={'Away_Goals': 'Goals'})
            goals = pd.concat([home_goals, away_goals]).sort_values('Date')
            return self._join_helper("Goals", df=goals)[0]

    



if __name__ == "__main__":
    pass
    # cal = StatsExtractor('Arsenal')
    # cal.prepare_df()
    # res = cal.calculate_gd_and_points()
    # goals = cal.get_all_goals()
