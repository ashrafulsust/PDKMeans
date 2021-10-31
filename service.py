from kombu.log import get_logger

from config import Config

LOGGER = get_logger(__name__)


class HostService:

    def __init__(self):
        self.config = Config()

        self.actions = {
            'command.run.test': self.process_test
        }

    def process_action(self, action, data):
        if action not in self.actions:
            return

        return self.actions[action](data)

    def process_test(self, data):
        LOGGER.info(f'Host : {data}')


class WorkerService:

    def __init__(self):
        self.config = Config()

        self.actions = {
            'command.run.test': self.process_test
        }

    def process_action(self, action, data):
        if action not in self.actions:
            return

        return self.actions[action](data)

    def process_test(self, data):
        LOGGER.info(f'Worker : {data}')
