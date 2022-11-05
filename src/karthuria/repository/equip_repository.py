import logging

from requests.exceptions import HTTPError

from karthuria.client import KarthuriaClient

LOG_ID = "EquipRepository"


class EquipRepository:
    """
    Repository with the information of equips
    """

    def __init__(self, client: KarthuriaClient):
        self.client = client
        self.equips = self.__load_equips()

    def get_equips_by_character_id(self, character_id: int) -> list:
        """
        Search for equips information by a given Character ID.
        If its not found returns None

        :param character_id: The character id to get its equips
        :return: The different Equips instances found for the given id
        """
        result = [equip for equip in self.equips if
                  (equip.characters is not None and character_id in equip.characters)]
        if len(result) > 0:
            return result

    def __load_equips(self) -> list:
        """
        Calls Karthuria API to load equips basic information

        :return: A list with the equips information if is successful, otherwise an empty list
        """
        equips = []
        try:
            equips = self.client.get_equips()
            logging.debug('[{0}] - Equips information loaded successfully'.format(LOG_ID))
        except HTTPError as error:
            logging.error("[{0}] - Couldn't load equips information {1}".format(LOG_ID, error))
        return equips
