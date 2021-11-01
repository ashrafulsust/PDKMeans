from action import HostAction
from config import KombuConfig
from producer import EventProducer

data = {
    'k': 3,
    'e': 0,
    'path': 'data/500_Person_Gender_Height_Weight_Index.csv'
}

producer = EventProducer()
producer.send(KombuConfig.routing, KombuConfig.queue, HostAction.SUBMIT, data)
