"""
    Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Joshua Sutcliffe
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Unit test to ensure available spaces does not go below zero.
    Test currently does not run: CarPark object runs (confirmed by MQTT message) but then test just spins forever.
    Manual testing of this feature confirms no negative spaces.
"""

import unittest
from simple_mqtt_carpark import CarPark
from config_parser import parse_config


class TestParkingLot(unittest.TestCase):
    def test_no_negative_spaces(self):
        config = parse_config()
        carpark = CarPark(config)
        while carpark.available_spaces > -2:
            carpark.on_car_entry()
        self.assertEqual(carpark.available_spaces, 0)
        carpark.on_car_exit()
        carpark.on_car_exit()
        self.assertEqual(carpark.available_spaces, 1)
