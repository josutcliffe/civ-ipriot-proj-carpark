"""
    Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Joshua Sutcliffe
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Carpark object that defines the carpark attributes.
                Ensure mosquitto -v running in terminal.
"""

from datetime import datetime
import random
import mqtt_device
from config_parser import parse_config


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['config']['total-spaces']
        self.total_cars = config['config']['total-cars']
        self.client.subscribe('lot/sensor')
        self.client.on_message = self.on_message
        self.client.loop_forever()
        self._temperature = 0

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        self.temperature = random.randint(0, 45)
        print(
            (
                    f"TIME: {readable_time} "
                    + f"SPACES: {self.available_spaces} "
                    + f"TEMPERATURE: {self.temperature}"
            )
        )
        message = (
                f"TIME: {readable_time} "
                + f"SPACES: {self.available_spaces} "
                + f"TEMPERATURE: {self.temperature}"
        )
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, message):
        payload = message.payload.decode()
        print(f"Message received:")
        if 'exit' in payload:
            self.on_car_exit()
        else:
            self.on_car_entry()


if __name__ == '__main__':
    config = parse_config()
    print("Carpark initialised")
    car_park = CarPark(config)
