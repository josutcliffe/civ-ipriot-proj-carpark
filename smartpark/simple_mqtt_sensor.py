"""
    Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Joshua Sutcliffe
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Sensor class to simulate cars entering and exiting car park
                Ensure mosquitto -v running in terminal.
"""

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

    def incoming_car(self):
        client = mqtt.Client('sensor')
        broker = config['config']['broker']
        port = config['config']['port']
        client.connect(broker, port)
        client.publish('lot/sensor', 'entry')
        print("Car goes in")
        client.loop()

    def outgoing_car(self):
        client = mqtt.Client('sensor')
        broker = config['config']['broker']
        port = config['config']['port']
        client.connect(broker, port)
        client.publish('lot/sensor', 'exit')
        print("Car goes out")
        client.loop()


if __name__ == '__main__':
    config = parse_config()
    print("Loading incoming/outgoing car simulator")
    Sensor()
