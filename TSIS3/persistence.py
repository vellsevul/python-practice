import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "difficulty": 1,
            "car_color": "red",
            "sound": True
        }
        save_settings(default_settings)
        return default_settings
    
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"difficulty": 1, "car_color": "red", "sound": True}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)
