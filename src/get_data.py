import numpy as np
import pandas as pd
from datetime import datetime
import requests
from dateutil.relativedelta import relativedelta
import sys

from sportsreference.nfl.boxscore import Boxscore, AbstractPlayer
from sportsreference.nfl.roster import Player, Roster
from sportsreference.nfl.schedule import Schedule
from sportsreference.nfl.teams import Teams

# helper function to get player age during each season.
def get_age(player_df):
    age_lst = []
    for year, bd in zip(player_df.index, player_df['birth_date']):
        if year[0] == "Career":
            age_lst.append(age_lst[-1])
        else:
            age_lst.append(int(float(year[0])) - int(float(bd[0:4])))
    return age_lst
    
# helper function to get year for each row and denote
# rows that contain career totals.
def get_year(ix):
    if ix[0] == "Career":
        return "Career"
    elif ix[0] == "1999-00":
        return "2000"
    else:
        return ix[0][0:2] + ix[0][-2:]

# Function to get player info from Player class object.def get_player_df(player):

def get_player_df(player):
    # get player df and add some extra info
    player_df = player.dataframe
    if player_df is None:
        print(f'Unable to find {player}')
        return None
    player_df['birth_date'] = player.birth_date
    player_df['player_id'] = player.player_id
    player_df['name'] = player.name
    player_df['year'] = [get_year(ix) for ix in player_df.index]
    player_df['id'] = [player_id + ' ' + year for player_id, year in zip(player_df['player_id'], player_df['year'])]
    player_df['age'] = get_age(player_df)
    player_df['years_played'] = [x for x in range(player_df.shape[0])]
    return player_df


# initialize a list of players that we have pulled data for
players_collected = []
season_df_init = 0
career_df_init = 0
season_df = 0
career_df = 0# iterate through years.
for year in range(2020, 1999, -1):
    print('\n' + str(year))
        
    # iterate through all teams in that year.
    for team in Teams(year = str(year)).dataframes.index:
        print('\n' + team + '\n')
        
        # iterate through every player on a team roster.
        for player_id in Roster(team, year = year,
                         slim = True).players.keys():
            
            # only pull player info if that player hasn't
            # been pulled already.
            if player_id not in players_collected:
                
                player = Player(player_id)
                player_info = get_player_df(player)
                player_seasons = player_info[
                                 player_info['year'] != "Career"]
                player_career = player_info[
                                player_info['year'] == "Career"]
                
                # create season_df if not initialized
                if not season_df_init:
                    season_df = player_seasons
                    season_df_init = 1
                
                # else concatenate to season_df
                else:
                    season_df = pd.concat([season_df,
                                   player_seasons], axis = 0)
                    
                if not career_df_init:
                    career_df = player_career
                    career_df_init = 1
                
                # else concatenate to career_df
                else:
                    career_df = pd.concat([career_df,
                                   player_career], axis = 0)
                
                # add player to players_collected
                players_collected.append(player_id)
                print(player.name)

season_df.to_csv('../data/nfl_player_stats_by_season.csv')
career_df.to_csv('../data/nfl_player_stats_by_career.csv')