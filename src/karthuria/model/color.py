from enum import Enum


class Color(Enum):
    """
    Enum with the representative colors of each one of the girls
    """

    KAREN = 'Karen Aijo', (251, 84, 87)
    HIKARI = 'Hikari Kagura', (98, 145, 233)
    MAHIRU = 'Mahiru Tsuyuzaki', (97, 191, 153)
    CLAUDINE = 'Claudine Saijo', (254, 153, 82)
    MAYA = 'Maya Tendo', (171, 167, 172)
    JUNNA = 'Junna Hoshimi', (141, 188, 219)
    NANA = 'Nana Daiba', (216, 173, 66)
    FUTABA = 'Futaba Isurugi', (140, 103, 170)
    KAORUKO = 'Kaoruko Hanayagi', (224, 134, 150)
    TAMAO = 'Tamao Tomoe', (198, 153, 238)
    ICHIE = 'Ichie Otonashi', (246, 181, 230)
    FUMI = 'Fumi Yumeoji', (180, 220, 132)
    RUI = 'Rui Akikaze', (98, 202, 138)
    YUYUKO = 'Yuyuko Tanaka', (236, 118, 138)
    ARURU = 'Aruru Otsuki', (218, 188, 72)
    MISORA = 'Misora Kano', (112, 195, 228)
    LALAFIN = 'Lalafin Nonomiya', (249, 122, 185)
    TSUKASA = 'Tsukasa Ebisu', (240, 161, 81)
    SHIZUHA = 'Shizuha Kocho', (97, 204, 170)
    AKIRA = 'Akira Yukishiro', (186, 191, 218)
    MICHIRU = 'Michiru Otori', (255, 188, 71)
    MEIFAN = 'MeiFan Liu', (236, 138, 243)
    SHIORI = 'Shiori Yumeoji', (112, 217, 219)
    YACHIYO = 'Yachiyo Tsuruhime', (233, 99, 161)
    KOHARU = 'Koharu Yanagi', (212, 49, 78)
    SUZU = 'Suzu Minase', (34, 151, 115)
    HISAME = 'Hisame Honami', (221, 211, 97)

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: int, rgb: str = None):
        self._rgb_ = rgb

    def __str__(self):
        return self.value

    @property
    def rgb(self):
        return self._rgb_
