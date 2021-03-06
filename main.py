import math

from angles import Angle, Zodiac
from eccentric import Eccentric, Ellipse
from datetime import datetime, timedelta

MARS_ANGLE = 1.83333333
MARS_LIMITS = [Angle.from_zondiac_to_number(Zodiac.LEO, deg=16, min=30),
               Angle.from_zondiac_to_number(Zodiac.AQUARIUS, deg=16, min=30)]

def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

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

def get_expected_latitude(time, radius_ratio=1.519, earth_eccentricity=1792, mars_ratio=None):
    # original_earth_eccentricity = earth.eccentricity
    earth.eccentricity = earth_eccentricity
    # earth.aequant_eccentricity = original_earth_eccentricity - earth_eccentricity


    mars_latitude_from_sun = get_latitude_of_mars_from_sun_by_date(time)

    # bisicate mars (after we got latitude from sun):
    if mars_ratio:
        total_mars_eccentricity = mars.aequant_eccentricity + mars.eccentricity
        mars.eccentricity = total_mars_eccentricity * mars_ratio
        mars.aequant_eccentricity = total_mars_eccentricity - mars.eccentricity
    # semi_mars = (mars.aequant_eccentricity + mars.eccentricity) / 2
    # mars.aequant_eccentricity = semi_mars
    # mars.eccentricity = semi_mars


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



def check_latitude_observations(observation_times, radius_ratio=1.519, earth_eccentricity=1792,
                                mars_ratio=None):
    for ob in observations_times:
        # print (get_latitude_of_mars_from_sun_by_date(ob))
        print (get_expected_latitude(ob, radius_ratio=radius_ratio, earth_eccentricity=earth_eccentricity,
                                     mars_ratio=mars_ratio))

observations_times = [datetime(year=1585, month=1, day=30, hour=19, minute=14),
                      datetime(year=1593, month=8, day=25, hour=17, minute=27),
                      datetime(year=1600, month=1, day=18, hour=14, minute=2),
                      datetime(year=1591, month=6, day=8, hour=7, minute=43)]

# ratio is eccnetricy/aequant_eccenntricity. in the model the ratio is 0.61
def shrink_mars_eccentricity(new_eccentricity_ratio):
    # we want quator a "year" in 10 peaces
    kepler_example_time = datetime(year=1582, month=12, day=28, hour=3, minute=58)
    # kepler_example_time = datetime(year=1593, month=8, day=25, hour=17, minute=27)
    # kepler_example_time = datetime(year=1582, month=12, day=28, hour=0, minute=58)
    spots_count = 1000
    seconds_in_section = (mars.orbit_time / 1.0) / spots_count
    times = [mars.aphelion_time + timedelta(seconds=seconds_in_section)*i for i in range(spots_count)]
    original_longtitudes = [mars.get_moment(time).longtitude for time in times]
    original_kepler_long = mars.get_moment(kepler_example_time).longtitude
    total_mars_eccentricity = mars.aequant_eccentricity + mars.eccentricity
    mars.eccentricity = total_mars_eccentricity * new_eccentricity_ratio
    mars.aequant_eccentricity = total_mars_eccentricity - mars.eccentricity
    new_kepler_long = mars.get_moment(kepler_example_time).longtitude
    new_longtitudes = [mars.get_moment(time).longtitude for time in times]
    diff = [decdeg2dms(abs(new_longtitudes[i]-original_longtitudes[i])) for i in range(spots_count)]
    print (original_longtitudes)
    print (new_longtitudes)
    # print (max(diff))
    print (original_kepler_long, new_kepler_long)
    print ("max diff:{}".format(max(diff)))
    print ("diff in Kepler example: {}".format(decdeg2dms(new_kepler_long - original_kepler_long)))

def compare_tycho_and_kepler_earth():
    _ecc = 3584
    _earth_aphelion = Angle.from_zondiac_to_number(Zodiac.CAPRICON, deg=4)
    _earth_aphelion_date = datetime(year=1590, month=6, day=15, hour=19, minute=37)
    tycho = Eccentric(eccentricity=_ecc, aequant_eccentricity=0, aphelion=_earth_aphelion,
                      apehlion_time=_earth_aphelion_date, orbit_time=365.25)
    kepler = Eccentric(eccentricity=_ecc/2, aequant_eccentricity=_ecc/2, aphelion=_earth_aphelion,
                      apehlion_time=_earth_aphelion_date, orbit_time=365.25)
    # kepler = Eccentric(eccentricity=1670, aequant_eccentricity=1670, aphelion=_earth_aphelion,
    #                   apehlion_time=_earth_aphelion_date, orbit_time=365.25)

    spots_count = 1000
    seconds_in_section = (tycho.orbit_time / 1.0) / spots_count
    times = [mars.aphelion_time + timedelta(seconds=seconds_in_section) * i for i in range(spots_count)]

    tycho_longtitudes = [tycho.get_moment(time).longtitude for time in times]
    kepler_longtitudes = [kepler.get_moment(time).longtitude for time in times]
    tycho_distances = [tycho.get_moment(time).distance for time in times]
    kepler_distances = [kepler.get_moment(time).distance for time in times]

    diff = [decdeg2dms(abs(kepler_longtitudes[i]-tycho_longtitudes[i])) for i in range(spots_count)]
    print ("max diff:{}".format(max(diff)))
    diff_distance = [abs(kepler_distances[i]-tycho_distances[i]) for i in range(spots_count)]
    print ("max diff:{}".format(max(diff_distance)))

    # what happens in 90 deg mean longtitude?
    test_time = timedelta(days=138*365.25/360) + _earth_aphelion_date
    kepler_test_moment = kepler.get_moment(test_time)
    tycho_test_moment = tycho.get_moment(test_time)
    print (kepler_test_moment.mean_longtitude - _earth_aphelion, tycho_test_moment.mean_longtitude)
    print(kepler_test_moment.longtitude, tycho_test_moment.longtitude)
    print (decdeg2dms(abs(kepler_test_moment.longtitude - tycho_test_moment.longtitude)))

# check_latitude_observations(observations_times, radius_ratio=1.52, earth_eccentricity=2000,
#                             mars_ratio=0.55)

# shrink_mars_eccentricity(0.50)

def check_ellipse():
    p_phelion = Angle.from_zondiac_to_number(Zodiac.ARIES, deg=0)
    p_phelion_date = datetime(year=1590, month=6, day=15, hour=19, minute=37)
    p = Ellipse(eccentricity=0.016, semi_major_axis=1, phelion=p_phelion,
                pehlion_time=p_phelion_date, orbit_time=365.25)
    times = [p_phelion_date + timedelta(days=1) * i for i in range(365)]

    for time in times:
        moment = p.get_moment(time)
        print (moment.mean_longtitude, moment.longtitude, moment.center_angle, moment.longtitude-moment.mean_longtitude)


check_ellipse()
