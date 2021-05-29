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
        elif year[0] == '':
            age_lst.append(np.nan)
        else:
            age_lst.append(int(float(year[0])) - int(float(bd[0:4])))
    return age_lst
    

# Function to get player info from Player class object.def get_player_df(player):
def get_player_df(player):
    # get player df and verify that a DataFrame was actually created, if not return None
    player_df = player.dataframe
    if player_df is None:
        print(f'Unable to find {player}')
        return None
    
    # Getting extra information including age, years_played
    player_df['age'] = get_age(player_df)
    player_df['years_played'] = [x for x in range(player_df.shape[0])]

    # Modifying column to verify that all positions are listed in upper case letters
    player_df['position'] = player_df['position'].str.upper()

    # Resetting index in preperation for returning career and season DataFrames
    player_df = player_df.reset_index()
    player_df.rename(columns={'level_0':'year'},inplace=True)

    # Creating two DataFrames, one for season by season stats, one for career stats
    career = player_df[player_df['year'] == 'Career']
    seasons = player_df[player_df['year'] != 'Career']

    # Adding lists of different positions & teams played for to the Career row for the career DF
    positions = list(filter(None, list(player_df['position'].unique())))
    if len(positions) > 1:
        career['position'] = ' '.join(positions)
    elif len(positions) == 0:
        career['position'] = np.nan
    else:
        career['position'] = positions[0]
        
    team_abbreviations = list(filter(None, list(player_df['team_abbreviation'].unique())))
    if len(team_abbreviations) > 1:
        career['team_abbreviation'] = ' '.join(team_abbreviations)
    elif len(positions) == 0:
        career['position'] = np.nan
    else:
        career['team_abbreviation'] = team_abbreviations[0]

    # Setting up DataFrame to have Multi-Index so that manipulating DataFrame doesn't get rid of a columns unique identifiers
    seasons.set_index(['name', 'player_id', 'position', 'team_abbreviation', 'age', 'year'], inplace=True)
    career.set_index(['name', 'player_id', 'position', 'team_abbreviation', 'age', 'year'], inplace=True)
    
    return seasons, career


''' # initialize a list of players that we have pulled data for
players_collected = []
season_df_init = 0
career_df_init = 0
season_df = 0
career_df = 0 
empty_player_df = []

# iterate through years.
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

                # Check to verify that the DataFrame exists, else move to next player
                if player.dataframe is None:
                    empty_player_df.append(player_id)
                    continue

                # Getting season & career dataframes
                player_seasons, player_career = get_player_df(player)
                
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

season_df.to_pickle('../data/nfl_player_stats_by_season.pkl')
career_df.to_pickle('../data/nfl_player_stats_by_career.pkl') '''