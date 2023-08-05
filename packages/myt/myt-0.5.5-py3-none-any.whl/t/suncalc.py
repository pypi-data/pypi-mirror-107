# Mostly from https://github.com/Broham/suncalcPy/blob/master/suncalc.py
# Updated for Python 3

import math
from datetime import datetime, timedelta, timezone
import time
import calendar

_rad = math.pi / 180.0
dayMs = 1000 * 60 * 60 * 24
J1970 = 2440588
J2000 = 2451545
J0 = 0.0009

_times = [
    [-0.833*_rad, "sunrise", "sunset"],
    [-0.3*_rad, "sunriseEnd", "sunsetStart"],
    [-6*_rad, "dawn", "dusk"],
    [-12*_rad, "nauticalDawn", "nauticalDusk"],
    [-18*_rad, "nightEnd", "night"],
    [6*_rad, "goldenHourEnd", "goldenHour"],
]

_e = _rad * 23.4397  # obliquity of the Earth


def rightAscension(l, b):
    return math.atan2(math.sin(l) * math.cos(_e) - math.tan(b) * math.sin(_e), math.cos(l))


def declination(l, b):
    return math.asin(math.sin(b) * math.cos(_e) + math.cos(b) * math.sin(_e) * math.sin(l))


def azimuth(H, phi, dec):
    return math.atan2(math.sin(H), math.cos(H) * math.sin(phi) - math.tan(dec) * math.cos(phi))


def altitude(H, phi, dec):
    return math.asin(math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.cos(H))


def siderealTime(d, lw):
    return _rad * (280.16 + 360.9856235 * d) - lw


def toJulian(date):
    return (time.mktime(date.timetuple()) * 1000) / dayMs - 0.5 + J1970


def fromJulian(j):
    #fromtimestamp returns local time unless tz is specified
    return datetime.fromtimestamp(((j + 0.5 - J1970) * dayMs) / 1000.0, tz=timezone.utc)


def toDays(date):
    return toJulian(date) - J2000


def julianCycle(d, lw):
    return round(d - J0 - lw / (2 * math.pi))


def approxTransit(Ht, lw, n):
    return J0 + (Ht + lw) / (2 * math.pi) + n


def solarTransitJ(ds, M, L):
    return J2000 + ds + 0.0053 * math.sin(M) - 0.0069 * math.sin(2 * L)


def hourAngle(h, phi, d):
    try:
        ret = math.acos((math.sin(h) - math.sin(phi) * math.sin(d)) / (math.cos(phi) * math.cos(d)))
        return ret
    except ValueError as e:
        print(h, phi, d)
        print(e)

def observerAngle(height):
    return (-2.076 * math.sqrt(height)/60.0)*_rad

def solarMeanAnomaly(d):
    return _rad * (357.5291 + 0.98560028 * d)


def eclipticLongitude(M):
    C = _rad * (
        1.9148 * math.sin(M) + 0.02 * math.sin(2 * M) + 0.0003 * math.sin(3 * M)
    )  # equation of center
    P = _rad * 102.9372  # perihelion of the Earth
    return M + C + P + math.pi


def sunCoords(d):
    M = solarMeanAnomaly(d)
    L = eclipticLongitude(M)
    return dict(dec=declination(L, 0), ra=rightAscension(L, 0))


def getSetJ(h, lw, phi, dec, n, M, L):
    '''

    :param h:
    :param lw: longitude, radians
    :param phi: latitude, radians
    :param dec: declination
    :param n: julian cycle
    :param M: solar mean anomaly
    :param L: ecliptic longitude
    :return:
    '''
    w = hourAngle(h, phi, dec)
    a = approxTransit(w, lw, n)
    return solarTransitJ(a, M, L)


# geocentric ecliptic coordinates of the moon
def moonCoords(d):
    L = _rad * (218.316 + 13.176396 * d)
    M = _rad * (134.963 + 13.064993 * d)
    F = _rad * (93.272 + 13.229350 * d)

    l = L + _rad * 6.289 * math.sin(M)
    b = _rad * 5.128 * math.sin(F)
    dt = 385001 - 20905 * math.cos(M)

    return dict(ra=rightAscension(l, b), dec=declination(l, b), dist=dt)


def getMoonIllumination(date):
    d = toDays(date)
    s = sunCoords(d)
    m = moonCoords(d)

    # distance from Earth to Sun in km
    sdist = 149598000
    phi = math.acos(
        math.sin(s["dec"]) * math.sin(m["dec"])
        + math.cos(s["dec"]) * math.cos(m["dec"]) * math.cos(s["ra"] - m["ra"])
    )
    inc = math.atan2(sdist * math.sin(phi), m["dist"] - sdist * math.cos(phi))
    angle = math.atan2(
        math.cos(s["dec"]) * math.sin(s["ra"] - m["ra"]),
        math.sin(s["dec"]) * math.cos(m["dec"])
        - math.cos(s["dec"]) * math.sin(m["dec"]) * math.cos(s["ra"] - m["ra"]),
    )

    return dict(
        fraction=(1 + math.cos(inc)) / 2,
        phase=0.5 + 0.5 * inc * (-1 if angle < 0 else 1) / math.pi,
        angle=angle,
    )


