import pandas as pd

# Load generated player stats
df = pd.read_csv("generated_player_stats.csv")

# Convert player names to lowercase for flexible search
df['Player_Name_lower'] = df['Player_Name'].str.lower()

def get_player_stats(name):
    name = name.strip().lower()
    result = df[df['Player_Name_lower'].str.contains(name)]

    if result.empty:
        print("❌ Player not found.")
        return

    for idx, row in result.iterrows():
        print(f"\n🔹 Stats for: {row['Player_Name']}")
        print(f"Player ID         : {row['Player_ID']}")
        print(f"Total Runs        : {int(row['Total_Runs'])}")
        print(f"Matches Played    : {int(row['Matches_Played'])}")
        print(f"Balls Faced       : {int(row['Balls_Faced'])}")
        print(f"Batting Average   : {round(row['Batting_Average'], 2)}")
        print(f"Strike Rate       : {round(row['Strike_Rate'], 2)}")
        print(f"4s                : {row['No_of_Fours']}, 6s: {row['No_of_Sixes']}")
        print(f"\n🎯 Bowling Stats:")
        print(f"Balls Bowled      : {int(row['Balls_Bowled'])}")
        print(f"Runs Conceded     : {int(row['Runs_Conceded'])}")
        print(f"Wickets Taken     : {int(row['Wickets_Taken'])}")
        print(f"Economy           : {round(row['Economy'], 2)}")
        print(f"Bowling Average   : {round(row['Bowling_Average'], 2)}")
        print(f"Bowling SR        : {round(row['Bowling_SR'], 2)}")
        print("="*40)

# Input loop
if __name__ == "__main__":
    while True:
        name_input = input("\nEnter player name (or type 'exit' to quit): ")
        if name_input.lower() == 'exit':
            break
        get_player_stats(name_input)
