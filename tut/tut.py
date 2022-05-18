import gdspy
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np

gdsii = gdspy.GdsLibrary(infile='files/DC_375.gds')

x = []
y = []
for cell, body in gdsii.cells.items():
    for polygon in body.polygons:
        x_ = []
        y_ = []
        # if len(polygon.polygons[0]) > 4:
        #     continue
        for coord in polygon.polygons[0]:
            x_.append(coord[0])
            y_.append(coord[1])
        x.append(x_)
        y.append(y_)

plt.style.use('_mpl-gallery')

# plot
fig, ax = plt.subplots()

for i, x_ in enumerate(x):
    ax.step(x_, y[i], linewidth=2.5)
    ax.plot(x_, y[i])

plt.show()