def getSunrise(date, lat, lng):
    ret = getTimes(date, lat, lng)
    return ret["sunrise"]


def getTimes(date, lat, lng, height=0.0):
    if height < 0.0:
        height = 0.0
    obs_angle = observerAngle(height)
    lw = _rad * -lng
    phi = _rad * lat
    d = toDays(date)
    n = julianCycle(d, lw)
    ds = approxTransit(0, lw, n)
    M = solarMeanAnomaly(ds)
    L = eclipticLongitude(M)
    dec = declination(L, 0)
    Jnoon = solarTransitJ(ds, M, L)
    result = dict()
    for tt in _times:
        Jset = getSetJ(tt[0] + obs_angle, lw, phi, dec, n, M, L)
        Jrise = Jnoon - (Jset - Jnoon)
        result[tt[1]] = fromJulian(Jrise)
        result[tt[2]] = fromJulian(Jset)
    return result


def hoursLater(date, h):
    return date + +timedelta(hours=h)


def getMoonTimes(date, lat, lng):
    t = date.replace(hour=0, minute=0, second=0)
    hc = 0.133 * _rad
    pos = getMoonPosition(t, lat, lng)
    h0 = pos["altitude"] - hc
    rise = 0
    sett = 0
    # go in 2-hour chunks, each time seeing if a 3-point quadratic curve crosses zero (which means rise or set)
    for i in range(1, 24, 2):
        h1 = getMoonPosition(hoursLater(t, i), lat, lng)["altitude"] - hc
        h2 = getMoonPosition(hoursLater(t, i + 1), lat, lng)["altitude"] - hc

        a = (h0 + h2) / 2 - h1
        b = (h2 - h0) / 2
        xe = -b / (2 * a)
        ye = (a * xe + b) * xe + h1
        d = b * b - 4 * a * h1
        roots = 0
        if d >= 0:
            dx = math.sqrt(d) / (abs(a) * 2)
            x1 = xe - dx
            x2 = xe + dx
            if abs(x1) <= 1:
                roots += 1
            if abs(x2) <= 1:
                roots += 1
            if x1 < -1:
                x1 = x2
        if roots == 1:
            if h0 < 0:
                rise = i + x1
            else:
                sett = i + x1
        elif roots == 2:
            rise = i + (x2 if ye < 0 else x1)
            sett = i + (x1 if ye < 0 else x2)
        if rise and sett:
            break
        h0 = h2
    result = dict()
    if rise:
        result["rise"] = hoursLater(t, rise)
    if sett:
        result["set"] = hoursLater(t, sett)
    if not rise and not sett:
        value = "alwaysUp" if ye > 0 else "alwaysDown"
        result[value] = True
    return result


def getMoonPosition(date, lat, lng):
    lw = _rad * -lng
    phi = _rad * lat
    d = toDays(date)
    c = moonCoords(d)
    H = siderealTime(d, lw) - c["ra"]
    h = altitude(H, phi, c["dec"])
    # altitude correction for refraction
    h = h + _rad * 0.017 / math.tan(h + _rad * 10.26 / (h + _rad * 5.10))
    return dict(azimuth=azimuth(H, phi, c["dec"]), altitude=h, distance=c["dist"])


def getPosition(date, lat, lng):
    lw = _rad * -lng
    phi = _rad * lat
    d = toDays(date)
    c = sunCoords(d)
    H = siderealTime(d, lw) - c["ra"]
    return dict(azimuth=azimuth(H, phi, c["dec"]), altitude=altitude(H, phi, c["dec"]))


# def getMoonAndSunrise(date, lat, lng):
#   # print(date,lat,lng)
#   currentDate = datetime.strptime(date,'%Y-%m-%d %H:%M:%S');
#   times = getTimes(currentDate, float(lat), float(lng))
#   moon = getMoonIllumination(currentDate)
#   sunrise = datetime.strptime(times["sunrise"],'%Y-%m-%d %H:%M:%S')
#   fraction = float(moon["fraction"])
#   return dict(sunrise=sunrise, fraction=fraction)

# testDate = datetime.strptime('2015-04-17 17:00:00','%Y-%m-%d %H:%M:%S')
# sunTimes = getTimes(testDate, 37.7745985956747,-122.425891675136)

# data = getMoonAndSunrise('2015-04-17 17:00:00', "37.7745985956747","-122.425891675136")

# print(testDate.strftime('%Y-%m-%d %H:%M:%S'), data["sunrise"].strftime('%Y-%m-%d %H:%M:%S'))
# print(data["fraction"])
