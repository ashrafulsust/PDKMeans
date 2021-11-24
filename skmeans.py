import math
import time

import numpy as np

from utils import plot_bmi_data, load_bmi_data, load_mri_image, plot_mri_image, plot_bmi_index


def skmeans(data, k, e):
    n = data.shape[0]
    d = data.shape[1]

    centroids = data[np.random.randint(n, size=k), :]

    print(f"centroids = {centroids}")

    J1 = 0

    for t in range(10000):
        print(f"iteration#{t}")

        RD = 0
        RC = np.zeros((k, d))
        Card = np.zeros(k)

        for row in data:
            min_distance = float("inf")
            min_centroid = None

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

        for i in range(k):
            for j in range(d):
                centroids[i, j] = RC[i][j] / Card[i]

        print(f"centroid = {centroids}")

        J2 = RD

        print(f"J = {J2}")

        if math.isnan(J2):
            raise Exception(f"J is nan")

        if abs(J1 - J2) <= e:
            break

        J1 = J2

    return centroids


def test_bmi_index():
    k = 6
    e = 0

    data = load_bmi_data("data/500_Person_Gender_Height_Weight_Index.csv")
    start_time = time.time()
    centroids = skmeans(data, k, e)
    print(f"Execution time : {time.time() - start_time}s")
    plot_bmi_data(data, centroids)


def test_mri_image():
    k = 3
    e = 0

    original, data = load_mri_image("data/mri-3.jpg")
    start_time = time.time()
    centroids = skmeans(data, k, e)
    print(f"Execution time : {time.time() - start_time}s")
    plot_mri_image(original, data, centroids)


if __name__ == '__main__':
    test_bmi_index()
    test_mri_image()
