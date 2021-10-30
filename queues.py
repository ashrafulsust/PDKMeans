from kombu import Exchange, Queue

from config import KombuConfig

event_exchange = Exchange(KombuConfig.exchange, type='direct')

event_queues = [
    Queue(KombuConfig.queue, event_exchange, routing_key=KombuConfig.exchange)
]
