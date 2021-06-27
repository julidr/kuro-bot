import json
import os.path


def load_json_file(file_path: str) -> dict:
    """
    Load data from an existing json file

    :param file_path: File to load its respective values
    :return: A dictionary with the data that was loaded
    """
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def write_json_file(file_path: str, data: dict) -> None:
    """
    Write data into a json file
    :param file_path: File to write the given information
    :param data: The data to be saved in the file
    :return: None
    """
    with open(file_path, 'w') as file:
        json.dump(data, file)


def is_file(file_path: str) -> bool:
    """
    Checks if a given path is a file
    :param file_path: Path were the file is
    :return: True if is a file False otherwise
    """
    return os.path.isfile(file_path)
