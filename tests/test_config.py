"""
    Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Joshua Sutcliffe
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Unit test for parsing config file attributes
"""


import unittest
from config_parser import parse_config


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        """
        Unit test to check that config file has correct attributes such as location and total spaces
        [config]
        location = "Moondalup City Square Parking"
        total-spaces = 192
        """
        parking_lot = parse_config()
        self.assertEqual(parking_lot['config']['location'], "Moondalup City Square Parking")  # test for location name
        self.assertEqual(parking_lot['config']['total-spaces'], 192)  # test for total spaces
        self.assertGreater(parking_lot['config']['total-spaces'], 0)  # test that total spaces is greater than zero
