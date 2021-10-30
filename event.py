from sys import argv

from kombu.connection import Connection
from config import KombuConfig
from queues import event_exchange, event_queues


def send_event(action, data, routing=KombuConfig.exchange):
    payload = {'action': action, 'data': data}

    with Connection(KombuConfig.host) as connection:
        producer = connection.Producer()
        producer.publish(
            payload,
            serializer='pickle',
            exchange=event_exchange,
            routing_key=routing,
            declare=event_queues
        )


if __name__ == '__main__':
    action = argv[1]
    data = argv[2]

    send_event(action, data)
