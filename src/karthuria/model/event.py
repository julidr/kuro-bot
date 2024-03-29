from datetime import datetime


class Event:
    """
    Model class of Events information that can be retrieved from Karthuria API
    """

    def __init__(self, event_id: int, end_date: int = None, name: str = None, start_date: int = None, event_url: str = ''):
        self.event_id = event_id
        self.name = name
        self.start_date = datetime.fromtimestamp(start_date) if start_date is not None else start_date
        self.end_date = datetime.fromtimestamp(end_date) if end_date is not None else end_date
        self.icon = '{0}/res_en/res/event_permanent/banner/event_banner_{1}.png'.format(event_url, event_id)

    def set_start_date(self, start_date: int) -> None:
        self.start_date = datetime.fromtimestamp(start_date)

    def set_end_date(self, end_date: int) -> None:
        self.end_date = datetime.fromtimestamp(end_date)

    def set_name(self, name: str) -> None:
        self.name = name


class Challenge(Event):
    """
    Model class of Challenge information that can be retrieved from Karthuria API
    """

    def __init__(self, challenge_id: int, end_date: int, name: str = None, rarity: int = None, start_date: int = None,
                 challenge_url: str = ''):
        super().__init__(challenge_id, end_date, name, start_date)
        self.icon = '{0}/res/item_root/large/1_{1}.png'.format(challenge_url, challenge_id)
        self.rarity = rarity

    def set_rarity(self, rarity: int) -> None:
        self.rarity = rarity


class Boss(Event):
    """
    Model class of Enemy information that can be retrieved from Karthuria API
    """

    def __init__(self, boss_id: int, end_date: int, name: str = None, rarity: int = None, hp_percentage: str = None,
                 boss_url: str = ''):
        super().__init__(boss_id, end_date, name, None)
        self.rarity = rarity
        self.hp_percentage = hp_percentage
        self.enemy_icon_url = '{0}/{1}'.format(boss_url, 'res/icon/enemy/{0}.png')

    def set_rarity(self, rarity: int) -> None:
        self.rarity = rarity

    def set_hp_percentage(self, hp_percentage: str) -> None:
        self.hp_percentage = hp_percentage

    def set_icon(self, icon_id: int):
        self.icon = self.enemy_icon_url.format(icon_id)
