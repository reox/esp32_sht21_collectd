# calculate weather information
from math import exp

def saettigungsdampfdruck(t):
    """
    Using the Magnus Formular above Water

    Valid for -45 <= t <= 60
    """
    if t < -45 or t > 60:
        raise ValueError("Can not use formular for such a value")
    return 6.112 * exp((17.62 * t) / (243.12 + t))

def steam_pressure(t, h):
    """
    Get the steam pressure for water in air
    for a given temperature in degree C and humidity in %RH
    """
    E = saettigungsdampfdruck(t)

    return (h / 100.0) * E


def reduced_pressure(p, t, hum, height=162.0):
    """
    p ... pressure
    t ... temperature
    h ... humidity
    """

    g_0 = 9.80665  # m * s**-2
    R = 287.05  # m**2 * s**-2 * K**-1
    #h = 160.425  # m  ... Above Adria
    T = t + 273.15  # K
    a = 0.0065  # K * m**-1
    E = steam_pressure(t, hum)
    C_h = 0.12  # K * hPa**-1

    x = g_0 / (R * (T + C_h * E + a * (height/2))) * height
    return p * exp(x)

