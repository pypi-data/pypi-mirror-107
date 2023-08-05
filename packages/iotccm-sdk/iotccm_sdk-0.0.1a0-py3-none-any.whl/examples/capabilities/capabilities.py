from enum import Enum

from .lcd_capability import LcdCapability
from .dht11_capability import Dht11Capability
from .motion_capability import MotionDetectionCapability

class Capabilities(Enum):
    LCD = LcdCapability
    DHT11 = Dht11Capability
    MotionSensor = MotionDetectionCapability