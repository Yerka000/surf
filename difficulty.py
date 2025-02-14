DIFFICULTY_SETTINGS = {
    'easy': {
        'traffic_speed_range': (7, 10),
        'spawn_interval': 2000,
    },
    'medium': {
        'traffic_speed_range': (10, 15),
        'spawn_interval': 1500,
    },
    'hard': {
        'traffic_speed_range': (15, 20),
        'spawn_interval': 1000,
    }
}


def get_difficulty_settings(difficulty):
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS['easy'])
