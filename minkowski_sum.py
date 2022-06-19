from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


fig, ax = plt.subplots()


class Point2d:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        return Point2d(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point2d(self.x - p.x, self.y - p.y)

    def cross(self, q):
        return self.x * q.y - self.y * q.x

    def toList(self):
        return np.array([self.x, self.y])


def reorder_polygon(P):
    pos = 0
    for i in range(1, len(P)):
        if P[i].y < P[pos].y or (P[i].y == P[pos].y and P[i].x < P[pos].x):
            pos = i
        i += 1

    P = deque(P)
    P.rotate(pos)
    P = list(P)


def minkowski(P, Q):
    # the first vertex must be the lowest
    reorder_polygon(P)
    reorder_polygon(Q)
    # we must ensure cyclic indexing
    P.append(P[0])
    P.append(P[1])
    Q.append(Q[0])
    Q.append(Q[1])

    i = 0
    j = 0
    result = []
    while i < len(P) - 2 or j < len(Q) - 2:
        result.append(P[i] + Q[j])
        a = P[i + 1] - P[i]
        b = Q[j + 1] - Q[j]
        cr = a.cross(b)
        if cr >= 0:
            i += 1
        if cr <= 0:
            j += 1

    return result

def visualize(P,color):
    y = P[0].toList()
    for p in P:
        y = np.vstack((y, p.toList()))
    poly = Polygon(y, facecolor=color)

    ax.add_patch(poly)
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 10)


def main():
    P = [Point2d(2, 1), Point2d(4, 1), Point2d(4, 3), Point2d(2, 3)]
    Q = [Point2d(-3, 1), Point2d(-2, 2), Point2d(-4, 2)]
    visualize(P, 'red')
    visualize(Q, 'green')

    result = minkowski(P, Q)
    visualize(result, 'blue')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()