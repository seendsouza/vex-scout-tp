import json
import os
import click
import pprint
import statistics

def is_empty(lis1): 
    if len(lis1) == 0: 
        return 0
    else: 
        return 1

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

def prune_data(original_data):
    """
    Deletes empty statistics from dictionary
    Returns cleaner and shortened dictionary
    """
    # TODO: FIX THIS SO IT DOESN'T DELETE THE WHOLE DICT
    with open('../config.json') as f:
        config_data = json.load(f)

    first_level_stats = config_data["first_level_stats"]
    second_level_stats = config_data["second_level_stats"]
    third_level_stats = config_data["third_level_stats"]
    empty_counter = 0

    for _, team in enumerate(list(original_data.keys())):
        for __, data in enumerate(list(original_data[team].keys())):
            if data in first_level_stats:
                if is_empty(original_data[team][data]):
                    original_data[team].pop(data, None)
            elif data in second_level_stats:
                if is_empty(original_data[team][data]):
                    original_data[team].pop(data, None)

        if is_empty(original_data[team]):
            original_data.pop(team, None)

    return original_data

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
    pprint.pprint(team_data)
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
