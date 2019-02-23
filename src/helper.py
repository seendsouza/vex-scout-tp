def is_empty(lis1): 
    if len(lis1) == 0: 
        return 0
    else: 
        return 1

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
                if helper.is_empty(original_data[team][data]):
                    original_data[team].pop(data, None)
            elif data in second_level_stats:
                if helper.is_empty(original_data[team][data]):
                    original_data[team].pop(data, None)

        if helper.is_empty(original_data[team]):
            original_data.pop(team, None)

    return original_data