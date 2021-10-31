from sys import argv

from producer import EventProducer

if __name__ == '__main__':
    routing = argv[1]
    queue = argv[2]
    action = argv[3]
    data = argv[4]

    producer = EventProducer()
    producer.send(routing, queue, action, data)
