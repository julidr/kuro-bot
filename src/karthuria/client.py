import requests

from karthuria.model.character import Character, Dress, Enemy
from karthuria.model.event import Event, Challenge, Boss
from karthuria.model.school import School


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
        schools = set(item.value for item in School)
        if response.ok:
            characters_json = response.json()
            for character in characters_json:
                basic_info = characters_json[character]['basicInfo']
                if basic_info['birth_day'] != 0 and basic_info['school_id'] in schools:
                    list_of_characters.append(convert_to_character(basic_info))

        return list_of_characters if response.ok else response.raise_for_status()

    def get_character(self, chara_id: int) -> Character:
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

    def get_dress(self, dress_id: int) -> Dress:
        """
        Retrieve detailed information of one dress based on if its given id

        :param dress_id: the identifier of the dress
        :return: An object of Dress type with the detailed information
        """
        path = '/dress/{0}.json'.format(dress_id)
        response = requests.get(self.endpoint + path)

        if response.ok:
            dress_json = response.json()
            basic_info = dress_json['basicInfo']

        return convert_to_dress(basic_info) if response.ok else response.raise_for_status()

    def get_dresses_ids_by_character(self, character_id: int) -> list:
        """
        Retrieves all dresses ids for a given character

        :param character_id: the identifier of the character to search they dresses
        :return: A list with the found dresses ids
        """
        path = '/dress.json'
        list_of_dresses = []
        response = requests.get(self.endpoint + path)

        if response.ok:
            dresses_json = response.json()
            for dress in dresses_json:
                basic_info = dresses_json[dress]['basicInfo']
                if basic_info['character'] == character_id:
                    list_of_dresses.append(dress)

        return list_of_dresses if response.ok else response.raise_for_status()

    def get_equips_ids_by_character(self, character_id: int) -> list:
        """
        Retrieves all equips ids for a given character

        :param character_id: the identifier of the character to search they equips
        :return: A list with the found equips ids
        """
        path = '/equip.json'
        list_of_equips = []
        response = requests.get(self.endpoint + path)

        if response.ok:
            equips_json = response.json()
            for equip in equips_json:
                basic_info = equips_json[equip]['basicInfo']
                if basic_info['charas'] != 'None' and character_id in basic_info['charas']:
                    list_of_equips.append(equip)

        return list_of_equips if response.ok else response.raise_for_status()

    def get_enemy(self, enemy_id: int) -> Enemy:
        """
        Retrieve detailed information of one enemy based on if its given id

        :param enemy_id: the identifier of the dress
        :return: An object of Enemy type with the detailed information
        """
        path = '/enemy/{0}_0.json'.format(enemy_id)
        response = requests.get(self.endpoint + path)

        if response.ok:
            enemy_json = response.json()
            basic_info = enemy_json['basicInfo']

        return convert_to_enemy(basic_info) if response.ok else response.raise_for_status()

    def get_events(self) -> list:
        """
        Get all existing events information.

        :return: A list of Event with its id and name
        """
        path = '/event.json'
        response = requests.get(self.endpoint + path)
        events = []

        if response.ok:
            events_json = response.json()
            for event in events_json:
                name = events_json[event]['name']['en'] \
                    if events_json[event]['name']['en'] is not None else events_json[event]['name']['ja']
                events.append(Event(event, name=name))

        return events if response.ok else response.raise_for_status()

    def get_current_events(self) -> dict:
        """
        Retrieve basic information of current events.

        :return: A dictionary with different type of active events, challenges or boss battles
        """
        path = '/event/ww/current.json'
        response = requests.get(self.endpoint + path)
        current_events = {}

        if response.ok:
            events_json = response.json()
            if 'event' in events_json:
                event_info = events_json['event']
                events = [convert_to_event(event_info[event]) for event in event_info if event_info[event]['info'] != 0]
                current_events['events'] = events
            if 'rogue' in events_json:
                rogue_info = events_json['rogue']
                challenges = [convert_to_challenge(rogue_info[challenge]) for challenge in rogue_info]
                current_events['challenges'] = challenges
            if 'titan' in events_json:
                titan_info = events_json['titan']
                boss_end_at = titan_info['endAt']
                bosses = [convert_to_boss(titan_info['enemy'][boss], boss_end_at) for boss in titan_info['enemy']]
                current_events['bosses'] = bosses

        return current_events if response.ok else response.raise_for_status()


def convert_to_character(basic_info: dict, detailed_info: dict = None) -> Character:
    """
    Transform a dictionary with the 'basicInfo' and 'info' information returned by Karthuria API
    into a Character object

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


def convert_to_dress(basic_info: dict) -> Dress:
    """
    Transform a dictionary with the 'basicInfo' information returned by Karthuria API
    into a Dress object

    :param basic_info: Information retrieved from the 'basicInfo' response
    :return: A new instance of the Dress model with the given information
    """
    name = basic_info['name']['en'] if 'en' in basic_info['name'] else basic_info['name']['ja']
    dress = Dress(basic_info['cardID'],
                  name,
                  basic_info['rarity'])

    return dress


def convert_to_enemy(basic_info: dict) -> Enemy:
    """
    Transform a dictionary with the 'basicInfo' information returned by Karthuria API
    into a Enemy object

    :param basic_info: Information retrieved from the 'basicInfo' response
    :return: A new instance of the Enemy model with the given information
    """
    name = basic_info['name']['en'] if basic_info['name']['en'] is not None else basic_info['name']['ja']
    enemy = Enemy(int(basic_info['enemyID'].split('_', 1)[0]),
                  name,
                  basic_info['rarity'],
                  basic_info['icon'])

    return enemy


def convert_to_event(event_info: dict) -> Event:
    """
    Transform a dictionary with the 'event' information returned by Karthuria API into a Event object

    :param event_info: Information retrieved from the 'event' response
    :return: A new instance of the Event model with the given information
    """
    event = Event(event_info['id'],
                  end_date=event_info['endAt'][0],
                  start_date=event_info['beginAt'][0])

    return event


def convert_to_challenge(challenge_info: dict) -> Challenge:
    """
    Transform a dictionary with the 'rogue' information returned by Karthuria API into a Challenge object

    :param challenge_info: Information retrieved from the 'rogue' response
    :return: A new instance of the Challenge model with the given information
    """
    challenge = Challenge(challenge_info['id'],
                          challenge_info['endAt'],
                          start_date=challenge_info['beginAt'])

    return challenge


def convert_to_boss(boss_info: dict, end_at: int) -> Boss:
    """
    Transform a dictionary with the 'titan' and 'enemy' information returned by Karthuria API into a Boss object

    :param boss_info: Information retrieved from the 'titan' and 'enemy' response
    :param end_at: End date of the boss battle
    :return: A new instance of the Boss model with the given information
    """
    boss = Boss(boss_info['id'],
                end_at,
                hp_percentage=boss_info['hpLeftPercent'])

    return boss
