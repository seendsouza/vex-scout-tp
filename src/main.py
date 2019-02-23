import json
import os
import click
import pprint
import statistics
import math

import helper


def extract_json_data():
    """
    Uses the config.json file to find input filepath
    Puts json into a dictionary
    Returns dictionary of all teams' stats
    """
    team_data = dict()
    
    with open('../config.json') as f:
        config_data = json.load(f)
    
    input_folder_path = config_data["input_folder_path"]
    file_extension_length = len(".json")
    
    for _, team_json in enumerate(os.listdir(input_folder_path)):
        team_number = team_json[:-1 * file_extension_length]
        with open(os.path.join(input_folder_path, team_json)) as team_file:
            team_data[team_number] = json.load(team_file)
    return team_data


def calculate_data(original_data):
    """
    Calculations:
    Drive Speed: (Inches/s)
    Shot accuracy: % of hits
    Cap flip accuracy: % of flips
    Cap post accuracy: % of posts
    In total
    Average points per match (calculated based on successful shots and cap flips)
    """
    seconds_per_minute = 60
    for _, team in enumerate(original_data):
        # Drive Speed
        diameter_of_omni = float(original_data[team]["drive_wheel_diameter"])
        rpm = float(original_data[team]["drive_rpm"])
        vel_in_per_sec = ((math.pi * diameter_of_omni) * rpm ) / seconds_per_minute 
        original_data[team]["vel_in_per_sec"] = vel_in_per_sec

        if original_data[team]["shot_accuracy"][0] != ["",""]:
            # Shot Accuracy
            hit_list = list()
            shit_list = list()
            for game in original_data[team]["shot_accuracy"]:
                print(game)
                hit_list.append(game[0])
                shit_list.append(game[1])
                succ_shot_percentage = [int(hit_list[i])/(int(shit_list[i])+int(hit_list[i])) for i,attempt in enumerate(hit_list)]
                original_data[team]["shot_accuracy_percent"] = succ_shot_percentage
                original_data[team]["shot_accuracy_percent_avg"] = statistics.mean(succ_shot_percentage)

            # Cap Flip Accuracy
        if original_data[team]["cap_flip_accuracy"][0] != ["",""]:
            hit_list = list()
            shit_list = list()
            for game in original_data[team]["cap_flip_accuracy"]:
                hit_list.append(game[0])
                shit_list.append(game[1])
                succ_cap_flip_percentage = [int(hit_list[i])/(int(shit_list[i])+int(hit_list[i])) for i,attempt in enumerate(hit_list)]
                original_data[team]["cap_flip_accuracy_percent"] = succ_cap_flip_percentage
                original_data[team]["cap_flip_accuracy_percent_avg"] = statistics.mean(succ_cap_flip_percentage)

            # Cap Post Accuracy
        if original_data[team]["cap_post_accuracy"][0] != ["",""]:
            hit_list = list()
            shit_list = list()
            for game in original_data[team]["cap_post_accuracy"]:
                hit_list.append(game[0])
                shit_list.append(game[1])
                succ_cap_post_percentage = [int(hit_list[i])/(int(shit_list[i])+int(hit_list[i])) for i,shot in enumerate(hit_list)]
                original_data[team]["cap_post_accuracy_percent"] = succ_cap_post_percentage
                original_data[team]["cap_post_accuracy_percent_avg"] = statistics.mean(succ_cap_post_percentage)

        #TODO: Average points per match
    return original_data

def sorted_stat(team_data, stat):
    with open('../config.json') as f:
        config_data = json.load(f)

    first_level_stats = config_data["first_level_stats"]
    second_level_stats = config_data["second_level_stats"]
    stat_teams = dict()
    for _, team in enumerate(team_data):
        if stat in first_level_stats:
            stat_teams[team] = team_data[team][stat]            
        elif stat in second_level_stats:
            current_stat_full = team_data[team][stat]
            current_stat_full = list(map(float, current_stat_full))
            stat_teams[team] = statistics.mean(current_stat_full)
        
    return sorted(stat_teams.items(), key=lambda x: x[1])

"""
Click Functions
"""
def show_all_data(ctx, param, value):
    if not value or ctx.resilient_parsing:
    	return
    team_data = extract_json_data()
    new_data = calculate_data(team_data)
    pprint.pprint(new_data)
    ctx.exit()

@click.group()
@click.option('--show_all_data', is_flag = True, expose_value = False,
              callback = show_all_data, 
              help='Shows all data from every single team.')
def cli():
    pass

@cli.command()
@click.argument('statistic')
def show_ranking(statistic):
    with open('../config.json') as f:
        config_data = json.load(f)

    first_level_stats = config_data["first_level_stats"]
    second_level_stats = config_data["second_level_stats"]
    third_level_stats = config_data["third_level_stats"]

    if statistic in first_level_stats or statistic in second_level_stats:
        team_data = extract_json_data()    
        for i,line in enumerate(sorted_stat(team_data, statistic)):
            pprint.pprint(line)
    else:
        click.echo("Invalid Statistic for show_ranking")

if __name__ == "__main__":
    cli()	
