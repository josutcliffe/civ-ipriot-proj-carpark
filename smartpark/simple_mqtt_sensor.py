""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
import random
import tkinter as tk
import mqtt_device
import paho.mqtt.client as mqtt

from config_parser import parse_config


class Sensor(mqtt_device.MqttDevice):

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘', font=('Arial', 50), cursor='bottom_left_corner',
            command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    @property
    def temperature(self):
        """Returns the current temperature"""
        return random.randint(10, 35)

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        self.client.publish('sensor', message)

    def start_sensing(self):
        """ A blocking event loop that waits for detection events, in this
        case Enter presses"""
        while True:
            print("Press E when 🚗 entered!")
            print("Press X when 🚖 exited!")
            detection = input("E or X> ").upper()
            if detection == 'E':
                self.on_detection(f"entered, {self.temperature}")
            else:
                self.on_detection(f"exited, {self.temperature}")

    def incoming_car(self):
        # TODO: implement this method to publish the detection via MQTT
        client = mqtt.Client('sensor')
        print(client)
        broker = config['config']['broker']
        port = config['config']['port']
        print(broker)
        print(port)
        client.connect(broker, port)
        client.publish('lot/sensor', 'entry')
        print("Car goes in")
        client.loop()

    def outgoing_car(self):
        # TODO: implement this method to publish the detection via MQTT
        client = mqtt.Client('sensor')
        print(client)
        broker = config['config']['broker']
        port = config['config']['port']
        print(broker)
        print(port)
        client.connect(broker, port)
        client.publish('lot/sensor', 'exit')
        print("Car goes out")
        client.loop()


if __name__ == '__main__':
    # TODO: Read previous config from file instead of embedding
    config = parse_config()
    print("Loading incoming/outgoing car display")
    Sensor()
