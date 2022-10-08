import numpy as np
from math import sin, cos, tan, pi

class Matrix(object):

    @staticmethod
    def makeIdentity():
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeTranslation(x, y, z):
        return np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeRotationX(angle):
        c = cos(angle)
        s = sin(angle)
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeRotationY(angle):
        c = cos(angle)
        s = sin(angle)
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeRotationZ(angle):
        c = cos(angle)
        s = sin(angle)
        return np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeScale(s):
        return np.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makePerspective(angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        a = angle_of_view * pi/180.0
        d = 1.0 / tan(a/2)
        r = aspect_ratio
        b = (far + near) / (near - far)
        c = 2*far*near / (near - far)
        return np.array([
            [d/r, 0, 0, 0],
            [0, d, 0, 0],
            [0, 0, b, c],
            [0, 0, -1, 0]
        ]).astype(float)