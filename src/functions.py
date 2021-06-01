import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

from sportsreference.nfl.boxscore import Boxscore, AbstractPlayer
from sportsreference.nfl.roster import Player, Roster
from sportsreference.nfl.schedule import Schedule
from sportsreference.nfl.teams import Teams

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

# Numeric columns
numerics = []

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

