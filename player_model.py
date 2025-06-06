import pandas as pd
import numpy as np

# Load ball-by-ball data
ball_df = pd.read_csv('Ball_By_Ball_new.csv')

# =======================
# BATSMAN STATS
# =======================
batting = ball_df.groupby('Batsmen_ID').agg({
    'batsman_run': 'sum',
    'Match_ID': pd.Series.nunique,
    'ballnumber': 'count',
    'Batsmen': 'first',
    'isWicketDelivery': 'sum'
}).rename(columns={
    'batsman_run': 'Total_Runs',
    'Match_ID': 'Matches_Played',
    'ballnumber': 'Balls_Faced',
    'Batsmen': 'Player_Name',
    'isWicketDelivery': 'Outs'
}).reset_index()

# Ensure no zero divisions
batting['Batting_Average'] = batting.apply(lambda row: row['Total_Runs'] / row['Outs'] if row['Outs'] > 0 else row['Total_Runs'], axis=1)
batting['Strike_Rate'] = (batting['Total_Runs'] / batting['Balls_Faced']) * 100

# Fours and Sixes
fours = ball_df[(ball_df['batsman_run'] == 4)].groupby('Batsmen_ID').size().rename('No_of_Fours')
sixes = ball_df[(ball_df['batsman_run'] == 6)].groupby('Batsmen_ID').size().rename('No_of_Sixes')

batting = batting.merge(fours, on='Batsmen_ID', how='left')
batting = batting.merge(sixes, on='Batsmen_ID', how='left')
batting['No_of_Fours'] = batting['No_of_Fours'].fillna(0).astype(int)
batting['No_of_Sixes'] = batting['No_of_Sixes'].fillna(0).astype(int)

# =======================
# BOWLER STATS
# =======================
bowling = ball_df.groupby('Bowler_ID').agg({
    'total_run': 'sum',
    'ballnumber': 'count',
    'Bowler': 'first',
    'Match_ID': pd.Series.nunique,
    'isWicketDelivery': lambda x: (x & ball_df.loc[x.index, 'player_out'].notnull()).sum()
}).rename(columns={
    'total_run': 'Runs_Conceded',
    'ballnumber': 'Balls_Bowled',
    'Bowler': 'Player_Name',
    'Match_ID': 'Matches_Bowled',
    'isWicketDelivery': 'Wickets_Taken'
}).reset_index()

# Bowling metrics
bowling['Overs'] = bowling['Balls_Bowled'] / 6
bowling['Economy'] = bowling['Runs_Conceded'] / bowling['Overs']
bowling['Bowling_Average'] = bowling.apply(lambda row: row['Runs_Conceded'] / row['Wickets_Taken'] if row['Wickets_Taken'] > 0 else 0, axis=1)
bowling['Bowling_SR'] = bowling.apply(lambda row: row['Balls_Bowled'] / row['Wickets_Taken'] if row['Wickets_Taken'] > 0 else 0, axis=1)

# =======================
# MERGE BATTING & BOWLING
# =======================
# Use outer join to capture both batsmen and bowlers
player_stats = pd.merge(batting, bowling, left_on='Batsmen_ID', right_on='Bowler_ID', how='outer')

# Fill missing values
player_stats['Player_ID'] = player_stats['Batsmen_ID'].combine_first(player_stats['Bowler_ID'])
player_stats['Player_Name'] = player_stats['Player_Name_x'].combine_first(player_stats['Player_Name_y'])

# Drop unnecessary columns
player_stats.drop(columns=['Batsmen_ID', 'Bowler_ID', 'Player_Name_x', 'Player_Name_y'], inplace=True)

# Reorder columns
cols = ['Player_ID', 'Player_Name',
        'Total_Runs', 'Balls_Faced', 'Strike_Rate', 'Batting_Average', 'Matches_Played', 'No_of_Fours', 'No_of_Sixes',
        'Balls_Bowled', 'Runs_Conceded', 'Wickets_Taken', 'Matches_Bowled', 'Overs', 'Economy', 'Bowling_Average', 'Bowling_SR']

# Some players may not have all stats, so fill NaNs
for col in cols:
    if col not in player_stats.columns:
        player_stats[col] = 0

player_stats = player_stats[cols].fillna(0)

# Save to CSV
player_stats.to_csv('generated_player_stats.csv', index=False)
print("✅ Player stats generated and saved to 'generated_player_stats.csv'")
