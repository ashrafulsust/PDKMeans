from sys import argv

from kombu import Exchange
from kombu.connection import Connection
from config import KombuConfig


def send_event(routing, action, data):
    payload = {'action': action, 'data': data}

    exchange = Exchange(KombuConfig.exchange, type='direct')

    with Connection(KombuConfig.host) as connection:
        producer = connection.Producer()
        producer.publish(
            payload,
            serializer='pickle',
            exchange=exchange,
            routing_key=routing
        )


if __name__ == '__main__':
    routing = argv[1]
    action = argv[2]
    data = argv[3]

    send_event(routing, action, data)
