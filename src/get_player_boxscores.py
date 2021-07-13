import pandas as pd
from sportsipy.nfl.boxscore import Boxscore, Boxscores

# Function to get long list of boxscore strings to be used like Boxscore('string') for each game to get boxscores

boxscore_strings = []
end_week = 21

# Getting all strings for boxscores in a list to be iterated through
for year in range(2000, 2021):
    print(year)
    try:
        boxscores_dict = Boxscores(1, year, end_week=end_week).games
    except:
        print(f'For year {year} it did not find {end_week} weeks, pulling {end_week-1} instead')
        boxscores_dict = Boxscores(1, year, end_week=end_week-1).games

    for idx, val in enumerate(boxscores_dict.keys()):
        for game in range(len(boxscores_dict[val])):
            boxscore_strings.append(boxscores_dict[val][game]['boxscore'])

# Function to gather all boxscore strings into single dataframe

df_boxscore = Boxscore(boxscore_strings[0]).dataframe

for game in boxscore_strings:
    print(f'Spinning up {game}')
    
    try:
        boxscore = Boxscore(game).dataframe
        df_boxscore = df_boxscore.append(boxscore)
    except:
        print(f'DAWWWWW {game} did not get a boxscore')
        continue

# Adding additional columns

# String of full day of the week (Sunday, Monday, Thursday)
df_boxscore['day_of_week'] = df_boxscore['date'].str.split(expand=True)[0]
# Abbreviation of month as a string
df_boxscore['month'] = df_boxscore['date'].str.split(expand=True)[1]
# Adding year column
df_boxscore['year'] = df_boxscore['date'].str[-4:]
# Temperature as integer in Farenheight
df_boxscore['temperature'] = df_boxscore['weather'].str.split(',', expand=True)[0].str.split(expand=True)[0]
# Relative humidity as a percentage
df_boxscore['humidity'] = df_boxscore['weather'].str.split(',', expand=True)[1].str.split(expand=True)[2]
# Wind chill as integer
df_boxscore['wind_chill'] = df_boxscore['weather'].str.split(',', expand=True)[3].str.split(expand=True)[2]

# Wind in MPH, takes a few extra steps
df_boxscore['wind'] = df_boxscore['weather'].str.split(',', expand=True)[2]
# Converts any games played in a dome to 0, originally listed as NoneType
df_boxscore['wind'] = df_boxscore['wind'].apply(lambda x: 0 if x is None else x)
# Converts any games listed as 'no wind' to 0
df_boxscore['wind'] = df_boxscore['wind'].apply(lambda x: 0 if str(x)[-1:] == 'd' else x)
# Changing all values to the integers
df_boxscore['wind'] = df_boxscore['wind'].str.split(expand=True)[1].fillna(0).astype('int64')

df_boxscore.to_pickle('../data/df_boxscores.pkl')