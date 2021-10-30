import os
from kombu.log import get_logger

from utils import Singleton

LOGGER = get_logger(__name__)


class Config(metaclass=Singleton):
    def __init__(self):
        self._config = dict(os.environ)

    def get_property(self, key, default=None):
        return self._config.get(key.upper(), default)


class KombuConfig(Config):

    @property
    def host(self):
        return self.get_property("KOMBU_HOST")

    @property
    def exchange(self):
        return self.get_property("KOMBU_EXCHANGE")

    @property
    def queue(self):
        return self.get_property("KOMBU_QUEUE")


KombuConfig = KombuConfig()
