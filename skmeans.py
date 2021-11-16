import numpy as np
import matplotlib.pyplot as plt

k = 4
d = 2
e = 0

data = np.loadtxt("data/500_Person_Gender_Height_Weight_Index.csv", delimiter=",", dtype=object, skiprows=1)
data = data[:, 1:3].astype(float)

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

    for i in range(k):
        for j in range(d):
            centroids[i, j] = RC[i][j] / Card[i]

    print(f"centroid = {centroids}")

    J2 = RD

    print(f"J = {J2}")

    if abs(J1 - J2) <= e:
        break

    J1 = J2

# setting color values for our
color = ["brown", "blue", "green", "cyan"]

for row in data:
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

    plt.scatter(row[0], row[1], c=color[min_centroid])

# plot centroids
for centroid in centroids:
    plt.scatter(centroid[0], centroid[1], c="red")

plt.xlabel("Height/ cm")
plt.ylabel("Weight/ kg")
plt.show()
