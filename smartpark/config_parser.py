"""
    Course:     ICT40120 Cert IV in IT (Programming)
    Name:       Joshua Sutcliffe
    Unit:       IP4RIoT (Cluster)
    Assessment: AT3 Project
    Date:       June 2023
    Purpose:    Parser code that returns values of config file, to initialise CarPark, Display and Sensor.
                Ensure mosquitto -v running in terminal.
"""


def parse_config() -> dict:
    """Parse the config file and return the values as a dictionary"""
    import tomli
    with open("../smartpark/config.toml", "r") as file:
        config_string = file.read()

    config = tomli.loads(config_string)
    return config
