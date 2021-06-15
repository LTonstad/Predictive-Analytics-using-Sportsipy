import pandas as pd
from sportsipy.nfl.boxscore import Boxscore, BoxscorePlayer, Boxscores

boxscore_strings = []

# Getting all strings for boxscores in a list to be iterated through
for year in range(2000, 2021):
    boxscores_dict = Boxscores(1, 2020, end_week=21).games

    for idx, val in enumerate(boxscores_dict.keys()):
        for game in range(len(boxscores_dict[val])):
            boxscore_strings.append(boxscores_dict[val][game]['boxscore'])