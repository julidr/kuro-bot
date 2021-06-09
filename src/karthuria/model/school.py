from enum import Enum


class School(Enum):
    """
    Enum with all the available schools in Shoujo Kageki Revue Starlight.
    The id and description can be retrieve from it.
    """

    SEISHO = 1, 'Seisho Music Academy 99th Class'
    RINMEIKAN = 2, 'Rinmeikan Girls School'
    FRONTIER = 3, 'Frontier School of Arts'
    SIEGFELD = 4, 'Siegfeld Institute of Music'
    SEIRAN = 5, 'Seiran General Art Institute'

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: int, description: str = None):
        self._description_ = description

    def __str__(self):
        return self.value

    @property
    def description(self):
        return self._description_
