import logging
import time
import random
from iotccm_sdk.capability.sensor_capability import SensorCapability

class Dht11Capability(SensorCapability):
    def start_sensor(self, **kwargs):
        pin = int(self.sensor_config["pin"])
        model = int(self.sensor_config["model"])
        logging.info(f"Starting temperature reading on pin#{pin}...")
        super().start_sensor(pin=pin, model=model)

    def sense(self, pin, model):
        while True:
            temp = round(random.uniform(22.5, 22.7), 1)
            logging.info(f"DHT11 - {self.sensor_name} - temperature = {temp}")
            time.sleep(2)

    @staticmethod
    def configure_sensor():
        # print("Configuring DHT11 Sensor:")
        model = int(
            input("What is the model of your DHT11 Sensor? (Blue=0, White=1)? ")
        )
        pin = int(
            input("Which pin on the Raspberry Pi the DHT11 sensor is connected to? ")
        )
        return {
            "model": model,
            "pin": pin,
        }
