class MomentInEccentric():
    def __init__(self, eccentric, angle_from_sun=None, angle_from_aequant=None,
                 current_time=None):
        self.angle_from_sun = angle_from_sun
        self.angle_from_aequant = angle_from_aequant
        self.current_time = current_time

class Eccentric():
    def __init__(self, eccentricity, aequant_eccentricity,
                 aphelion, apehlion_time, orbit_time):
        self.eccentricity = eccentricity
        self.aequant_eccentricity = aequant_eccentricity
        self.aphelion = aphelion
        self.aphelion_time = apehlion_time
        self.orbit_time = orbit_time

    def get_moment(self):
        pass

    def get_sun_planet_distance(self, moment):
        pass
        # triangle Sun-Center-Planet:
        # data: Sun-center (=eccentricity); center-planet = 1;
        # angle_from_sun - given in moment
