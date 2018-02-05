# calculate weather information
from math import exp

def saettigungsdampfdruck(t):
    """
    Using the Magnus Formular above Water

    Valid for -45 <= t <= 60

    From: https://de.wikipedia.org/wiki/S%C3%A4ttigungsdampfdruck#%C3%9Cber_ebenen_Wasseroberfl%C3%A4chen
    """
    if t < -45 or t > 60:
        raise ValueError("Can not use formular for such a value")
    return 6.112 * exp((17.62 * t) / (243.12 + t))

def steam_pressure(t, h):
    """
    Get the steam pressure for water in air
    for a given temperature in degree C and humidity in %RH

    This is the same as the absolute humidity

    From: https://de.wikipedia.org/wiki/Luftfeuchtigkeit#Relative_Luftfeuchtigkeit
    by solving phi = e/E for e
    """
    E = saettigungsdampfdruck(t)

    return (h / 100.0) * E

def steam_density(t, h):
    """
    Get the steam density from the steam pressure
    """

    R_w = 461.52  # J * kg**-1 * K**-1
    T = t + 273.15  # K
    e = steam_pressure(t, h)

    return e / (R_w * T)


def reduced_pressure(p, t, hum, height=162.0):
    """
    p ... pressure
    t ... temperature
    h ... humidity

    From: https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henformel#Reduktion_auf_Meeresh%C3%B6he
    """

    g_0 = 9.80665  # m * s**-2
    R = 287.05  # m**2 * s**-2 * K**-1
    #h = 160.425  # m  ... Above Adria
    T = t + 273.15  # K
    a = 0.0065  # K * m**-1
    # This is the absolute pressure of water (partial pressure of water in air)
    e = steam_pressure(t, hum)
    C_h = 0.12  # K * hPa**-1

    x = g_0 / (R * (T + C_h * e + a * (height/2))) * height
    return p * exp(x)

