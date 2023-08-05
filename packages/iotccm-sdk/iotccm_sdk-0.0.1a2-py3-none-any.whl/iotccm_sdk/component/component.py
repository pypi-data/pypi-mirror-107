import logging
import json
import re
from pathlib import Path
from ..capability.capability import Capability
from ..capability.actuator_capability import ActuatorCapability
from ..capability.sensor_capability import SensorCapability

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-5.5s] %(message)s")


class Component:

    DEAFULT_CONFIG_FILE = "config_sample.json"

    def __init__(self, name=None, config_file=DEAFULT_CONFIG_FILE) -> None:
        self.config = dict()
        self.config["name"] = name
        self.config["environment"] = None
        self.config["system"] = None
        self.capabilities = dict()
        self.load_config(config_file)
        logging.info("New component created!")

    def __repr__(self) -> str:
        return f"Component {self.id} has {len(self.capabilities)} capabilities."

    @property
    def environment(self):
        return self.config["environment"]

    @property
    def system(self):
        return self.config["system"]

    @property
    def name(self):
        return self.config["name"]
    
    @name.setter
    def name(self, name):
        if not re.match(r"^[a-zA-Z0-9_\-\.\!\~\*\'\(\)]*$", name):
            raise ValueError
        self.config["name"] = name
    
    @property
    def id(self):
        """
        Creates the component id out of the environment, system and name.
        :return: the component id
        :rtype: string
        """
        return self.environment + ":" + self.system + ":" + self.name
    
    def add_capability(self, name, capability):
        """
        Adds the given capability to the component capabilities.
        """
        if not isinstance(capability, Capability):
            raise AttributeError(f"Attribute capability must be of type {Capability.__class__}")
        self.capabilities[name] = capability

    def get_capability(self, name):
        """
        Returns the capability for the corresponding given name.
        """
        return self.capabilities[name]

    def get_capabilities_list(self):
        """
        Returns a list of the component capabilities.
        """
        caps_list = []
        for cap in self.capabilities:
            caps_list.append(cap)
        return caps_list

    def run(self):
        for key in self.capabilities:
            if isinstance(self.capabilities[key], ActuatorCapability):
                self.capabilities[key].start_actuator()
            if isinstance(self.capabilities[key], SensorCapability):
                self.capabilities[key].start_sensor()

    def load_config(self, config_file=DEAFULT_CONFIG_FILE):
        """
        Loads component configuration from local config file.
        """
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        logging.debug(f"Loaded component configuration from {config_file}")

    @staticmethod
    def has_config_file():
        """
        Checks if there is an existing config file.
        :return: whether a config file exists or no
        :rtype: boolean
        """
        if Path(Component.DEAFULT_CONFIG_FILE).is_file():
            return True
        return False