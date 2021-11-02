from sys import argv

from action import HostAction
from config import KombuConfig
from producer import EventProducer

data = {
    'k': int(argv[1]),
    'e': int(argv[2]),
    'path': argv[3]
}

producer = EventProducer()
producer.send(KombuConfig.routing, KombuConfig.queue, HostAction.SUBMIT, data)
