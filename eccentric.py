import math

SECONDS_IN_DAY = 24*3600
RADIUS = 100000.0

class MomentInEccentric():
    def __init__(self, time, mean_longtitude, angle_from_sun):

class Eccentric():

    def __init__(self, eccentricity, aequant_eccentricity,
                 aphelion, apehlion_time, orbit_time):
        self.eccentricity = eccentricity
        self.aequant_eccentricity = aequant_eccentricity
        self.aphelion = aphelion
        self.aphelion_time = apehlion_time
        self.orbit_time = orbit_time * SECONDS_IN_DAY

    def get_moment(self, time):
        self.time = time
        time_diff = self.time - self.aphelion_time
        self.time_in_orb = time_diff.total_seconds() % self.orbit_time
        self.mean_longtitude = 360.0 * self.time_in_orb / self.orbit_time
        MomentInEccentric()

    def get_apparent_angle_by_mean_longtitude(self, mean_longtitude, current_aphelion):
        angle_from_aphelion = math.radians(mean_longtitude - current_aphelion)
        # triangle Center-Planter-aequant
        planet_angle = math.asin(math.sin(angle_from_aphelion)*self.aequant_eccentricity/RADIUS)
        # if aequant eccentricity = 0 than the planet angle is 0 - which is good

        #triangle Sun-Center-planet
        center_angle = planet_angle + angle_from_aphelion # external_angle
        sun_distance = math.sqrt(RADIUS**2+self.eccentricity**2
                                 -2*RADIUS*self.eccentricity*math.acos(center_angle))
        apparent_angle = math.asin(math.sin(center_angle)*RADIUS/sun_distance)

        center_angle = (math.degrees(center_angle) + current_aphelion) % 360
        apparent_angle = (math.degrees(apparent_angle) + current_aphelion) % 360

        return center_angle, apparent_angle, sun_distance

    def mean_longtitude_by_apparent_angle(self,):

    def get_sun_planet_distance(self, time):
        moment = self.get_moment(time)
        print (moment.mean_longtitude)
        # triangle Sun-Center-Planet:
        # data: Sun-center (=eccentricity); center-planet = 1;
        # angle_from_sun - given in moment
