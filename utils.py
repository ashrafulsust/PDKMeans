import json
import math

import cv2
import matplotlib.pyplot as plt
import numpy as np
from kombu.log import get_logger

LOGGER = get_logger(__name__)


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def dict_upper(data):
    if isinstance(data, dict):
        return {key.upper(): dict_upper(value) for key, value in data.items()}
    else:
        return data


def to_json(data):
    return json.dumps(data, ensure_ascii=False, default=str)


def from_json(data):
    return json.loads(data)


def to_file(data, file):
    return json.dump(data, file, ensure_ascii=False, default=str)


def from_file(file):
    return json.load(file)


def to_format_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def to_format_file(data, file):
    return json.dump(data, file, indent=2, ensure_ascii=False, default=str)


def load_bmi_data(path):
    data = np.loadtxt(path, delimiter=",", dtype=object, skiprows=1)
    data = data[:, 1:3].astype(float)
    return data


def get_closest_centroid(row, centroids):
    min_distance = float("inf")
    min_centroid = -1

    for i, centroid in enumerate(centroids):
        distance = 0

        for j in range(len(centroid)):
            distance += (centroid[j] - row[j]) ** 2

        distance = np.sqrt(distance)

        if distance < min_distance:
            min_distance = distance
            min_centroid = i

    return min_centroid


def plot_bmi_data(data, centroids, save=False):
    k = len(centroids)

    # setting color values for our
    color = np.random.rand(k + 1, 3)

    for row in data:
        centroid = get_closest_centroid(row, centroids)
        plt.scatter(row[0], row[1], c=[color[centroid]])

    # plot centroids
    for centroid in centroids:
        plt.scatter(centroid[0], centroid[1], c=[color[k]])

    plt.xlabel("Height/ cm")
    plt.ylabel("Weight/ kg")

    if save:
        plt.savefig("bmi-output.png")
    else:
        plt.show()


def load_mri_image(path):
    original = cv2.imread(path)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    vectorized = np.float32(original.reshape((-1, 3)))
    return original, vectorized


def plot_mri_image(original, data, centroids, save=False):
    k = len(centroids)
    images = np.zeros((k, *data.shape))

    for index, row in enumerate(data):
        centroid = get_closest_centroid(row, centroids)
        images[centroid][index] = row

    n = math.ceil((k + 1) / 2)

    plt.subplot(n, 2, 1), plt.imshow(original)
    plt.title("Original")
    plt.axis("off")

    for i in range(k):
        image = images[i].reshape(original.shape)
        plt.subplot(n, 2, i + 2), plt.imshow(image)
        plt.title(f"Cluster#{i}")
        plt.axis("off")

    if save:
        plt.savefig("mri-output.png")
    else:
        plt.show()


def plot_bmi_index(path, save=False):
    data = np.loadtxt(path, delimiter=",", dtype=object, skiprows=1)

    # data[data == "Male"] = 1
    # data[data == "Female"] = 0

    # setting color values for our
    color = np.random.rand(6, 3)

    for row in data:
        plt.scatter(float(row[1]), float(row[2]), c=[color[int(row[3])]])

    plt.xlabel("Height/ cm")
    plt.ylabel("Weight/ kg")

    if save:
        plt.savefig("index-output.png")
    else:
        plt.show()


def load_synthetic_data(path):
    return np.loadtxt(path, dtype=float)


def plot_synthetic_data(data, centroids, save=False):
    k = len(centroids)

    # setting color values for our
    color = np.random.rand(k + 1, 3)

    for row in data:
        centroid = get_closest_centroid(row, centroids)
        plt.scatter(row[0], row[1], c=[color[centroid]])

    # plot centroids
    for centroid in centroids:
        plt.scatter(centroid[0], centroid[1], c=[color[k]])

    plt.xlabel("x")
    plt.ylabel("y")

    if save:
        plt.savefig("synthetic-output.png")
    else:
        plt.show()
