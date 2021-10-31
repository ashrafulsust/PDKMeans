from kombu.log import get_logger

from action import *
from config import Config
from producer import EventProducer

LOGGER = get_logger(__name__)


class HostService:

    def __init__(self):
        self.config = Config()
        self.producer = EventProducer()

        self.actions = {
            HostAction.PING: self.process_ping,
            HostAction.REGISTER: self.process_register
        }

    def process_action(self, action, data):
        if action not in self.actions:
            return

        return self.actions[action](data)

    def process_ping(self, data):
        LOGGER.info(f'ping {data}')

    def process_register(self, data):
        LOGGER.info(f'registered worker id {data}')


class WorkerService:

    def __init__(self):
        self.config = Config()
        self.producer = EventProducer()

        self.actions = {
            WorkerAction.PING: self.process_ping
        }

    def process_action(self, action, data):
        if action not in self.actions:
            return

        return self.actions[action](data)

    def process_ping(self, data):
        LOGGER.info(f'ping {data}')
