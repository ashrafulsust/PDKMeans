from action import HostAction
from config import KombuConfig
from producer import EventProducer


def benchmark_bmi_index():
    data = {
        'k': 4,
        'e': 0,
        'path': 'data/500_Person_Gender_Height_Weight_Index.csv'
    }

    producer = EventProducer()

    for t in range(10):
        producer.send(KombuConfig.routing, KombuConfig.queue, HostAction.SUBMIT, data)


if __name__ == '__main__':
    benchmark_bmi_index()
