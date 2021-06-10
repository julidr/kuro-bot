import logging

from requests.exceptions import HTTPError

from src.karthuria.client import KarthuriaClient
from src.karthuria.model.character import Character
from src.utils.settings_utils import load_settings

LOG_ID = "BirthdayRepository"
logging.basicConfig(level=logging.INFO)


class BirthdayRepository:
    """
    Repository with the information of characters birthdays
    """

    def __init__(self):
        self.config = load_settings()
        self.client = KarthuriaClient(self.config.get('karthuria_api'))
        self.characters = self._load_characters()

    def get_characters(self) -> list:
        """
        Return the list of characters that are currently loaded

        :return: A list with characters information
        """
        return self.characters

    def get_character_by_name(self, name: str) -> Character:
        """
        Looks for a character name in the list of available characters an return it

        :param name: Of the character to search, can be the first name, the last name or the full name
        :return: A character that match with the queried name
        """
        result = [character for character in self.characters if name.lower() in character.name.lower()]
        if len(result) > 0:
            return result[0]

    def _load_characters(self) -> list:
        """
        Calls Karthuria API to load characters basic information

        :return: A list with the characters information if is successful, otherwise an empty list
        """
        characters = []
        try:
            characters = self.client.get_characters()
            logging.info('[{0}] - Characters information loaded successfully'.format(LOG_ID))
        except HTTPError:
            logging.error("[{0}] - Couldn't load characters information".format(LOG_ID))
        return characters
