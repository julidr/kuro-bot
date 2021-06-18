from karthuria.client import KarthuriaClient
from karthuria.repository.character_repository import CharacterRepository
from utils.settings_utils import load_settings


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
        self.settings = load_settings()
        self.karthuria_client = KarthuriaClient(self.settings.get('karthuria_api_url'))
        self.character_repository = CharacterRepository(self.karthuria_client)

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
