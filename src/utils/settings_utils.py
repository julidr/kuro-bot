import json


def load_settings(settings_file: str = 'settings.json') -> dict:
    """
    Load the data existing in settings.json into a dict to be used in any moment according to the need

    :param settings_file: File to load its respective configuration
    :return: A dictionary with the data that was loaded
    """
    with open(settings_file, encoding="utf-8") as settings:
        return json.load(settings)
