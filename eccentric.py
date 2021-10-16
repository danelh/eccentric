SECONDS_IN_DAY = 24*3600

class MomentInEccentric():
    def __init__(self, eccentric, time):
        self.time = time
        time_diff = self.time - eccentric.aphelion_time
        self.time_in_orb = time_diff.total_seconds() % eccentric.orbit_time
        self.mean_longtitude = 360.0 * self.time_in_orb / eccentric.orbit_time

class Eccentric():
    def __init__(self, eccentricity, aequant_eccentricity,
                 aphelion, apehlion_time, orbit_time):
        self.eccentricity = eccentricity
        self.aequant_eccentricity = aequant_eccentricity
        self.aphelion = aphelion
        self.aphelion_time = apehlion_time
        self.orbit_time = orbit_time * SECONDS_IN_DAY

    def get_moment(self, time):
        return MomentInEccentric(self, time)

    def get_sun_planet_distance(self, time):
        moment = self.get_moment(time)
        print (moment.mean_longtitude)
        # triangle Sun-Center-Planet:
        # data: Sun-center (=eccentricity); center-planet = 1;
        # angle_from_sun - given in moment
