#!/usr/bin/env python

import logging
import asyncio
import os
from iotccm_sdk.component.component import Component
from examples.capabilities.capabilities import Capabilities
from examples import helpers
from examples.helpers import Entity

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-5.5s] %(message)s")


def give_name(entity):
    name = input("Choose a name for the new " + entity.value + ": ")
    name = helpers.input_should_match_regex("^[_a-zA-Z][_a-zA-Z0-9\-]*$", name)
    return name

def setup_component():
    """
    Displays a list of available capabilities the user can choose from.
    :return: None
    :rtype: None
    """
    print("Please choose a capability to be added to your component:")
    capability = helpers.choose_from_enum(Capabilities)

    # if it's a sensor capability
    try:
        configure = capability.value.configure_sensor
    except AttributeError:
        pass
    else:
        sensor_name = give_name(Entity.Sensor)
        sensor_config = configure()
        sensor_config["type"] = capability.name
        sensor_capability = Capabilities[capability.name].value(name=sensor_name)
        sensor_capability.setup_sensor(sensor_name, sensor_config)
        component.add_capability(sensor_name, sensor_capability)

    # if it's an actuator capability
    try:
        configure = capability.value.configure_actuator
    except AttributeError:
        pass
    else:
        actuator_name = give_name(Entity.Actuator)
        actuator_config = configure()
        actuator_config["type"] = capability.name
        actuator_capability = Capabilities[capability.name].value(name=actuator_name)
        actuator_capability.setup_actuator(actuator_name, actuator_config)
        component.add_capability(actuator_name, actuator_capability)

def setup_new_component():
    add_new_capability = True
    while add_new_capability:
        setup_component()
        add_new_capability = helpers.yes_or_no_question("\nDo you want to add another capability?")

async def main():
    global component
    component = Component()
    component.load_config()
    logging.info("Starting configuration of your IoT Component.")
    if component.has_config_file():
        logging.info("An existing configuration file was found.")
        if helpers.yes_or_no_question("Would you like to import it?"):
            component.load_config()
            logging.info(f"Component {component.name} was loaded successfully.")
        else:
            logging.warn("The existing configuration will be overwritten.")
            setup_new_component()
    else:
        setup_new_component()

    logging.info("Finished configuring the new IoT Component.")
    logging.debug(component)

    component.run()
    await asyncio.sleep(30)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Process interrupted by the user.")                        
    