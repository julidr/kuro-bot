import json


def load_settings() -> dict:
    """
    Load the data existing in settings.json into a dict to be used in any moment according to the need
    :return: A dictionary with the data that was loaded
    """
    with open("settings.json", encoding="utf-8") as config:
        return json.load(config)


config = load_settings()
