import logging

from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.model.character import Dress

LOG_ID = "EnemyRepository"
logging.basicConfig(level=logging.INFO)


class EnemyRepository:
    """
    Repository with the information of enemies
    """

    def __init__(self, client: KarthuriaClient):
        self.client = client

    def get_enemy_by_id(self, enemy_id: int) -> Dress:
        """
        Search for an Enemy information by a given ID.
        If its not found returns None

        :param enemy_id: The id to search the Enemy
        :return: The Enemy instance found for the given id
        """
        enemy = None
        try:
            enemy = self.client.get_enemy(enemy_id)
            logging.info('[{0}] - Enemy wit id [{1}] retrieved successfully'.format(LOG_ID, enemy_id))
        except HTTPError as error:
            logging.error("[{0}] - Couldn't retrieve Enemy with id [{1}]: {2}".format(LOG_ID, enemy_id, error))
        return enemy
