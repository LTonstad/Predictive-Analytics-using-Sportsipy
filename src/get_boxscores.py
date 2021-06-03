from get_data import *

boxscores_df_init = 0
boxscores_df = 0

# iterate through years.
for year in range(2020, 2019, -1):
    print('\n', str(year))
        
    # iterate through all teams in that year.
    for team in Teams(year = str(year)).dataframes.index:
        print('\n', team, '\n')

        # Getting all boxscores for the Team
        for boxscore in Schedule(team, int(year)):

            # Checking if boxscore_df is created already
            if not boxscores_df_init:
                boxscores_df = boxscore.dataframe_extended
                boxscores_df_init = 1

            else:
                boxscores_df = pd.concat([boxscores_df, boxscore.dataframe_extended], axis = 0)

# Creating new columns
boxscores_df['day_of_week'] = ''
boxscores_df['month'] = ''
boxscores_df['day_of_month'] = np.nan
boxscores_df['year'] = np.nan

boxscores_df = modify_dates(boxscores_df)

boxscores_df = boxscores_df.set_index(['date', 'losing_abbr', 'losing_name', 'stadium', 'time', 'winner',
'winning_abbr', 'winning_name'])

boxscores_df.to_pickle('../data/boxscores_df.pkl')