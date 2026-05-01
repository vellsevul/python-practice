import json, os

def load_settings():
    if not os.path.exists("settings.json"): return {"difficulty": 1}
    with open("settings.json", "r") as f: return json.load(f)

def save_settings(data):
    with open("settings.json", "w") as f: json.dump(data, f, indent=4)

def load_leaderboard():
    if not os.path.exists("leaderboard.json"): return []
    with open("leaderboard.json", "r") as f: return json.load(f)

def save_leaderboard(data):
    with open("leaderboard.json", "w") as f: json.dump(data, f, indent=4)