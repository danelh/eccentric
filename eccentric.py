class Eccentric():
    def __init__(self, eccentricity, aequant_eccentricity,
                 aphelion, apehlion_time):
        self.eccentricity = eccentricity
        self.aequant_eccentricity = aequant_eccentricity
        self.aphelion = aphelion
        self.aphelion_time = apehlion_time

    def get_sun_planet_distance(self):