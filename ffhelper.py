import pandas as pd
import math

class Team:
    def __init__(self, name, offense_stats, defense_stats):
        """
        Initialize a team instance.

        name: Name of the team.
        offense_stats: A dictionary containing the team's offensive production
        defense_stats: A dictionary containing the team's defensive production
        """
        self.name = name

        #offense stats
        self.games_played = offense_stats.get("GP", 0)
        self.points_per_game = offense_stats.get("PTS", 0)
        self.total_offense_production = offense_stats.get("All", 0)
        self.plays_per_game = offense_stats.get("Run", 0) + offense_stats.get("Pass", 0)
        self.team_efficiency = self.total_offense_production / self.plays_per_game

        #defense stats
        self.points_allowed_per_game = defense_stats.get("PA", 0)
        self.total_defense_production = defense_stats.get("DEF", 0)
        self.offensive_production_allowed = defense_stats.get("QB", 0) + defense_stats.get("RB", 0) + defense_stats.get("WR", 0) + defense_stats.get("TE", 0)
        
        #wins losses ties
        self.current_wins = 0
        self.current_losses = 0
        self.current_ties = 0
        
    def expected_points_for(self):
        """
        Calculate the expected points scored by the team based on their offensive production
        """
        return self.points_per_game * self.team_efficiency
        
    def calculate_net_production(self):
        """
        Calculate the team's net production using an original formula
        """
        return round( ((self.points_per_game - self.points_allowed_per_game) + (self.total_offense_production - self.total_defense_production)/self.team_efficiency) , 4)


    def __repr__(self):
        """
        Return a string representation of the team's data
        """
        return (f"Team: {self.name}, Games Played: {self.games_played}\n"
                f"Offense - Points Per Game: {self.points_per_game}, Total Offensive Production: {self.total_offense_production}, Plays Per Game: {self.plays_per_game}, Team Efficiency: {round(self.team_efficiency, 3)}\n"
                f"Defense - Points Allowed Per Game: {self.points_allowed_per_game}, Total Defensive Production: {self.total_defense_production}, Offensive Production Allowed to Opponents: {round(self.offensive_production_allowed, 2)}\n"
                f"Net Production: {self.calculate_net_production()}")
        
    def update_record(self, result):
        """
        Update the team's record based on a game result
        """
        if result == "win":
            self.current_wins += 1
        elif result == "loss":
            self.current_losses += 1
        elif result == "tie":
            self.current_ties += 1
            
            

            
def create_teams(offense_file, defense_file):
    """
    Create a dictionary of teams using offense and defense data from CSV files

    offense_file: Path to the Fantasy Offense Stats CSV file
    defense_file: Path to the Fantasy Defense Stats CSV file
    
    return A dictionary where the keys are team names and the values are Team instances
    """
    #read CSV files
    offense_df = pd.read_csv(offense_file)
    defense_df = pd.read_csv(defense_file)

    #create a dictionary of teams
    teams = {}
    for i, offense_row in offense_df.iterrows():
        team_name = offense_row["Name"]

        #find the matching defense row for the same team
        defense_row = defense_df[defense_df["Name"] == team_name].iloc[0].to_dict()

        #convert offense row to dictionary
        offense_stats = offense_row.to_dict()

        #create and store the team object
        teams[team_name] = Team(team_name, offense_stats, defense_row)

    return teams



def simulate_game(team1, team2):
    """
    Simulate a game between two teams and determine the winner

    team1: The first team instance
    team2: The second team instance
    
    return winner (Team object), loser (Team object), and outcome ('win1'/'win2'/'tie').
    """
    #use team efficiency and net production to determine the winner
    team1_score = team1.team_efficiency + (team1.calculate_net_production() - team2.offensive_production_allowed)
    team2_score = team2.team_efficiency + (team2.calculate_net_production() - team1.offensive_production_allowed)

    if team1_score > team2_score:
        return team1, team2, "win1"
    elif team2_score > team1_score:
        return team2, team1, "win2"
    else:
        return None, None, "tie"
    
def simulate_season(schedule_file, teams):
    """
    Simulate an NFL season based on the schedule csv and update team records

    schedule_file: path to the schedule CSV file.
    teams: dictionary containing Team instances indexed by team names.
    """
    schedule = pd.read_csv(schedule_file)

    results = []
    for _, game in schedule.iterrows():
        week = game["Week"]
        team1_name = game["Team1"]
        team2_name = game["Team2"]

        #get the team objects
        team1 = teams[team1_name]
        team2 = teams[team2_name]

        #simulate the game
        winner, loser, outcome = simulate_game(team1, team2)

        #ppdate records based on the outcome
        if outcome == "win1":
            team1.update_record("win")
            team2.update_record("loss")
            results.append(f"Week {week}: {team1_name} defeat {team2_name}.")
        elif outcome == "win2":
            team2.update_record("win")
            team1.update_record("loss")
            results.append(f"Week {week}: {team2_name} defeat {team1_name}.")
        elif outcome == "tie":
            team1.update_record("tie")
            team2.update_record("tie")
            results.append(f"Week {week}: {team1_name} ties with {team2_name}.")

    return results


def print_team_records(teams):
    """
    Print the final records of all teams.

    teams: dict containing Team instances
    """
    for team_name, team in teams.items():
        print(f"{team.name} - Wins: {team.current_wins}, Losses: {team.current_losses}, Ties: {team.current_ties}")


if __name__ == "__main__":
    offense_file = "2023 Fantasy Offense Stats.csv"
    defense_file = "2023 Fantasy Defense Stats.csv"
    schedule_file = "2023 Schedule.csv"

    #create the teams
    teams = create_teams(offense_file, defense_file)

    #simulate the season
    season_results = simulate_season(schedule_file, teams)
    
    #print individual team stats
    for team_name, team in teams.items():
        print(team)
        print("")

    #print the results of each matchup
    print("\nGame Results:")
    for result in season_results:
        print(result)

    #print final team records
    print("\nFinal Team Records:")
    print_team_records(teams)