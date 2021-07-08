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
    
# Removes Slashes that exist in position column
def remove_slash(series):
    modified_df = series.copy()
    for idx, pos in enumerate(series):
        if len(str(pos)) <= 0:
            continue
        elif str(pos)[0] == '/':
            modified_df[idx] = str(pos)[1:]
        else:
            modified_df[idx] = str(pos)
    return modified_df

# Function to find Nonetypes and update column to 0's as an int
def update_num_column(df, col):
    for idx, pos in enumerate(df[col]):
        if pos is None:
            print(idx, '    ', pos, '    ', type(pos), '    ', df[col][idx])
            df[col][idx] = np.nan
        
    df[col] = df[col].fillna(0)
    df[col] = df[col].astype('int64')

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

# For getting Boxscore data, converts date column to datetime and adds others for easy access

months = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

def modify_dates(boxscores_df):
    for idx, date in enumerate(boxscores_df['date']):
        # Creating list of date information
        date_lst = boxscores_df['date'][idx].split()

        if len(str(date_lst[2][:-1])) == 1:
            date = '0' + str(date_lst[2][:-1])
        else:
            date = str(date_lst[2][:-1])

        if boxscores_df['time'][idx][-2:] == 'pm':
            time = str(int(boxscores_df['time'][idx][:1]) + 12) + boxscores_df['time'][idx][2:-2]
        else:
            time = '0' + boxscores_df['time'][idx][:1] + boxscores_df['time'][idx][2:-2]

        # Creating new columns
        boxscores_df['day_of_week'][idx] = date_lst[0]
        boxscores_df['month'][idx] = date_lst[1]
        boxscores_df['day_of_month'][idx] = int(date)
        boxscores_df['year'][idx] = int(date_lst[3])

        boxscores_df['date'][idx] = str(date_lst[3]) + str(months[date_lst[1]]) + str(date) + time
    
    boxscores_df['date'] = pd.to_datetime(boxscores_df['date'], format='%Y%m%d%H%M')

    return boxscores_df



# Function to get player stats from individual games using the string of the boxscore uri
def get_player_game_boxscore(game_uris):
    for uri in game_uris:
        # Getting game boxscore
        boxscore = Boxscore(uri)
        df_box = boxscore.dataframe

        # Getting home player boxscores
        home_df = boxscore.home_players[0].dataframe

        for player in boxscore.home_players[1:]:
            home_df = pd.concat([home_df, player.dataframe], axis=0)

        home_df['away_abbreviation'] = boxscore.home_abbreviation.upper()
        home_df['game_uri'] = df_box.index[0]
        home_df['name'] = [x.name for x in boxscore.home_players]

        home_df.set_index(['game_uri', 'away_abbreviation', 'name'], inplace=True)

        # Getting away player boxscore
        away_df = boxscore.away_players[0].dataframe

        for player in boxscore.away_players[1:]:
            away_df = pd.concat([away_df, player.dataframe], axis=0)

        away_df['away_abbreviation'] = boxscore.away_abbreviation.upper()
        away_df['game_uri'] = df_box.index[0]
        away_df['name'] = [x.name for x in boxscore.away_players]

        away_df.set_index(['game_uri', 'away_abbreviation', 'name'], inplace=True)

        # Combining two dataframes
        game_df = pd.concat([home_df, away_df], axis=0)

        try:
            final_df = pd.concat([final_df, game_df], axis=0)
        except:
            final_df = game_df.copy()