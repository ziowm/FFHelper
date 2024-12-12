import unittest
from FFHelper import Team, reset_all_teams, get_weather, simulate_game

class Test(unittest.TestCase):

    def setUp(self):
        """
        Set up a Team object for testing
        """
        #Miami Dolphins stats for consistency with CSV file
        self.offense_stats = {
            "GP": 17,
            "PTS": 29.2,
            "All": 81.1,
            "Run": 26.8,
            "Pass": 35.1
        }
        self.defense_stats = {
            "PA": 23.0,
            "DEF": 9.2,
            "QB": 18.1,
            "RB": 17.3,
            "WR": 29.0,
            "TE": 10.6
        }
        #Miami Dolphins team
        self.team = Team("Miami Dolphins", self.offense_stats, self.defense_stats)

    def test_init(self):
        """
        Test init method and see if team attributes are initialized and set correctly
        """
        #check if team name is Miami Dolphins
        self.assertEqual(self.team.name, "Miami Dolphins")
        #check if there are 17 games played
        self.assertEqual(self.team.games_played, 17)
        #check if team attributes match to the CSV file and have been read properly
        self.assertEqual(self.team.team_efficiency, self.offense_stats["All"] / (self.offense_stats["Run"] + self.offense_stats["Pass"]))
        self.assertEqual(self.team.points_allowed_per_game, self.defense_stats["PA"])
        self.assertEqual(self.team.offensive_production_allowed, sum([self.defense_stats["QB"], self.defense_stats["RB"], self.defense_stats["WR"], self.defense_stats["TE"]]))

    def test_calculate_expected_wins(self):
        """
        Test calculate_expected_wins and see if correct values are given
        """
        #call calculate_expected_wins and perform calculations
        self.team.calculate_expected_wins()
        expected_x_off = 0.19 * self.offense_stats["All"] + 12
        expected_x_def = -1.24 * self.defense_stats["DEF"] + 30.8
        net_points = expected_x_off - expected_x_def
        expected_x_wins = 0.418 * net_points + 8.5
        
        #check if the calculations match to the correct values
        self.assertEqual(self.team.x_off, expected_x_off)
        self.assertEqual(self.team.x_def, expected_x_def)
        self.assertEqual(self.team.x_wins, expected_x_wins)
        
    def test_expected_points_for(self):
        """
        Test expected_points_for calculation of expected points based on offensive stats
        """
        #calculate expected points for and see if they match the correct value
        expected_points = self.offense_stats["PTS"] * self.team.team_efficiency
        self.assertAlmostEqual(self.team.expected_points_for(), expected_points)

    def test_calculate_net_production(self):
        """
        Test calculate_net_production calculation
        """
        #calculate net production and see if they match the correct value
        expected_net_production = round(self.team.off + self.team.de * 7.06)
        self.assertEqual(self.team.calculate_net_production(), expected_net_production)

    def test_update_record(self):
        """
        Test update_record updating the win/loss/tie records and resetting the win streak
        """
        #check if the update_record method works and see if it matches the correct team record and win streak
        self.team.update_record("win")
        self.assertEqual(self.team.current_wins, 1)
        self.assertEqual(self.team.win_streak, 1)

        #check if the winstreak gets reset in a loss
        self.team.update_record("loss")
        self.assertEqual(self.team.current_losses, 1)
        self.assertEqual(self.team.win_streak, 0)

        #check if the winstreak gets reset in a tie
        self.team.update_record("tie")
        self.assertEqual(self.team.current_ties, 1)
        self.assertEqual(self.team.win_streak, 0)

    def test_reset_record(self):
        """
        Test reset_record resetting all team records to zero after simulations so it can be ran again
        """
        #update the team record with 17 games played and 9 wins and 8 losses
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        self.team.update_record("loss")
        self.team.update_record("win")
        
        #check to see if team record got reset back to zero
        self.team.reset_record()
        self.assertEqual(self.team.current_wins, 0)
        self.assertEqual(self.team.current_losses, 0)
        self.assertEqual(self.team.current_ties, 0)
        self.assertEqual(self.team.win_streak, 0)

    def test_reset_all_teams(self):
        """
        Test reset_all_teams resetting the records of all teams in the dictionary
        """
        teams = {"Team 1": self.team, "Team 2": Team("Sample Team", self.offense_stats, self.defense_stats)}
        #make every team play a full 17 games and add 9 wins and 8 losses
        for team in teams.values():
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
            self.team.update_record("loss")
            self.team.update_record("win")
        #reset all team records to 0
        reset_all_teams(teams)
        for team in teams.values():
            #test if all values went back to 0 so simulation can be run again
            self.assertEqual(team.current_wins, 0)
            self.assertEqual(team.current_losses, 0)
            self.assertEqual(team.current_ties, 0)
            self.assertEqual(team.win_streak, 0)


    def test_get_weather(self):
        """
        Test get_weather.
        It tests to make sure that the random weather possibilities unique to each stadium are satisfied and being generated.
        It tests both indoor and outdoor stadiums.
        In this test we test 2 indoor stadiums: The Arizona Cardinals and The Houston Texans
        We also test 2 outdoor stadiums with very different weather patterns: The Green Bay Packers and the Miami Dolphins
        """       
        #testing indoor stadiums, so always clear weather
        weather = get_weather("Arizona Cardinals")
        self.assertEqual(weather, "Clear")
        weather = get_weather("Houston Texans")
        self.assertEqual(weather, "Clear")
        
        #testing outdoor stadiums
        weather_types = set()  #create a set for all 4 possible weather types for the Packers
        for _ in range(10000):  #run through a stadium weather 10000 times to get every weather possibility
            weather = get_weather("Green Bay Packers")
            weather_types.add(weather)
            #if all weather types are found break out of loop
            if weather_types == {"Clear", "Rain", "Snow", "Wind"}:
                break
        #test that all weather types were observed
        self.assertEqual(weather_types, {"Clear", "Rain", "Snow", "Wind"})
        
        weather_types = set()  #create a set for all 2 possible weather types for the Dolphins
        for _ in range(10000):  #run through a stadium weather 10000 times to get every weather possibility
            weather = get_weather("Miami Dolphins")
            weather_types.add(weather)
            #if all weather types are found break out of loop
            if weather_types == {"Clear", "Rain"}:
                break
        #test that all weather types were observed
        self.assertEqual(weather_types, {"Clear", "Rain"})
        

    def test_simulate_game(self):
        """
        Tests simulate_game by creating a second team and playing eachother
        """
        #New England Patriots stats for consistency with the CSV file
        team2_offense_stats = {
            "GP": 17,
            "PTS": 13.9,
            "All": 24.3,
            "Run": 24.4,
            "Pass": 35.6
        }
        team2_defense_stats = {
            "PA": 21.5,
            "DEF": 6.4,
            "QB": 15.2,
            "RB": 18.4,
            "WR": 26.4,
            "TE": 7.1
        }
        team2 = Team("New England Patriots", team2_offense_stats, team2_defense_stats)
        
        #calls simulate_game and checks if the outcome is team 1 win, team 2 win, or tie
        winner, loser, outcome = simulate_game(self.team, team2)
        self.assertIn(outcome, ["win1", "win2", "tie"])