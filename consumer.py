from kombu.log import get_logger
from kombu.mixins import ConsumerMixin

from queues import event_queues

LOGGER = get_logger(__name__)


class EventConsumer(ConsumerMixin):

    def __init__(self, connection, service):
        self.connection = connection
        self.service = service

    def get_consumers(self, consumer, channel):
        return [
            consumer(queues=event_queues, accept=['pickle'], callbacks=[self.process])
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
