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

df_boxscore.to_pickle('../data/df_boxscores.pkl')