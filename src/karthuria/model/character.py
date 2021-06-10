from src.karthuria.model.color import Color
from src.karthuria.model.school import School

PORTRAIT_URL = 'https://api.karen.makoo.eu/api/assets/jp/res/ui/images/archive/archive_chara/select' \
               '/chara_portrait_{0}.png '


class Character:
    """
    Model class of the basic information that can be retrieved from the Karthuria API
    """

    def __init__(self, chara_id, name, birth_day, birth_month, school_id, detailed_info=None):
        self.id = chara_id
        self.name = name
        self.birthday = '{0}/{1}'.format(birth_day, birth_month)
        self.school = School(school_id)
        self.portrait = PORTRAIT_URL.format(self.id)
        self.color = Color(name)
        if detailed_info:
            self.description = detailed_info['introduction']['en']
            self.seiyuu = detailed_info['cv']['en']
            self.likes = detailed_info['likes']['en']
            self.dislikes = detailed_info['dislikes']['en']
