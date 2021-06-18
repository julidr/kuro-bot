from unittest.mock import Mock

import pytest
from requests import Response, HTTPError

from karthuria.model.character import Character


@pytest.fixture
def character():
    detailed_info = {
        'introduction': {'en': 'Beautiful'},
        'cv': {'en': 'Aina Aiba'},
        'likes': {'en': 'Film/theater, training'},
        'dislikes': {'en': 'Scary stories (esp. Japanese horror films)'},
    }
    return Character(104, 'Claudine Saijo', 1, 8, 1, detailed_info)


@pytest.fixture(scope='module')
def ok_characters_response():
    """
    Fixture to return a correct response of the endpoint chara.json in Karthuria API

    :return: A Response Mock of the requests library, with its respective ok value and a dict with different characters
    """
    response = Mock(spec=Response)
    response.ok = True
    response.json.return_value = get_characters_sample_request()

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
    response.json.return_value = get_character_sample_request()

    return response


def get_characters_sample_request() -> dict:
    """
    Sample request of the call to Karthuria API chara.json

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


def get_character_sample_request():
    """
    Sample request of the call to Karthuria API chara/id.json

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
