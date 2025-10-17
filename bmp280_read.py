# bmp280_read.py
from machine import Pin, I2C
import bmp280
import math

class BMP280Sensor:
    def __init__(self, scl=22, sda=21):
        # Initialize I2C (change pins if needed)
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda))
        self.bmp = bmp280.BMP280(self.i2c)
        self.sea_level_pressure = 1013.25  # hPa (standard sea-level pressure)

    def read_data(self):
        temp = self.bmp.temperature
        pres = self.bmp.pressure
        alt = self.calculate_altitude(pres)
        return temp, pres, alt

    def calculate_altitude(self, pressure):
        """Calculate altitude from pressure (in meters)."""
        altitude = 44330 * (1 - (pressure / self.sea_level_pressure) ** (1 / 5.255))
        return altitude
