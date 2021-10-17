import math

from angles import Angle, Zodiac
from eccentric import Eccentric
from datetime import datetime

MARS_ANGLE = 1.83333333
MARS_LIMITS = [Angle.from_zondiac_to_number(Zodiac.LEO, deg=16, min=30),
               Angle.from_zondiac_to_number(Zodiac.AQUARIUS, deg=16, min=30)]

# Earth eccentricity according to Tycho/Copernicus:
# See ch. 17 Mars vs Earth radius is 1.519
# Now in ch. 5 (p.99) Earth eccentricity 3584 of 100000 Mars radius,
# so Earth eccebtricity in Earth radius is 5444 of 100000 Earth Radius
# NO, 3584 is the figure for Earth 100000.
# Accorfing to TBOO 2. p.46 & 83 and observation 1579 Dec it seems
# the perigee (Earh seen from Sun) is about Cancer 4-5 deg. in about 15 Dec.
# the apogee seen from the Sun will be Capricon 5 deg.
earth_aphelion = Angle.from_zondiac_to_number(Zodiac.CAPRICON, deg=4)
earth_aphelion_date = datetime(year=1590, month=6, day=15, hour=19, minute=37)
earth = Eccentric(eccentricity=3584, aequant_eccentricity=0, aphelion=earth_aphelion,
                  apehlion_time=earth_aphelion_date, orbit_time=365.25)
# m = earth.get_moment(datetime(year=1585, month=1, day=30, hour=19, minute=14))
m = earth.get_moment(datetime(year=1593, month=8, day=25, hour=17, minute=30))
# m = earth.get_moment(datetime(year=1595, month=10, day=31, hour=0, minute=39))

# print (m.distance, m.longtitude, m.mean_longtitude)

#observation 1587 (removed 8 sec from value bacauce we need Mars to be on pehekion,
# and it happend 2 month earlier ); but I decided to leave ir
mars_aphelion = Angle.from_zondiac_to_number(Zodiac.LEO, deg=28, min=48, sec=45) #

# mars_aphelion_date = datetime(year=1587, month=1, day=13, hour=11, minute=26, second=25) # we need to add 3.55 from what in the table
mars_aphelion_date = datetime(year=1587, month=1, day=4, hour=3, minute=46, second=10)
# difficult to pin point. it is not accurate. but within 1 minute
mars = Eccentric(eccentricity=11332, aequant_eccentricity=7232, aphelion=mars_aphelion,
                  apehlion_time=mars_aphelion_date, orbit_time=686.9963, aphelion_seconds_movement_a_year=16)

# m = mars.get_moment(datetime(year=1587, month=3, day=6, hour=7, minute=23))
m = mars.get_moment(datetime(year=1597, month=12, day=13, hour=15, minute=44))
m2 = mars.get_moment(datetime(year=1604, month=3, day=28, hour=16, minute=23))
print (m.distance, m.longtitude, m.mean_longtitude)
print (m.distance, m2.longtitude, m2.mean_longtitude)

def get_expected_latitude(time, radius_ratio=1.519, earth_eccentricity=1792):
    # original_earth_eccentricity = earth.eccentricity
    earth.eccentricity = earth_eccentricity
    # earth.aequant_eccentricity = original_earth_eccentricity - earth_eccentricity

    # bisicate mars:
    # semi_mars = (mars.aequant_eccentricity + mars.eccentricity) / 2
    # mars.aequant_eccentricity = semi_mars
    # mars.eccentricity = semi_mars

    mars_latitude_from_sun = get_latitude_of_mars_from_sun_by_date(time)
    earth_sun_distance = earth.get_moment(time).distance / radius_ratio
    mars_sun_distance = mars.get_moment(time).distance

    # triable SUn-earh-mars
    earth_mars_distance = math.sqrt(earth_sun_distance**2 + mars_sun_distance**2
                                    - 2*earth_sun_distance*mars_sun_distance*math.cos(math.radians(mars_latitude_from_sun)))

    mars_angle = math.asin(math.sin(math.radians(mars_latitude_from_sun)) * earth_sun_distance / earth_mars_distance)
    mars_angle = math.degrees(mars_angle)
    mars_latitude_from_earth = mars_angle + mars_latitude_from_sun#external

    return mars_latitude_from_earth


# No sign
# also we use time of the model - not the longtitude from observation.
# not best accuracy - but we don't need accuracy here
def get_latitude_of_mars_from_sun_by_date(time):
    longtitude = mars.get_moment(time).longtitude
    limit_distance = max(abs(longtitude-MARS_LIMITS[0]), abs(longtitude-MARS_LIMITS[1]))
    return abs(math.cos(math.radians(limit_distance)) * MARS_ANGLE)



def check_latitude_observations(observation_times, radius_ratio=1.519, earth_eccentricity=1792):
    for ob in observations_times:
        # print (get_latitude_of_mars_from_sun_by_date(ob))
        print (get_expected_latitude(ob, radius_ratio=radius_ratio, earth_eccentricity=earth_eccentricity))

observations_times = [datetime(year=1585, month=1, day=30, hour=19, minute=14),
                      datetime(year=1593, month=8, day=25, hour=17, minute=27)]

check_latitude_observations(observations_times, radius_ratio=1.5225, earth_eccentricity=0)