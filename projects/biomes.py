import random
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=4)


try:
    w = int(input("Enter a Matrix size between 50 and 200: "))
    e = int(input("Enter an elevation noise value: "))
    e2 = int(input("Enter a Humidity noise value: "))
except not (49 < w < 201) or (e <= 0) or (e2 <= 0):
    assert ValueError, "Please enter valid values"
except Exception:
    assert Exception, "Please enter valid Values"


class square:
    
    def __init__(self, elev, hum):
        self._elev = elev
        self._hum = hum
        self.set_biome()

    def get_elev(self):
        return self._elev

    def get_hum(self):
        return self._hum

    def set_elev(self, elev):
        self._elev = elev
        self.set_biome()

    def set_hum(self, hum):
        self._hum = hum
        self.set_biome()

    def set_biome(self):
        if self._elev >= 0.6:
            self._biome = 'S'
        elif self._elev <= 0.4:
            self._biome = 'O'
        elif self._hum >= 0.55:
            self._biome = 'R'
        elif self._hum >= 0.40:
            self._biome = 'T'
        else:
            self._biome = 'D'

    def __str__(self):
        return self._biome
    def __repr__(self):
        return self._biome


width, height = w, w

row = []

for i in range(height):
    col = []
    for j in range(width):
        val = noise([i/e, j/e])
        val = (val + 0.7) / 2
        val2 = noise([i/e2, j/e2])
        val2 = (val2 + 0.7) / 2
        col.append(square(val, val2))
    row.append(col)

#for r in row:
 #   for _ in r:
  #      print(_)

color_map = {
    'S': 0,
    'R': 1,
    'O': 2,
    'T': 3,
    'D': 4
}

img = [[color_map[sq._biome] for sq in r] for r in row]

Z = []

for r in row:
    new_row = []
    for sq in r:
        new_row.append(sq.get_elev())
    Z.append(new_row)

Z = np.array(Z)

import matplotlib.pyplot as plt

x = np.arange(width)
y = np.arange(height)
X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.plot_surface(X, Y, Z, cmap='terrain')

plt.show()

#plt.imshow(img)
#plt.show()

