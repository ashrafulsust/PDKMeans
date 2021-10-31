import uuid

from kombu import Connection
from kombu.log import get_logger
from kombu.utils.debug import setup_logging

from config import KombuConfig
from consumer import WorkerEventConsumer
from service import WorkerService

LOGGER = get_logger(__name__)


def run():
    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])

    service = WorkerService()
    service.producer.send(KombuConfig.routing, KombuConfig.queue, 'register', KombuConfig.id)

    # Connect to AMQ and start the consumer
    with Connection(KombuConfig.host) as connection:
        try:
            consumer = WorkerEventConsumer(connection, service, KombuConfig.id, KombuConfig.id)
            consumer.run()
        except KeyboardInterrupt:
            LOGGER.info('Worker Stopped')


if __name__ == '__main__':
    run()
