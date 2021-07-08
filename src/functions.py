import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

from sportsreference.nfl.boxscore import Boxscore, AbstractPlayer
from sportsreference.nfl.roster import Player, Roster
from sportsreference.nfl.schedule import Schedule
from sportsreference.nfl.teams import Teams

import seaborn as sn
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Seperation of player positions
offensive_positions = ['WR', 'LT', 'RB', 'TE', 'C', 'RG', 'QB', 'RT', 'RT/T', 'LG', 'LG/T', 'FB',
                       'T', 'LT/T', 'TE', 'FB', 'G', 'G/LG', 'G/TE', 'G/RG', 'C/LG', 'HB', 'FB/TE',
                      'C/RG', 'G/LT']
defensive_positions = ['LCB', 'SS', 'FS', 'RILB', 'RLB', 'MLB', 'NT', 'LDT', 'RDT', 'DT/LDT', 
                       'RCB', 'RDE', 'LLB', 'LILB', 'LDE', 'LOLB', 'ROLB', 'DB', 'DE/RDE', 'DT/LOLB', 
                       'IL', 'CB/RCB', 'CB/LCB', 'DE/LDE', 'DT', 'DE', 'DT', 'FS/SS', 'CB', 'LB', 
                       'CB/DB', 'DT/RDT', 'IL/LILB', 'IL/RILB', 'DE/LOLB', 'RDE/RDT', 'LDT/NT', 'DB/SS', 
                       'IL/RLB', 'DB/FS', 'OLB', 'DT/RDE', 'DE/RDT', 'ML/MLB', 'LILB/ML', 'DT/LDE', 'NT/RDT',
                      'S', 'ILB']
special_teams_positions = ['K', 'P']
no_position = ['nan', '']

# Features of offense, defense and special teams
offensive_features = ['name', 'player_id', 'position', 'team_abbreviation',
       'age', 'year', 'adjusted_net_yards_per_attempt_index',
       'adjusted_net_yards_per_pass_attempt',
       'adjusted_yards_per_attempt', 'adjusted_yards_per_attempt_index',
       'all_purpose_yards', 'approximate_value',
       'attempted_passes', 'birth_date',
       'catch_percentage', 'completed_passes',
       'completion_percentage_index', 'espn_qbr', 'fourth_quarter_comebacks', 'fumbles',
       'game_winning_drives', 'games', 'games_started', 'height',
       'interception_percentage', 'interception_percentage_index',
       'interceptions_thrown', 'longest_pass', 'longest_reception', 'longest_rush',
       'net_yards_per_attempt_index', 'net_yards_per_pass_attempt',
       'passer_rating_index', 'passing_completion',
       'passing_touchdown_percentage', 'passing_touchdowns',
       'passing_yards', 'passing_yards_per_attempt',
       'qb_record', 'quarterback_rating', 'receiving_touchdowns',
       'receiving_yards', 'receiving_yards_per_game',
       'receiving_yards_per_reception', 'receptions',
       'receptions_per_game', 'rush_attempts', 'rush_attempts_per_game',
       'rush_touchdowns', 'rush_yards', 'rush_yards_per_attempt',
       'rush_yards_per_game', 'rushing_and_receiving_touchdowns',
       'season', 'times_pass_target',
       'times_sacked', 'touchdown_percentage_index',
       'touches', 'weight',
       'yards_from_scrimmage', 'yards_lost_to_sacks',
       'yards_per_attempt_index', 'yards_per_completed_pass',
       'yards_per_game_played', 'yards_per_touch', 'years_played']
defensive_features = ['index', 'name', 'player_id', 'position', 'team_abbreviation', 'age',
       'year', 'approximate_value', 'assists_on_tackles', 'birth_date', 'fumbles_forced',
       'fumbles_recovered', 'fumbles_return_yards', 'games', 'games_started',
       'height', 'interceptions', 'interceptions_returned_for_touchdown',
       'longest_interception_return', 'passes_defended', 'sacks',
       'season', 'tackles', 'weight', 'yards_recovered_from_fumble',
       'yards_returned_from_interception', 'years_played']
special_teams_features = ['index', 'name', 'player_id', 'position', 'team_abbreviation', 'age',
       'year', 'approximate_value', 'assists_on_tackles', 'birth_date', 'blocked_punts',
       'extra_point_percentage', 'extra_points_attempted', 'extra_points_made',
       'field_goal_percentage', 'field_goals_attempted', 'field_goals_made',
       'fifty_plus_yard_field_goal_attempts',
       'fifty_plus_yard_field_goals_made',
       'fourty_to_fourty_nine_yard_field_goal_attempts',
       'fourty_to_fourty_nine_yard_field_goals_made', 'games',
       'games_started', 'height',
       'less_than_nineteen_yards_field_goal_attempts',
       'less_than_nineteen_yards_field_goals_made', 'longest_field_goal_made', 'longest_punt',
       'longest_punt_return', 'punt_return_touchdown', 'punt_return_yards', 'punt_returns',
       'punts', 'total_punt_yards',  'season',
       'thirty_to_thirty_nine_yard_field_goal_attempts',
       'thirty_to_thirty_nine_yard_field_goals_made',
       'twenty_to_twenty_nine_yard_field_goal_attempts',
       'twenty_to_twenty_nine_yard_field_goals_made', 'weight',
       'yards_recovered_from_fumble', 'years_played']