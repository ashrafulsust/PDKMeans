from kombu.log import get_logger
from kombu import Exchange, Queue
from kombu.mixins import ConsumerMixin

from config import KombuConfig

LOGGER = get_logger(__name__)


class BaseEventConsumer(ConsumerMixin):

    def __init__(self, connection, service, routing, queue):
        self.connection = connection
        self.service = service

        exchange = Exchange(KombuConfig.exchange, type='direct')

        self.queues = [
            Queue(queue, exchange, routing_key=routing)
        ]

    def get_consumers(self, consumer, channel):
        return [
            consumer(queues=self.queues, accept=['pickle'], callbacks=[self.process])
        ]

    def process(self, body, message):
        action = body['action']
        data = body['data']

        LOGGER.info('Request to {}'.format(action))

        try:
            self.service.process_action(action, data)
        except Exception as e:
            LOGGER.exception(e)

        LOGGER.info('Performed {}'.format(action))

        message.ack()


class HostEventConsumer(BaseEventConsumer):

    def __init__(self, connection, service):
        super().__init__(connection, service, KombuConfig.routing, KombuConfig.queue)


class WorkerEventConsumer(BaseEventConsumer):

    def __init__(self, connection, service, routing, queue):
        super().__init__(connection, service, routing, queue)
