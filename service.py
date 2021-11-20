import math
import time
import numpy as np
from kombu.log import get_logger

from action import *
from config import Config, KombuConfig
from producer import EventProducer
from utils import load_bmi_data, plot_bmi_data, load_mri_image, plot_mri_image

LOGGER = get_logger(__name__)


class HostService:

    def __init__(self):
        self.config = Config()
        self.producer = EventProducer()

        self.actions = {
            HostAction.PING: self.process_ping,
            HostAction.REGISTER: self.process_register,
            HostAction.SUBMIT: self.process_submit,
            HostAction.RESULT: self.process_result
        }

        self.workers = []
        self.k = 0
        self.e = 0
        self.n = 0
        self.d = 0
        self.t = 0
        self.J = 0
        self.GRD = 0
        self.GRC = None
        self.GCard = None
        self.data = None
        self.original = None
        self.centroids = None
        self.remaining = 0
        self.start_time = 0

    def process_action(self, action, data):
        if action not in self.actions:
            return

        return self.actions[action](data)

    def process_ping(self, data):
        LOGGER.info(f'ping {data}')

    def process_register(self, worker_id):
        self.workers.append(worker_id)
        LOGGER.info(f'registered worker id {worker_id}')

    def process_submit(self, request):
        LOGGER.info(f"started processing {request}")

        self.k = request['k']
        self.e = request['e']
        self.t = 0
        self.J = 0

        if request['path'].endswith('csv'):
            self.original, self.data = None, load_bmi_data(request['path'])
        else:
            self.original, self.data = load_mri_image(request['path'])

        self.n = self.data.shape[0]
        self.d = self.data.shape[1]
        self.GRD = 0
        self.GRC = np.zeros((self.k, self.d))
        self.GCard = np.zeros(self.k)
        self.centroids = self.data[np.random.randint(self.n, size=self.k), :]

        self.start_time = time.time()

        w = len(self.workers)
        m = math.ceil(self.n / w)

        self.remaining = w

        for i, worker in enumerate(self.workers):
            item = {
                'data': self.data[i * m:(i + 1) * m],
                'centroids': self.centroids
            }
            self.producer.send(worker, worker, WorkerAction.DATA, item)

    def process_result(self, request):
        self.GRD += request['RD']
        self.GRC += request['RC']
        self.GCard += request['Card']

        self.remaining -= 1

        if self.remaining == 0:
            for i in range(self.k):
                for j in range(self.d):
                    self.centroids[i, j] = self.GRC[i][j] / self.GCard[i]

            LOGGER.info(f"centroid = {self.centroids}")

            if abs(self.GRD - self.J) <= self.e:
                execution_time = (time.time() - self.start_time)
                LOGGER.info(f"finished, execution time {execution_time}s")

                if self.original is None:
                    plot_bmi_data(self.data, self.centroids, True)
                else:
                    plot_mri_image(self.original, self.data, self.centroids, True)
            else:
                self.t += 1

                LOGGER.info(f"iteration#{self.t}")

                self.J = self.GRD

                self.GRD = 0
                self.GRC = np.zeros((self.k, self.d))
                self.GCard = np.zeros(self.k)
                self.remaining = len(self.workers)

                for worker in self.workers:
                    self.producer.send(worker, worker, WorkerAction.CENTROID, self.centroids)


class WorkerService:

    def __init__(self):
        self.config = Config()
        self.producer = EventProducer()

        self.actions = {
            WorkerAction.PING: self.process_ping,
            WorkerAction.DATA: self.process_data,
            WorkerAction.CENTROID: self.process_centroid
        }

        self.data = None

    def process_action(self, action, data):
        if action not in self.actions:
            return

        return self.actions[action](data)

    def process_ping(self, data):
        LOGGER.info(f'ping {data}')

    def process_data(self, request):
        self.data = request['data']
        self.process_centroid(request['centroids'])

    def process_centroid(self, centroids):
        k = centroids.shape[0]
        d = centroids.shape[1]

        RD = 0
        RC = np.zeros((k, d))
        Card = np.zeros(k)

        for row in self.data:
            min_distance = float("inf")
            min_centroid = -1

            for i, centroid in enumerate(centroids):
                distance = 0

                for j in range(d):
                    distance += (centroid[j] - row[j]) ** 2

                distance = np.sqrt(distance)

                if distance < min_distance:
                    min_distance = distance
                    min_centroid = i

                RD += distance

            for j in range(d):
                RC[min_centroid][j] += row[j]

            Card[min_centroid] += 1

        print(f"RD = {RD}")
        print(f"RC = {RC}")
        print(f"Card = {Card}")

        result = {
            'RD': RD,
            'RC': RC,
            'Card': Card
        }

        self.producer.send(KombuConfig.routing, KombuConfig.queue, HostAction.RESULT, result)
