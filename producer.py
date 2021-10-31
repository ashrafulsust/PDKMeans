from kombu.log import get_logger
from kombu import Exchange, Connection, Queue

from config import KombuConfig

LOGGER = get_logger(__name__)


class EventProducer:

    def __init__(self):
        self.exchange = Exchange(KombuConfig.exchange, type='direct')
        self.connection = Connection(KombuConfig.host)
        self.producer = self.connection.Producer()

    def send(self, routing, queue, action, data):
        payload = {'action': action, 'data': data}

        return self.producer.publish(
            payload,
            serializer='pickle',
            exchange=self.exchange,
            routing_key=routing,
            declare=[
                Queue(queue, self.exchange, routing_key=routing)
            ]
        )

    def close(self):
        self.connection.close()
