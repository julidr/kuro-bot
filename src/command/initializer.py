import os

from command.configuration.repository.server_repository import ServerRepository
from karthuria.client import KarthuriaClient
from karthuria.repository.character_repository import CharacterRepository
from karthuria.repository.dress_repository import DressRepository
from karthuria.repository.enemy_repository import EnemyRepository
from karthuria.repository.event_repository import EventRepository
from utils.file_utils import load_json_file


class Singleton(type):
    """
    Singleton class to avoid creating more that one instance of an specific class that uses it.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Initializer(metaclass=Singleton):
    """
    Class to initialize and inject all the dependencies of different classes.
    This can be done way better with a dependency injection framework or library, but right know lets just
    do it in the easy way.
    """

    def __init__(self):
        self.settings = load_json_file(os.getenv('SETTINGS_PATH', 'settings.json'))
        self.karthuria_client = KarthuriaClient(self.settings.get('karthuria_api_url'))
        self.character_repository = CharacterRepository(self.karthuria_client)
        self.server_repository = ServerRepository(self.settings.get('servers_path'))
        self.event_repository = EventRepository(self.karthuria_client)
        self.dress_repository = DressRepository(self.karthuria_client)
        self.enemy_repository = EnemyRepository(self.karthuria_client)

    def get_karthuria_client(self) -> KarthuriaClient:
        """
        Based on the class initialization return the specific client that was configured.
        :return: An instance of the Karthuria Client
        """
        return self.karthuria_client

    def get_character_repository(self) -> CharacterRepository:
        """
        Based on the class initialization return the specific character repository that was configured.
        :return: An instance of the Character Repository
        """
        return self.character_repository

    def get_servers_repository(self) -> ServerRepository:
        """
        Based on the class initialization return the specific server repository that was configured.
        :return: An instance of the Server Repository
        """
        return self.server_repository

    def get_event_repository(self) -> EventRepository:
        """
        Based on the class initialization return the specific event repository that was configured.
        :return: An instance of the Event Repository
        """
        return self.event_repository

    def get_dress_repository(self) -> DressRepository:
        """
        Based on the class initialization return the specific dress repository that was configured.
        :return: An instance of the Dress Repository
        """
        return self.dress_repository

    def get_enemy_repository(self) -> EnemyRepository:
        """
        Based on the class initialization return the specific enemy repository that was configured.
        :return: An instance of the Event Repository
        """
        return self.enemy_repository
