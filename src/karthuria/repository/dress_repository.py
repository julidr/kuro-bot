import logging

from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.model.character import Dress

LOG_ID = "DressRepository"


class DressRepository:
    """
    Repository with the information of dresses
    """

    def __init__(self, client: KarthuriaClient):
        self.client = client
        self.dresses = self.__load_dresses()

    def get_dress_by_id(self, dress_id: int) -> Dress:
        """
        Search for a Dress information by a given ID.
        If its not found returns None

        :param dress_id: The id to search the dress
        :return: The Dress instance found for the given id
        """
        dress = None
        try:
            dress = self.client.get_dress(dress_id)
            logging.debug('[{0}] - Dress wit id [{1}] retrieved successfully'.format(LOG_ID, dress_id))
        except HTTPError as error:
            logging.error("[{0}] - Couldn't retrieve Dress with id [{1}]: {2}".format(LOG_ID, dress_id, error))
        return dress

    def get_dresses_by_character_id(self, character_id: int) -> list:
        """
        Search for dresses information by a given Character ID.
        If its not found returns None

        :param character_id: The character id to get its dresses
        :return: The different Dresses instances found for the given id
        """
        result = [dress for dress in self.dresses if dress.character == character_id]
        if len(result) > 0:
            return result

    def __load_dresses(self) -> list:
        """
        Calls Karthuria API to load dresses basic information

        :return: A list with the dresses information if is successful, otherwise an empty list
        """
        dresses = []
        try:
            dresses = self.client.get_dresses()
            logging.debug('[{0}] - Dresses information loaded successfully'.format(LOG_ID))
        except HTTPError as error:
            logging.error("[{0}] - Couldn't load dresses information {1}".format(LOG_ID, error))
        return dresses
