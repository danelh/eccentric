class Zodiac():
    ARIES = 0
    TAURUS = 1
    GEMINI = 2
    CANCER = 3
    LEO = 4
    VIRGO = 5
    LIBRA = 6
    SCORPIO = 7
    SAGITTARIUS = 8
    CAPRICON = 9
    AQUARIUS = 10
    PISCES = 11

class Angle():
    @staticmethod
    def from_zondiac_to_number(zodiac, deg, min=0, sec=0):
        return 30 * zodiac + deg + (sec + 60*min)/3600.0