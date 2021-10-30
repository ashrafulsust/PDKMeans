from kombu import Connection
from kombu.log import get_logger
from kombu.utils.debug import setup_logging

from config import KombuConfig
from consumer import EventConsumer
from service import HostService

LOGGER = get_logger(__name__)


def run():
    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])

    service = HostService()

    # Connect to AMQ and start the consumer
    with Connection(KombuConfig.host) as connection:
        try:
            consumer = EventConsumer(connection, service)
            consumer.run()
        except KeyboardInterrupt:
            print('Host Stopped')


if __name__ == '__main__':
    run()
