import math
import statistics
import time
import numpy as np

from utils import plot


def skmeans(data, k, d, e):
    centroids = data[np.random.randint(data.shape[0], size=k), :]

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
    k = 4
    d = 2
    e = 0

    data = np.loadtxt("data/500_Person_Gender_Height_Weight_Index.csv", delimiter=",", dtype=object, skiprows=1)
    data = data[:, 1:3].astype(float)

    centroids = skmeans(data, k, d, e)

    plot(data, centroids, k, d)


def benchmark_bmi_index():
    k = 4
    d = 2
    e = 0

    data = np.loadtxt("data/500_Person_Gender_Height_Weight_Index.csv", delimiter=",", dtype=object, skiprows=1)
    data = data[:, 1:3].astype(float)

    execution_times = []

    for t in range(100):
        start_time = time.time()
        centroids = skmeans(data, k, d, e)
        execution_times.append((time.time() - start_time))

    print(f"Avg execution time : {statistics.mean(execution_times)}s")


if __name__ == '__main__':
    test_bmi_index()
    benchmark_bmi_index()
