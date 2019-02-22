import json

with open('../config.json') as f:
    config_data = json.load(f)

input_folder_path = config_data["input_folder_path"]
teams = list()

for _, team in folder:
    team_data = json.load(team)
    

