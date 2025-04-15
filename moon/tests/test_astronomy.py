# Copyright (c) 2025 Damien Boisvert (AlphaGameDeveloper)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import ephem
from datetime import datetime
import sys
import os

# Add parent directory to path to import astronomy module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from astronomy import Astronomy

class TestAstronomy(unittest.TestCase):
    def setUp(self):
        # San Francisco coordinates
        self.latitude = 37.7749
        self.longitude = -122.4194
        self.astronomy = Astronomy(self.latitude, self.longitude)
    
    def test_initialization(self):
        """Test if the Astronomy class initializes properly with given coordinates."""
        self.assertEqual(self.astronomy.latitude, self.latitude)
        self.assertEqual(self.astronomy.longitude, self.longitude)
        
        # ephem converts decimal degrees to a DMS (degrees:minutes:seconds) format
        # Convert back to float for approximate comparison
        lat_degrees = float(self.astronomy.observer.lat) * 180 / ephem.pi
        lon_degrees = float(self.astronomy.observer.lon) * 180 / ephem.pi
        
        # Use assertAlmostEqual with a small delta for floating point comparison
        self.assertAlmostEqual(lat_degrees, self.latitude, places=4)
        self.assertAlmostEqual(lon_degrees, self.longitude, places=4)
    
    def test_compute_moonrise(self):
        """Test if compute_moonrise returns a valid ephem.Date object."""
        moonrise = self.astronomy.compute_moonrise()
        self.assertIsInstance(moonrise, ephem.Date)
        
        # Convert to datetime for sanity check
        moonrise_dt = moonrise.datetime()
        self.assertIsInstance(moonrise_dt, datetime)
    
    def test_compute_moonset(self):
        """Test if compute_moonset returns a valid ephem.Date object."""
        moonset = self.astronomy.compute_moonset()
        self.assertIsInstance(moonset, ephem.Date)
        
        # Convert to datetime for sanity check
        moonset_dt = moonset.datetime()
        self.assertIsInstance(moonset_dt, datetime)
    
    def test_moonrise_moonset_sequence(self):
        """Test if moonrise and moonset timestamps make logical sense."""
        # Get current time
        now = ephem.now()
        
        # Get next moonrise and moonset
        next_moonrise = self.astronomy.compute_moonrise()
        next_moonset = self.astronomy.compute_moonset()
        
        # Both should be in the future
        self.assertGreaterEqual(next_moonrise, now)
        self.assertGreaterEqual(next_moonset, now)
        
        # If moonrise is before moonset, test a full cycle
        if next_moonrise < next_moonset:
            # Save the observer's date
            original_date = self.astronomy.observer.date
            
            # Set observer time to just after next_moonrise
            self.astronomy.observer.date = next_moonrise + ephem.hour
            
            # Get the next moonset
            after_rise_moonset = self.astronomy.compute_moonset()
            
            # Moonset should follow moonrise
            self.assertGreaterEqual(after_rise_moonset, next_moonrise)
            
            # Reset observer date
            self.astronomy.observer.date = original_date

if __name__ == '__main__':
    unittest.main()

