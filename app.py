from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
CORS(app, origins=["http://localhost:3000", "hhttps://www.mudbloom.com/"])

# Load player stats CSV once
df = pd.read_csv("generated_player_stats.csv")
df['Player_Name_lower'] = df['Player_Name'].str.lower()

@app.route("/")
def home():
    return "Welcome to the Player Stats API!"

@app.route("/player", methods=["GET"])
def get_player_stats():
    name_query = request.args.get("name", "").strip().lower()

    if not name_query:
        return jsonify({"error": "Please provide a player name using ?name=..."})

    matches = df[df['Player_Name_lower'].str.contains(name_query)]

    if matches.empty:
        return jsonify({"error": "Player not found."})

    results = []
    for _, row in matches.iterrows():
        stats = {
            "Player_ID": row["Player_ID"],
            "Player_Name": row["Player_Name"],
            "Total_Runs": int(row["Total_Runs"]),
            "Matches_Played": int(row["Matches_Played"]),
            "Balls_Faced": int(row["Balls_Faced"]),
            "Batting_Average": round(row["Batting_Average"], 2),
            "Strike_Rate": round(row["Strike_Rate"], 2),
            "Fours": int(row["No_of_Fours"]),
            "Sixes": int(row["No_of_Sixes"]),
            "Balls_Bowled": int(row["Balls_Bowled"]),
            "Runs_Conceded": int(row["Runs_Conceded"]),
            "Wickets_Taken": int(row["Wickets_Taken"]),
            "Economy": round(row["Economy"], 2),
            "Bowling_Average": round(row["Bowling_Average"], 2),
            "Bowling_SR": round(row["Bowling_SR"], 2)
        }
        results.append(stats)

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)
