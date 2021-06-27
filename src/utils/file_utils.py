import json


def load_json_file(file_path: str) -> dict:
    """
    Load data from an existing json file

    :param file_path: File to load its respective values
    :return: A dictionary with the data that was loaded
    """
    with open(file_path, encoding="utf-8") as settings:
        return json.load(settings)
