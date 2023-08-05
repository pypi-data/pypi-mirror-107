import logging
from threading import Thread
from .capability import Capability

class ActuatorCapability(Capability):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actuator_name = None
        self.actuator_config = None
    
    def setup_actuator(self, actuator_name, actuator_config):
        self.actuator_name = actuator_name
        self.actuator_config = actuator_config

    def start_actuator(self, **kwargs):
        logging.info("Starting actuator " + self.actuator_name)
        thread = Thread(target=self.actuate, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    def actuate(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def configure_actuator():
        raise NotImplementedError