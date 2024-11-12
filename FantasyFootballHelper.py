import csv
import pandas as pd

def read_csv_data(filepath):
    """
    This function reads a .csv file and returns a structured format containing relevant data.

    Parameters:
    - filepath (str): The file path to the .csv file containing fantasy football data.

    Returns:
    - pd.DataFrame: A pandas structured format containing the loaded data from the .csv file.
    """

    pass


class Team:

    """
    A class to represent an NFL team and track its statistics such as offense, defense, 
    and win/loss performance over time.

    Attributes:
    - team_name (str): team name
    - wins (int): total wins
    - losses (int): total losses
    - points_for (list of float): weekly points for
    - points_against (list of float): weekly points allowed
    - total_offense (list of float): offensive production for a week
    - total_defense (list of float): defensive production for a week
    """
    
    def __init__(self, team_name):   
        self.team_name = team_name
        self.wins = 0
        self.losses = 0
        self.points_for = []
        self.points_against = []
        self.total_offense = []
        self.total_defense = []
    
    def weekly_calculate_offensive_production():
        """
        This function takes the data from the read_csv_data function and applies a formula to calculate offensive production for one nfl week.

        Parameters:
        - values from the previous formula TBD which exact ones once we get the .csv finalized

        Returns:
        - offensive_production (float)
            
        uses this formula:
        (Team Points For) + (Team Points For * Wins/(Wins+Losses)) + (Team Points For - NFL Points Median for the week)
        """
        
        pass

    def weekly_calculate_defensive_production():
        """
        This function takes the data from the read_csv_data function and applies a formula to calculate defensive production for one nfl week.

        Parameters:
        - values from the previous formula TBD which exact ones once we get the .csv finalized

        Returns:
        - defensive_production (float)
        
        uses this formula:
        (Team Points Against) + (Team Points Against * Wins/(Wins+Losses)) + (Team Points Against - NFL Points Median for the week)
        """
        
        pass


    def weekly_calculate_net_production(offensive, defensive):
        """
        This function takes the offensive_production and defensive_production and returns a net score

        Parameters:
        - offensive
        - defensive

        Returns:
        - defensive_production (float)
        
        uses this formula:
        net_production = offensive + defensive
        """
        
        pass


    def cumulative_seasonal_production(weekly_productions):
        """
        This function takes a teams weekly net production to generate a seasonal score.

        Parameters:
        - weekly_productions (list of dict): A list where each element contains a dictionary of weekly stats for a team, including offensive and defensive production across several weeks.

        Returns:
        - cumulative_performance (float): The total performance over the season
        """
        
        pass


