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
