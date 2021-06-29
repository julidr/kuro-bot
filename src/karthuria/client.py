import requests

from karthuria.model.character import Character


class KarthuriaClient:
    """
    Client to connect an retrieve information from the Karthuria API.
    More information can be found in their web site: https://karth.top/home
    """

    def __init__(self, endpoint: str):
        """
        Initialize the KarthuriaClient

        :param endpoint: Base url to retrieve information from the Karthuria API
        """
        self.endpoint = endpoint

    def get_characters(self) -> list:
        """
        Get all existing character information.

        :return: A list of Character information
        """
        path = '/chara.json'
        list_of_characters = []

        response = requests.get(self.endpoint + path)
        if response.ok:
            characters_json = response.json()
            for character in characters_json:
                basic_info = characters_json[character]['basicInfo']
                if basic_info['birth_day'] != 0:
                    list_of_characters.append(convert_to_character(basic_info))

        return list_of_characters if response.ok else response.raise_for_status()

    def get_character(self, chara_id: int) -> dict:
        """
        Retrieve detailed information of one character based on if its given id

        :param chara_id: the identifier of the character
        :return: An object of Character type with the detailed information
        """
        path = '/chara/{0}.json'.format(chara_id)
        response = requests.get(self.endpoint + path)

        if response.ok:
            character_json = response.json()
            basic_info = character_json['basicInfo']
            info = character_json['info']

        return convert_to_character(basic_info, info) if response.ok else response.raise_for_status()


def convert_to_character(basic_info: dict, detailed_info: dict = None) -> Character:
    """
    Transform a dictionary with the 'basicInfo' and 'info' information returned by Karthuria API

    :param basic_info: Information retrieved from the 'basicInfo' response
    :param detailed_info: Information retrieved from the 'info' response of detailed character information
    :return: A new instance of the Character model with the given information
    """
    name = basic_info['name_ruby']['ja'] if 'name_ruby' in basic_info else detailed_info['name_ruby']['ja']
    character = Character(basic_info['charaID'],
                          name,
                          basic_info['birth_day'],
                          basic_info['birth_month'],
                          basic_info['school_id'],
                          detailed_info=detailed_info)
    return character
