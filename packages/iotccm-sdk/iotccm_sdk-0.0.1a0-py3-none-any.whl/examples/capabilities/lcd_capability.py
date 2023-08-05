from iotccm_sdk.capability.actuator_capability import ActuatorCapability


class LcdCapability(ActuatorCapability):
    def actuate(self, **kwargs):
        print("LCD capability")

    @staticmethod
    def configure_actuator():
        print("configure LCD")