import matplotlib.pyplot
import matplotlib.colors

cdict1 = {'red':   [[0.00, 0.10, 0.10],
                   [0.17, 0.30, 0.30],
                   [0.33, 0.35, 0.35],
                   [0.50, 1.00, 1.00],
                   [0.75, 0.92, 0.92],
                   [1.00, 0.87, 0.87]],
         'green': [[0.00, 0.30, 0.30],
                   [0.17, 0.53, 0.53],
                   [0.33, 0.72, 0.72],
                   [0.50, 1.00, 1.00],
                   [0.75, 0.52, 0.52],
                   [1.00, 0.32, 0.32]],
         'blue':  [[0.00, 0.29, 0.29],
                   [0.17, 0.53, 0.53],
                   [0.33, 0.73, 0.73],
                   [0.50, 1.00, 1.00],
                   [0.75, 0.20, 0.20],
                   [1.00, 0.15, 0.15]]}


diverging_hamster_colormap = matplotlib.colors.LinearSegmentedColormap('hamster', segmentdata=cdict1, N=256)

cdict2 = {'red':   [[0.00, 0.10, 0.10],
                   [0.33, 0.30, 0.30],
                   [0.67, 0.92, 0.92],
                   [1.00, 0.87, 0.87]],
         'green': [[0.00, 0.30, 0.30],
                   [0.3, 0.53, 0.53],
                   [0.67, 0.52, 0.52],
                   [1.00, 0.32, 0.32]],
         'blue':  [[0.00, 0.29, 0.29],
                   [0.33, 0.53, 0.53],
                   [0.67, 0.20, 0.20],
                   [1.00, 0.15, 0.15]]}

monotonic_hamster_colormap = matplotlib.colors.LinearSegmentedColormap('hamster', segmentdata=cdict2, N=256)
