from math import sqrt

__author__ = 'thanatv'


class Attenuation(object):
    """
    Defines an atmospheric attenuation based on ITU-R
    """
    def __init__(self, frequency, elevation, antenna_diameter,
                 link_availability, lat, lon, antenna_efficiency=0.5, atmospheric_pressure=1, surface_temp=27, humidity=99):
        self.frequency = frequency
        self.elevation = elevation
        self.antenna_diameter = antenna_diameter
        self.link_availability = link_availability
        self.latitude = lat
        self.longitude = lon
        self.antenna_efficiency = antenna_efficiency
        self.atmospheric_pressure = atmospheric_pressure
        self.surface_temp = surface_temp
        self.humidity = humidity

    def cloud(self):
        """
        Returns cloud attenuation
        """
        return 0

    def gas(self):
        """
        Returns gas attenuation
        """
        return 0

    def scin(self):
        """
        Returns scin attenuation
        """
        return 0

    def rain(self):
        """
        Returns rain attenuation
        """
        return 0

    def total_clear_sky(self):
        """
        Return total attenuation during clear sky
        """
        if self.elevation > 10:
            return self.gas() + self.cloud()
        else:
            return self.gas() + sqrt(self.cloud() ** 2 + self.scin() ** 2)

    def total_rain(self):
        """
        Return total attenuation during rain
        """
        return self.gas() + sqrt((self.rain() + self.cloud()) ** 2 + self.scin() ** 2)