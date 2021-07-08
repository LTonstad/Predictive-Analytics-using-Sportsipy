# Fantasy Football project using [Sports Reference API](https://pypi.org/project/sportsreference/)

Since this project is still in early stages this README is mostly just for notes of my own at the moment

## Helpful Links

* [Pro Football Reference Glossary](https://www.pro-football-reference.com/about/glossary.htm)

## Current Objectives

* Data Cleaning, creating functions to seperate poisitons and minimize included features based on the positions
  * May be helpful to identify certain features that are going to be important to sort by
* Doesn't appear to be a way to get current seasons schedule, only allows for schedule of already played seasons
* Need to get a DataFrame of all boxcores for each team throughout the last 10 years

## Current Solvable Issues

* Many players have no position listed, need to create functions that fill those positions
  * ~~Main issues include `kickers` and `punters`~~
  * Still 14,111 players without positions

## Data Notes

* Dates are all in `Eastern` time

## Known Issues (Backburner)

* API does not account for players traded during a season (See the EDA workbook for more clear examples)
  * Correcting the `age` column for this by using the [.fillna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html) method in Pandas, this works because the row above has their age at the beginning of that season.

## Future (lofty) Goals

* Get weather report as function for upcoming games during season
* Get coach dataframes and factor those into algorythim
  * [Open Weather Map](https://openweathermap.org/history)
  
    > * Need to find a way to get start times of games, also end times of the games (BoxScore Dataframe has duration of game)
    > * 

* [ESPN API](http://www.espn.com/apis/devcenter/docs/) for things like images and rankings etc.
  * Could possibly get from Reddit API

## Getting Player Dataframes

* Goals:
  > * Use multi-indexing for identifying characteristics like `Name`, `Position`, `Team`, `Player_id`, `Current_age`
  > * Figure out a way to identify if player is starter, 2nd string etc.
  > * Figure out a way to project injury proneness
  > * Create offensive/defensive player column
  > * Players `height` may want to be in inches, then have function to convert back for visibility

* Player Columns:

Columns `highlighted` below are read in as `float64` datatypes but to be switched to `int64` (Will modify `get_data.py` after filling `NaN` values with 0 and changing dtypes to `int64`)
**Bold** columns are in the index of DataFrame

`adjusted_net_yards_per_attempt_index` 6
adjusted_net_yards_per_pass_attempt
adjusted_yards_per_attempt
`adjusted_yards_per_attempt_index` 9
`all_purpose_yards` 10
`approximate_value` 11
`assists_on_tackles` 12
`attempted_passes` 13
birth_date
`blocked_punts` 15
catch_percentage
`completed_passes` 17
`completion_percentage_index` 18
espn_qbr
extra_point_percentage
`extra_points_attempted` 21
`extra_points_made` 22
field_goal_percentage
field_goals_attempted
`field_goals_made` 25
`fifty_plus_yard_field_goal_attempts` 26
`fifty_plus_yard_field_goals_made` 27
`fourth_quarter_comebacks` 28
`fourty_to_fourty_nine_yard_field_goal_attempts` 29
`fourty_to_fourty_nine_yard_field_goals_made` 30
`fumbles` 31
`fumbles_forced` 32
`fumbles_recovered` 33
`fumbles_recovered_for_touchdown` 34    This column is messed up...Renamed to `fumbles_return_yards`
`game_winning_drives` 35
`games` 36
`games_started`
height
interception_percentage
`interception_percentage_index` 40 [See PFR''s Glossary](https://www.pro-football-reference.com/about/glossary.htm), essentially 100 is average, above is better & below is worse
`interceptions` 41 
`interceptions_returned_for_touchdown` 42
`interceptions_thrown` 43
`kickoff_return_touchdown` 44
`kickoff_return_yards` 45
`kickoff_returns` 46
`less_than_nineteen_yards_field_goal_attempts` 47
`less_than_nineteen_yards_field_goals_made` 48
`longest_field_goal_made` 49
`longest_interception_return` 50
`longest_kickoff_return` 51
`longest_pass` 52
`longest_punt` 53
`longest_punt_return` 54
`longest_reception` 55
`longest_rush` 56
**name**
`net_yards_per_attempt_index` 57
net_yards_per_pass_attempt
`passer_rating_index` 59
`passes_defended` 60
passing_completion
passing_touchdown_percentage
passing_touchdowns
passing_yards
passing_yards_per_attempt
player_id
position
punt_return_touchdown
punt_return_yards
punt_returns
punts
qb_record
quarterback_rating
receiving_touchdowns
receiving_yards
receiving_yards_per_game
receiving_yards_per_reception
receptions
receptions_per_game
rush_attempts
rush_attempts_per_game
rush_touchdowns
rush_yards
rush_yards_per_attempt
rush_yards_per_game
rushing_and_receiving_touchdowns
sack_percentage
sack_percentage_index
sacks
safeties
season
tackles
team_abbreviation
thirty_to_thirty_nine_yard_field_goal_attempts
thirty_to_thirty_nine_yard_field_goals_made
times_pass_target
times_sacked
total_punt_yards
touchdown_percentage_index
touches
twenty_to_twenty_nine_yard_field_goal_attempts
twenty_to_twenty_nine_yard_field_goals_made
weight
yards_from_scrimmage
yards_lost_to_sacks
yards_per_attempt_index
yards_per_completed_pass
yards_per_game_played
yards_per_kickoff_return
yards_per_punt
yards_per_punt_return
yards_per_touch
yards_recovered_from_fumble
yards_returned_from_interception


## Getting Game Boxscore information

* Boxscore Format:
  * `{Year}{month}{date}{0}{Team_Abbreviation}`
  * Example: `202101240gnb`

* Goals:
  > * Use multi-indexing for identifying characteristics like Name, `Date`, `Stadium`, `Winning_name`, `Losing_name`

* DataFrame Columns:

```
['attendance', 'away_first_downs', 'away_fourth_down_attempts',
'away_fourth_down_conversions', 'away_fumbles', 'away_fumbles_lost',
'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts',
'away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards',
'away_penalties', 'away_points', 'away_rush_attempts',
'away_rush_touchdowns', 'away_rush_yards', 'away_third_down_attempts',
'away_third_down_conversions', 'away_time_of_possession',
'away_times_sacked', 'away_total_yards', 'away_turnovers',
'away_yards_from_penalties', 'away_yards_lost_from_sacks', 'date',
'duration', 'home_first_downs', 'home_fourth_down_attempts',
'home_fourth_down_conversions', 'home_fumbles', 'home_fumbles_lost',
'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts',
'home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards',
'home_penalties', 'home_points', 'home_rush_attempts',
'home_rush_touchdowns', 'home_rush_yards', 'home_third_down_attempts',
'home_third_down_conversions', 'home_time_of_possession',
'home_times_sacked', 'home_total_yards', 'home_turnovers',
'home_yards_from_penalties', 'home_yards_lost_from_sacks',
'losing_abbr', 'losing_name', 'stadium', 'time', 'winner',
'winning_abbr', 'winning_name']
```

## Schedule Information

* Getting schedule DataFrame example:

```python
sched = Schedule('GNB', 2020)
sched_df = sched.dataframe
```

* Goals:
    > * Get schedule for current season in order to make predictions

* Dataframe Columns:

```
boxscore_index
date
datetime
day
extra_points_attempted
extra_points_made
field_goals_attempted
field_goals_made
fourth_down_attempts
fourth_down_conversions
interceptions
location
opponent_abbr
opponent_name
overtime
pass_attempts
pass_completion_rate
pass_completions
pass_touchdowns
pass_yards
pass_yards_per_attempt
points_allowed
points_scored
punt_yards
punts
quarterback_rating
result
rush_attempts
rush_touchdowns
rush_yards
rush_yards_per_attempt
third_down_attempts
third_down_conversions
time_of_possession
times_sacked
type
week
yards_lost_from_sacks
```

## Roster Information

* Getting a teams players example (Gives --> player_id[`key`] & name[`value`] as a dictionary):

```python
green_bay = Roster('GNB', year=2020, slim=True)
gnb_players = green_bay.players

'AdamDa01': 'Davante Adams'
```

