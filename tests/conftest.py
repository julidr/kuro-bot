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
def ok_dresses_response():
    """
    Fixture to return a correct response of the endpoint dress.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and two dresses information
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_dresses_sample_response()

    return response


@pytest.fixture(scope='module')
def ok_equips_response():
    """
    Fixture to return a correct response of the endpoint equip.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and two equips information
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_equips_sample_response()

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


def get_dresses_sample_response():
    """
    Sample response of the call to Karthuria API dress.json

    :return: A list with two samples of response of the API with the found dresses
    """
    return {
        "1010001": {
            "basicInfo": {
                "cardID": "1010001",
                "rarity": 2,
                "character": 101,
                "name": {
                    "ja": "聖翔音楽学園",
                    "en": "Seisho Music Academy",
                    "ko": "세이쇼 음악학교",
                    "zh_hant": "聖翔音樂學院"
                },
                "released": {
                    "ww": 1540105200,
                    "ja": 1540105200
                }
            },
            "base": {
                "attribute": 1,
                "attackType": 1,
                "roleIndex": {
                    "role": "front",
                    "index": 11048
                },
                "skills": [
                    1,
                    89,
                    30,
                    11,
                    12
                ],
                "unitSkill": 0,
                "entrySkill": 0,
                "remake": False
            },
            "stat": {
                "total": 4782,
                "agi": 904,
                "atk": 832,
                "hp": 22582,
                "mdef": 835,
                "pdef": 860
            },
            "statRemake": False
        },
        "1010002": {
            "basicInfo": {
                "cardID": "1010002",
                "rarity": 3,
                "character": 101,
                "name": {
                    "ja": "太陽の国の騎士",
                    "en": "Knight of the Sun Nation",
                    "ko": "태양 나라의 기사",
                    "zh_hant": "太陽之國騎士"
                },
                "released": {
                    "ww": 1540105200,
                    "ja": 1540105200
                }
            },
            "base": {
                "attribute": 5,
                "attackType": 1,
                "roleIndex": {
                    "role": "front",
                    "index": 12048
                },
                "skills": [
                    1,
                    89,
                    20,
                    1,
                    17
                ],
                "unitSkill": 169,
                "entrySkill": 0,
                "remake": False
            },
            "stat": {
                "total": 5388,
                "agi": 1239,
                "atk": 1342,
                "hp": 19048,
                "mdef": 1007,
                "pdef": 639
            },
            "statRemake": False
        }
    }


def get_equips_sample_response():
    """
    Sample response of the call to Karthuria API equip.json

    :return: A dict with two samples of response of the API with the found equips
    """
    return {
        "2000021": {
            "basicInfo": {
                "cardID": "2000021",
                "rarity": 2,
                "charas": [
                    104
                ],
                "name": {
                    "ja": "Oui！",
                    "en": "Oui!",
                    "ko": "Oui!",
                    "zh_hant": "Oui（是的）！"
                },
                "profile": {
                    "ja": "――『少女☆歌劇 レヴュースタァライト 第１０話』より",
                    "en": "- From \"Revue Starlight\" Episode 10",
                    "ko": "――[소녀☆가극 레뷰 스타라이트 제10화]로부터",
                    "zh_hant": "──取自『少女☆歌劇 Revue Starlight 第10話』"
                },
                "released": {
                    "ww": 1540105200,
                    "ja": 1540105200
                }
            },
            "skill": {
                "id": 10018,
                "icon": 39,
                "type": {
                    "ja": "永続",
                    "en": "Passive",
                    "ko": "영구",
                    "zh_hant": "永續"
                },
                "params": [
                    {
                        "icon": 39,
                        "type": "normal",
                        "hits": None,
                        "duration": None,
                        "accuracy": None,
                        "target": {
                            "ja": "自身",
                            "en": "Self",
                            "ko": "자신",
                            "zh_hant": "自己"
                        },
                        "description": {
                            "ja": "有利属性ダメージアップ([6, 6, 7, 8, 9])",
                            "en": "Effective Element Dmg Up ([6, 6, 7, 8, 9])",
                            "ko": "유리한 속성 대미지 증가([6, 6, 7, 8, 9])",
                            "zh_hant": "提升有利屬性傷害（[6, 6, 7, 8, 9]）"
                        },
                        "descriptionExtra": None
                    }
                ]
            },
            "activeSkill": 0
        },
        "2000022": {
            "basicInfo": {
                "cardID": "2000022",
                "rarity": 2,
                "charas": "None",
                "name": {
                    "ja": "あの娘を捜して",
                    "en": "Searching for Her",
                    "ko": "그 아이를 찾아서",
                    "zh_hant": "找出那個女孩"
                },
                "profile": {
                    "ja": "――『少女☆歌劇 レヴュースタァライト 第１１話』より",
                    "en": "- From \"Revue Starlight\" Episode 11",
                    "ko": "――[소녀☆가극 레뷰 스타라이트 제11화]로부터",
                    "zh_hant": "──取自『少女☆歌劇 Revue Starlight 第11話』"
                },
                "released": {
                    "ww": 1540105200,
                    "ja": 1540105200
                }
            },
            "skill": {
                "id": 20004,
                "icon": 89,
                "type": {
                    "ja": "開幕時",
                    "en": "At Start",
                    "ko": "개막",
                    "zh_hant": "開幕時"
                },
                "params": [
                    {
                        "icon": 89,
                        "type": "normal",
                        "hits": None,
                        "duration": None,
                        "accuracy": 100,
                        "target": {
                            "ja": "自身",
                            "en": "Self",
                            "ko": "자신",
                            "zh_hant": "自己"
                        },
                        "description": {
                            "ja": "キラめき回復([16, 18, 20, 22, 24])",
                            "en": "Brilliance Recovery ([16, 18, 20, 22, 24])",
                            "ko": "반짝임 회복([16, 18, 20, 22, 24])",
                            "zh_hant": "回復光芒（[16, 18, 20, 22, 24]）"
                        },
                        "descriptionExtra": None
                    }
                ]
            },
            "activeSkill": 0
        },
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
