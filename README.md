# Fantasy Football project using [Sports Reference API](https://pypi.org/project/sportsreference/)

Since this project is still in early stages this README is mostly just for notes of my own at the moment

## Helpful Links

* [Pro Football Reference Glossary](https://www.pro-football-reference.com/about/glossary.htm)
* [Sportsipy](https://github.com/roclark/sportsipy)
* [NFL Stadiums/Teams dataset](https://www.kaggle.com/tobycrabtree/nfl-scores-and-betting-data)

## Current Objectives

* Continue data validation
* Setup Relational Database system with the current dataframes
* Start with some simple machine learning models training to predict the over/under

----------------------------

## Data Notes

* Dates are all in `Eastern` time
* All columns are lower-case and have underscores instead of spaces --> `team_abbreviation`

## Known Issues (Backburner)

* API does not account for players traded during a season (See the EDA workbook for more clear examples)
  * Correcting the `age` column for this by using the [.fillna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html) method in Pandas, this works because the row above has their age at the beginning of that season.

## Future (lofty) Goals

* Get weather report as function for upcoming games during season
  * [Open Weather Map](https://openweathermap.org/history)
* [ESPN API](http://www.espn.com/apis/devcenter/docs/) for things like images and rankings etc.
  * Could possibly get from Reddit API

----------------------------

## Data Structure

### df_boxscores
Each row is a particular games boxscore with stats from both teams along with additional data regarding the particular game

* **Primary Key**: `game_uri` *Is set as the index*. Example --> '200009030min'
* **Foriegn Key(s)**: `year`, `month`, `day_of_week`

### nfl_player_stats_by_career
Each row is 1 particular player that has played in the NFL within the last 20 years (if no stat exists for a column it is filled with a NaN value)

* **Primary Key**: `player_id`
* **Foriegn Key(s)**: `team_abbreviation`, `name` (of player)

### nfl_player_stats_by_season
Each row is 1 particular player during a particular season within the last 20 years (if no stat exists for a column it is filled with a NaN value)

* **Primary Key**: `player_id`
* **Foriegn Key(s)**: `team_abbreviation`, `year`, `name` (of player)

### player_game_stats
**Index**: Shows `year`, `game_uri` (*string that is a **primary key** for a particular NFL game played during that year*), `team_abbreviation`, `name` (*Players name*)
**Rows**: Each row is 1 particular player that has played in the NFL within the last 20 years.

* **Primary Key**: `game_uri`
* **Foriegn Key(s)**: `team_abbreviation`, `year`, `name` (of player)

### team_season_stats
Each row is 1 particular team throughout 1 particular year in the NFL within the last 20 years.

* **Primary Key**: `team_abbreviation`
* **Foriegn Key(s)**: `year`