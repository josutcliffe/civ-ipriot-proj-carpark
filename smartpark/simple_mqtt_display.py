import mqtt_device
import time
import random
import threading
import time
import tkinter as tk
from typing import Iterable
from config_parser import parse_config


# ------------------------------------------------------------------------------------#
# You don't need to understand how to implement this class, just how to use it.       #
# ------------------------------------------------------------------------------------#
# TODO: got to the main section of this script **first** and run the CarParkDisplay.  #


class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):
            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field + self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()


class Display(mqtt_device.MqttDevice):
    """Displays the number of cars and the temperature"""
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self, config):
        self.temperature = 0
        self.available_spaces = 192
        super().__init__(config)
        self.window = WindowedDisplay(
            'Moondalup', Display.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def on_message(self, client, userdata, message):
        payload = message.payload.decode()
        self.display(*payload.split(','))
        temperature = payload.strip().split()[5]
        self.temperature = temperature
        print(temperature)
        available_spaces = payload.strip().split()[3]
        self.available_spaces = available_spaces
        print(available_spaces)

    def check_updates(self):
        self.client.subscribe('display')
        self.client.on_message = self.on_message
        self.client.loop_start()
        # TODO: This is where you should manage the MQTT subscription
        while True:
            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(Display.fields, [
                f'{int(self.available_spaces):03d}',
                f'{int(self.temperature):02d}℃',
                time.strftime("%H:%M:%S")]))
            # Pretending to wait on updates from MQTT
            # time.sleep(random.randint(1, 10))
            # When you get an update, refresh the display.
            self.window.update(field_values)

    # def on_message(self, client, userdata, message):
    #     payload = message.payload.decode()
    #     self.display(*payload.split(','))
    #     temperature = payload.strip().split()[1]
    #     self.temperature = temperature
    #     print(self.temperature)
    #     available_spaces = payload.strip().split()[3]
    #     print(available_spaces)
    #     timestamp = payload.strip().split()[5]
    #     print(timestamp)
    #     # TODO: Parse the message and extract free spaces,\
    #     #  temperature, time

    def display(self, *args):
        print('*' * 20)
        for val in args:
            print(val)
            time.sleep(1)

        print('*' * 20)


if __name__ == '__main__':
    # TODO: Read config from file
    config = parse_config()
    display = Display(config)
