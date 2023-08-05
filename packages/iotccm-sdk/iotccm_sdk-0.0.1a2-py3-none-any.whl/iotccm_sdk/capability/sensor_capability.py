import logging
from threading import Thread
from .capability import Capability

class SensorCapability(Capability):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sensor_name = None
        self.sensor_config = None
        self.specifications = dict()
    
    def add_spec(self, spec_key, spec_value):
        self.specifications[spec_key] = spec_value

    def setup_sensor(self, sensor_name, sensor_config):
        self.sensor_name = sensor_name
        self.sensor_config = sensor_config

    def start_sensor(self, **kwargs):
        logging.info("Starting sensor " + self.sensor_name)
        thread = Thread(target=self.sense, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    def sense(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def configure_sensor():
        raise NotImplementedError