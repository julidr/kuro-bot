from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from discord import Role, TextChannel, Guild
from requests import Response, HTTPError

from command.configuration.model.server import Channel, Server
from karthuria.model.character import Character, Dress, Enemy
from karthuria.model.event import Event, Challenge, Boss


@pytest.fixture
def character():
    detailed_info = {
        'introduction': {'en': 'Beautiful'},
        'cv': {'en': 'Aina Aiba'},
        'likes': {'en': 'Film/theater, training'},
        'dislikes': {'en': 'Scary stories (esp. Japanese horror films)'},
    }
    return Character(104, 'Claudine Saijo', 1, 8, 1, detailed_info)


@pytest.fixture
def dress():
    return Dress(1, 'Dress Test', 5)


@pytest.fixture
def enemy():
    return Enemy(1, 'Enemy Test', 1, 1)


@pytest.fixture
def event():
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=1)
    return Event(1, name='Event Test', end_date=end_date.timestamp(), start_date=start_date.timestamp())


@pytest.fixture
def complete_current_events():
    end_date = datetime.now() + timedelta(days=1)
    event = Event(1, end_date=end_date.timestamp())
    challenge = Challenge(2, end_date=end_date.timestamp())
    boss = Boss(3, end_date=end_date.timestamp())

    current_events = {
        'events': [event],
        'challenges': [challenge],
        'bosses': [boss]
    }
    return current_events


@pytest.fixture(scope='module')
def ok_characters_response():
    """
    Fixture to return a correct response of the endpoint chara.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and a dict with different characters
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_characters_sample_response()

    return response


@pytest.fixture(scope='module')
def bad_response():
    """
    Fixture that returns a bad response to any resource

    :return: A Response of the requests library, with its respective no ok value and HTTPError exception
    """
    response = Mock(spec=Response)
    response.ok = False
    response.raise_for_status.side_effect = HTTPError('Ups')

    return response


@pytest.fixture(scope='module')
def ok_character_response():
    """
    Fixture to return a correct response of the endpoint chara/id.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and one character information
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_character_sample_response()

    return response


@pytest.fixture(scope='module')
def ok_dress_response():
    """
    Fixture to return a correct response of the endpoint dress/id.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and one dress information
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_dress_sample_response()

    return response


@pytest.fixture(scope='module')
def ok_enemy_response():
    """
    Fixture to return a correct response of the endpoint enemy/id.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and one enemy information
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_enemy_sample_response()

    return response


@pytest.fixture(scope='module')
def ok_events_response():
    """
    Fixture to return a correct response of the endpoint event.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and events information
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_events_sample_response()

    return response


@pytest.fixture(scope='module')
def ok_current_events_response():
    """
    Fixture to return a correct response of the endpoint current.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and current events information
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_current_events_sample_response()

    return response


@pytest.fixture(scope='module')
def only_challenge_current_events_response():
    """
    Fixture to return a correct response of the endpoint current.json in Karthuria API when only challenge exist

    :return: A Response Mock of the requests library, with its respective ok value and current events information
    """
    complete_response = get_current_events_sample_response()
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = {
        'rogue': complete_response['rogue']
    }

    return response


@pytest.fixture()
def complete_server_info():
    return [{
        "server_id": 1,
        "name": "Test Server",
        "birthday_channel": {
            "channel_id": 1,
            "name": "birthday-channel",
            "announcement_rol": 1
        },
        "event_channel": {
            "channel_id": 1,
            "name": "event-channel",
            "announcement_rol": 2
        }
    }]


@pytest.fixture()
def one_channels_server_info():
    return [{
        "server_id": 1,
        "name": "Test Server",
        "birthday_channel": {
            "channel_id": 1,
            "name": "birthday-channel",
            "announcement_rol": 1
        },
        "event_channel": ""
    }]


@pytest.fixture()
def server_with_channels():
    birthday_channel = Channel(1, 'birthday-channel', 1)
    event_channel = Channel(2, 'event_channel', 2)
    server = Server(1, 'Test Channel', birthday_channel, event_channel)
    return server


@pytest.fixture()
def discord_role():
    data = {'id': 1, 'name': 'Test'}
    test_role = Role(guild='tests guild', state=True, data=data)
    return test_role


