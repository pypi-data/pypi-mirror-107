import logging
import re


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-5.5s] %(message)s")

class Capability:
    def __init__(self, name, **kwargs) -> None:
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name