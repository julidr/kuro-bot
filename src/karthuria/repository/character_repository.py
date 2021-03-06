import logging

from requests.exceptions import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.model.character import Character

LOG_ID = "CharacterRepository"


class CharacterRepository:
    """
    Repository with the information of characters
    """

    def __init__(self, client: KarthuriaClient):
        self.client = client
        self.characters = self.__load_characters()

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

    def get_character_birthday(self, date: str) -> Character:
        """
        For a given date looks for a character with that date birthday and return it.
        :param date: A date in format %d/%m if this format is not used then it will never found a character.
        :return: The character that has a birthday in the given date
        """
        for character in self.characters:
            if character.birthday == date:
                return self.client.get_character(character.id)

    def __load_characters(self) -> list:
        """
        Calls Karthuria API to load characters basic information

        :return: A list with the characters information if is successful, otherwise an empty list
        """
        characters = []
        try:
            characters = self.client.get_characters()
            logging.debug('[{0}] - Characters information loaded successfully'.format(LOG_ID))
        except HTTPError as error:
            logging.error("[{0}] - Couldn't load characters information {1}".format(LOG_ID, error))
        return characters
