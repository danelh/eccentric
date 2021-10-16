from angles import Angle, Zodiac
from eccentric import Eccentric
from datetime import datetime

# Earth eccentricity according to Tycho/Copernicus:
# See ch. 17 Mars vs Earth radius is 1.519
# Now in ch. 5 (p.99) Earth eccentricity 3584 of 100000 Mars radius,
# so Earth eccebtricity in Earth radius is 5444 of 100000 Earth Radius
# NO, 3584 is the figure for Earth 100000.
# Accorfing to TBOO 2. p.46 & 83 and observation 1579 Dec it seems
# the perigee (Earh seen from Sun) is about Cancer 4-5 deg. in about 15 Dec.
# the apogee seen from the Sun will be Capricon 5 deg.
earth_aphelion = Angle.from_zondiac_to_number(Zodiac.CAPRICON, deg=5)
aphelion_date = datetime(year=1590, month=6, day=15)
earth = Eccentric(eccentricity=3584, aequant_eccentricity=0, aphelion=earth_aphelion,
                  apehlion_time=aphelion_date, orbit_time=365.25)
m = earth.get_moment(datetime(year=1585, month=1, day=30))
# m = earth.get_moment(datetime(year=1593, month=8, day=25))
print (m.distance, m.longtitude, m.mean_longtitude)