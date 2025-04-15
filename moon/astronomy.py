# Copyright (c) 2025 Damien Boisvert (AlphaGameDeveloper)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import ephem
import datetime

class Astronomy:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.observer = ephem.Observer()
        self.observer.lat = str(latitude)
        self.observer.lon = str(longitude)

    def compute_moonrise(self):
        moon = ephem.Moon()
        moon.compute(self.observer)
        moonrise = self.observer.next_rising(moon)
        return moonrise

    def compute_moonset(self):
        moon = ephem.Moon()
        moon.compute(self.observer)
        moonset = self.observer.next_setting(moon)
        return moonset

if __name__ == "__main__":
    # testing
    latitude = 37.7749  # Example: San Francisco
    longitude = -122.4194
    astronomy = Astronomy(latitude, longitude)
    moonrise = astronomy.compute_moonrise()
    moonset = astronomy.compute_moonset()
    print(f"Moonrise: {moonrise}")
    print(f"Moonset: {moonset}")
    