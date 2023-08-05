
import logging
import time
from iotccm_sdk.capability.sensor_capability import SensorCapability

class MotionDetectionCapability(SensorCapability):
    def start_sensor(self, **kwargs):
        pin = int(self.sensor_config["pin"])
        logging.info(f"PIR sensor connected to pin#{pin}")
        super().start_sensor(pin=pin)
    
    def sense(self, **kwargs):
        motion_detected = True
        while True:
            if motion_detected:
                logging.info("Motion detected!")
            time.sleep(2)

    @staticmethod
    def configure_sensor():
        print("Configuring the motion detection sensor:")
        pin = int(input("Which pin on the Raspberry Pi the Motion sensor is connected to? "))
        return {
            "pin": pin
        }
