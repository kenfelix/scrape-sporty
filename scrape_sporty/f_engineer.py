import pandas as pd
import numpy as np

# Attempt to read the CSV file
df = pd.read_csv("../Spain.csv")

# Convert Date to datetime for time-based features
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')

# 1. Match Date and Time Features
df['match_date'] = df['Date'].dt.date
df['match_time'] = df['Date'].dt.time
df['match_weekday'] = df['Date'].dt.day_name()
df['match_hour'] = df['Date'].dt.hour

# 2. Split Scores
df[['team_a_goals', 'team_b_goals']] = df['Score'].str.split(' : ', expand=True).astype(int)
df['total_goals'] = df['team_a_goals'] + df['team_b_goals']
df['goal_difference'] = abs(df['team_a_goals'] - df['team_b_goals'])

# 3. Match Outcome
df['match_outcome_team_a'] = np.where(df['team_a_goals'] > df['team_b_goals'], 'win', 
                                      np.where(df['team_a_goals'] < df['team_b_goals'], 'loss', 'draw'))
df['match_outcome_team_b'] = np.where(df['team_a_goals'] < df['team_b_goals'], 'win', 
                                      np.where(df['team_a_goals'] > df['team_b_goals'], 'loss', 'draw'))

# 4. Performance Metrics
df['is_clean_sheet_team_a'] = (df['team_b_goals'] == 0).astype(int)
df['is_clean_sheet_team_b'] = (df['team_a_goals'] == 0).astype(int)
df['is_high_scoring_game'] = (df['total_goals'] > 3).astype(int)
df['is_draw'] = (df['team_a_goals'] == df['team_b_goals']).astype(int)

# 5. Cumulative Points
df['points_team_a'] = np.where(df['match_outcome_team_a'] == 'win', 3, 
                               np.where(df['match_outcome_team_a'] == 'draw', 1, 0))
df['points_team_b'] = np.where(df['match_outcome_team_b'] == 'win', 3, 
                               np.where(df['match_outcome_team_b'] == 'draw', 1, 0))

df['cumulative_points_team_a'] = df.groupby('Team A')['points_team_a'].cumsum()
df['cumulative_points_team_b'] = df.groupby('Team B')['points_team_b'].cumsum()

# 6. Rolling Performance
df['team_a_goals_last_3'] = df.groupby('Team A')['team_a_goals'].apply(lambda x: x.rolling(3).mean())
df['team_b_goals_last_3'] = df.groupby('Team B')['team_b_goals'].apply(lambda x: x.rolling(3).mean())
df['team_a_wins_last_3'] = df.groupby('Team A')['match_outcome_team_a'].apply(lambda x: (x == 'win').rolling(3).sum())
df['team_b_wins_last_3'] = df.groupby('Team B')['match_outcome_team_b'].apply(lambda x: (x == 'win').rolling(3).sum())

# 7. Midweek or Weekend Game
df['is_midweek_game'] = df['match_weekday'].isin(['Tuesday', 'Wednesday', 'Thursday']).astype(int)

# 8. Winning Percentage
# Calculate cumulative wins for both teams
df['team_a_cumulative_wins'] = df.groupby('Team A')['match_outcome_team_a'].apply(lambda x: (x == 'win').cumsum())
df['team_b_cumulative_wins'] = df.groupby('Team B')['match_outcome_team_b'].apply(lambda x: (x == 'win').cumsum())

# Calculate cumulative games played for both teams
df['team_a_games_played'] = df.groupby('Team A').cumcount() + 1
df['team_b_games_played'] = df.groupby('Team B').cumcount() + 1

# Calculate Winning Percentage as cumulative wins divided by games played, then converted to a percentage
df['team_a_winning_percentage'] = (df['team_a_cumulative_wins'] / df['team_a_games_played']) * 100
df['team_b_winning_percentage'] = (df['team_b_cumulative_wins'] / df['team_b_games_played']) * 100

# Display the final dataset with all new features
df = df[['Game', 'League', 'League_Week', 'Event ID', 'Date', 'Team A', 'Team B', 'Score',
         'team_a_goals', 'team_b_goals', 'total_goals', 'goal_difference', 
         'match_outcome_team_a', 'match_outcome_team_b',
         'is_clean_sheet_team_a', 'is_clean_sheet_team_b', 'is_high_scoring_game', 'is_draw',
         'points_team_a', 'points_team_b', 'cumulative_points_team_a', 'cumulative_points_team_b',
         'team_a_goals_last_3', 'team_b_goals_last_3', 'team_a_wins_last_3', 'team_b_wins_last_3',
         'is_midweek_game', 'team_a_winning_percentage', 'team_b_winning_percentage']]

# Print the final DataFrame with all features
print(df)
