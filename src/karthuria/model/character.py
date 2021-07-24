from datetime import datetime

from karthuria.model.color import Color
from karthuria.model.school import School

PORTRAIT_URL = 'https://api.karen.makoo.eu/api/assets/jp/res/ui/images/archive/archive_chara/select' \
               '/chara_portrait_{0}.png '


class Character:
    """
    Model class of a Character with the basic information that can be retrieved from the Karthuria API
    """

    def __init__(self, chara_id, name, birth_day, birth_month, school_id, detailed_info=None):
        self.id = chara_id
        self.name = name
        self.birthday = datetime(1, birth_month, birth_day).strftime('%d/%m')
        self.school = School(school_id)
        self.portrait = PORTRAIT_URL.format(self.id)
        self.color = Color(name)
        if detailed_info:
            self.description = detailed_info['introduction']['en']
            self.seiyuu = detailed_info['cv']['en']
            self.likes = detailed_info['likes']['en']
            self.dislikes = detailed_info['dislikes']['en']


class Dress:
    """
    Model class of Dress with the basic information that can be retrieved from the Karthuria API
    """

    def __init__(self, dress_id: int, name: str, rarity: int):
        self.dress_id = dress_id
        self.name = name
        self.rarity = rarity


class Enemy:
    """
    Model class of Enemy with the basic information that can be retrieved from the Karthuria API
    """

    def __init__(self, enemy_id: id, name: str, rarity: int, icon: int):
        self.enemy_id = enemy_id
        self.name = name
        self.rarity = rarity
        self.icon = icon