@pytest.fixture()
def discord_channel():
    data = {'id': 1, 'name': 'Test', 'type': 'Text', 'position': 1}
    mock_guild = Mock(spec=Guild)
    mock_guild.id = 1
    test_channel = TextChannel(guild=mock_guild, state=True, data=data)
    return test_channel


def get_characters_sample_response() -> dict:
    """
    Sample response of the call to Karthuria API chara.json

    :return: A dict with two samples of response of the API, one a valid character and other one invalid
    """
    return {
        "104": {
            "basicInfo": {
                "charaID": 104,
                "birth_day": 1,
                "birth_month": 8,
                "school_id": 1,
                "name_ruby": {
                    "ja": "Claudine Saijo",
                    "en": "",
                    "ko": "Claudine Saijo",
                    "zh_hant": "Claudine Saijo"
                }
            }
        },
        "803": {
            "basicInfo": {
                "charaID": 803,
                "birth_day": 0,
                "birth_month": 0,
                "school_id": 0,
                "name_ruby": {
                    "ja": "",
                    "en": "",
                    "ko": "",
                    "zh_hant": ""
                }
            }
        }
    }


def get_character_sample_response():
    """
    Sample response of the call to Karthuria API chara/id.json

    :return: A dict with two samples of response of the API with the found character
    """
    return {
        "basicInfo": {
            "charaID": 104,
            "birth_day": 1,
            "birth_month": 8,
            "school_id": 1
        },
        "info": {
            "cv": {
                "en": "Aina Aiba",
            },
            "introduction": {
                "en": "Beautiful",
            },
            "dislikes": {
                "en": "Scary stories (esp. Japanese horror films)",
            },
            "likes": {
                "en": "Film/theater, training",
            },
            "name_ruby": {
                "ja": "Claudine Saijo",
            }
        }
    }


def get_dress_sample_response():
    """
    Sample response of the call to Karthuria API dress/id.json

    :return: A dict with one sample of response of the API with the found dress
    """
    return {
        "basicInfo": {
            "cardID": "1050009",
            "rarity": 4,
            "character": 105,
            "name": {
                "ja": "Japanese Tristan",
                "en": "Tristan"
            }
        }
    }


def get_enemy_sample_response():
    """
    Sample response of the call to Karthuria API enemy/id.json

    :return: A dict with one sample of response of the API with the found enemy
    """
    return {
        "basicInfo": {
            "enemyID": "900620402_0",
            "icon": 9006204,
            "rarity": 1,
            "name": {
                "en": "Resentful Andrew",
                "ja": "Japanese Andrew"
            }
        }
    }


def get_events_sample_response():
    """
    Sample response of the call to Karthuria API event.json

    :return: A dict with two samples of response of the API with the found events
    """
    return {
        "1": {
            "name": {
                "ja": "Hello to Halloween Japanese",
                "en": "Hello to Halloween"
            }
        },
        "101": {
            "name": {
                "ja": "Troupe Revue (2021/5) Japanese",
                "en": "Troupe Revue (2021/5)",
            }
        },
    }


def get_current_events_sample_response():
    """
    Sample response of the call to Karthuria API current.json

    :return: A dict with samples of response of the API with the found current events
    """
    return {
        "titan": {
            "id": 38,
            "endAt": 1626033599,
            "enemy": {
                "0": {
                    "id": 900620202,
                    "hpLeft": 1767977770,
                    "hpLeftPercent": "58"
                },
                "1": {
                    "id": 900620301,
                    "hpLeft": 1776909729,
                    "hpLeftPercent": "59"
                }
            },
            "reward": [
                7,
                8
            ]
        },
        "event": {
            "79": {
                "id": 79,
                "info": 0,
                "beginAt": [
                    1611640800
                ],
                "endAt": [
                    3999999999
                ]
            },
            "118": {
                "id": 118,
                "info": 2021070102,
                "beginAt": [
                    1625122800,
                    1625122800,
                    1625122800
                ],
                "endAt": [
                    1625813999,
                    1626073199,
                    1625813999
                ]
            }
        },
        "rogue": {
            "0": {
                "id": 1050009,
                "beginAt": 1624863600,
                "endAt": 1625641199
            },
            "1": {
                "id": 1080009,
                "beginAt": 1625641200,
                "endAt": 1626418799
            }
        }
    }
