import math as m
import numpy as np

r = 1
loop = True
iterations = 360
point_list = []
rot_a = (m.pi / 2) / 60

p = np.array([[1, 0, -1, 0],
              [0, 1, 0, -1]])

rotM = np.array([[m.cos(rot_a), -m.sin(rot_a)],
                [m.sin(rot_a), m.cos(rot_a)]])
