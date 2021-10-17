import math

SECONDS_IN_DAY = 24*3600
RADIUS = 100000.0
PRESSESSION_SECONDS_A_YEAR = 51
APOGEE_SECOND_MOVEMENT_A_YEAR = 0

class MomentInEccentric():
    def __init__(self, time, mean_longtitude, center_angle, planet_angle, distance):
        self.time = time
        self.mean_longtitude = mean_longtitude
        self.center_angle = center_angle
        self.longtitude = planet_angle
        self.distance = distance

class Eccentric():

    def __init__(self, eccentricity, aequant_eccentricity,
                 aphelion, apehlion_time, orbit_time, aphelion_seconds_movement_a_year=0):
        self.eccentricity = eccentricity
        self.aequant_eccentricity = aequant_eccentricity
        self.aphelion = aphelion
        self.aphelion_time = apehlion_time
        self.orbit_time = orbit_time * SECONDS_IN_DAY
        self.aphelion_seconds_movement_a_year = aphelion_seconds_movement_a_year

    def get_moment(self, time):
        time_diff = time - self.aphelion_time
        time_in_orb = time_diff.total_seconds() % self.orbit_time
        mean_longtitude = self.aphelion + 360.0 * time_in_orb / self.orbit_time
        fixed_mean_longtitude = self.fix_angle_precession(time, mean_longtitude)
        center_angle, planet_angle, distance =self.get_apparent_angle_by_mean_longtitude(fixed_mean_longtitude,
                                                   self.fix_angle_precession(time, self.fix_aphelion(time)))
        return MomentInEccentric(time, fixed_mean_longtitude, center_angle, planet_angle, distance)

    def get_apparent_angle_by_mean_longtitude(self, mean_longtitude, current_aphelion):
        angle_from_aphelion = math.radians((mean_longtitude - current_aphelion) % 360)
        changed_side = False
        if math.degrees(angle_from_aphelion) > 180:
            changed_side = True
            angle_from_aphelion = math.radians(360) - angle_from_aphelion

        # triangle Center-Planter-aequant
        planet_angle = math.asin(math.sin(angle_from_aphelion)*self.aequant_eccentricity/RADIUS)
        # if aequant eccentricity = 0 than the planet angle is 0 - which is good

        #triangle Sun-Center-planet
        center_angle = planet_angle + (math.radians(180)-angle_from_aphelion) # external_angle
        sun_distance = math.sqrt(RADIUS**2+self.eccentricity**2
                                 -2*RADIUS*self.eccentricity*math.cos(center_angle))
        # we are first after the sharp angle, becaue asin(sin(150)) = 30.
        # so if the apparent angle > 90 we have a problem
        planet_angle = math.asin(math.sin(center_angle)*self.eccentricity/sun_distance)
        # apparent_angle = math.asin(math.sin(center_angle)*RADIUS/sun_distance)
        apparent_angle = math.radians(180) - planet_angle - center_angle

        # the real center angle should be 180 - center angle of the tirangle (planet-center_earth)
        # beacue real center angle is aphelion-center-planet
        center_angle = math.radians(180)-center_angle


        # this must come before the addition of aphelion
        if changed_side:
            center_angle = math.radians(360) - center_angle
            apparent_angle = math.radians(360) - apparent_angle


        center_angle = (math.degrees(center_angle) + current_aphelion) % 360
        apparent_angle = (math.degrees(apparent_angle) + current_aphelion) % 360


        return center_angle, apparent_angle, sun_distance

    def mean_longtitude_by_apparent_angle(self):
        pass

    def fix_angle_by_seconds_a_year(self, new_date, angle, seconds_fix):
        time_diff = (new_date - self.aphelion_time).total_seconds()
        years_diff = time_diff / (SECONDS_IN_DAY*365.25)
        angle += years_diff * (seconds_fix / 3600.0)
        angle = angle % 360
        return angle

    def fix_angle_precession(self, new_date, angle):
        return self.fix_angle_by_seconds_a_year(new_date, angle, PRESSESSION_SECONDS_A_YEAR)

    def fix_aphelion(self, new_date):
        return self.fix_angle_by_seconds_a_year(new_date, self.aphelion, self.aphelion_seconds_movement_a_year)