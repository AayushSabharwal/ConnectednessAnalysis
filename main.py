import networkx as nx
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


class PlotData:
    def __init__(self):
        self.n_comp = 0
        self.sizes = []
        self.avg_deg = []


nnodes = 100
data = []
g = nx.Graph()
g.add_nodes_from(list(range(nnodes)))
max_deg = 0


def sample_plot():
    components = nx.connected_components(g)
    data.append(PlotData())
    max_deg = 0
    for component in components:
        data[-1].n_comp += 1
        data[-1].sizes.append(len(component))
        avg = 0
        for node in component:
            avg += g.degree[node]
        avg /= data[-1].sizes[-1]
        max_deg = max(max_deg, avg)
        data[-1].avg_deg.append(avg)
    return max_deg


while not nx.is_connected(g):
    max_deg = max(max_deg, sample_plot())
    edge = random.choices(list(g.nodes()), k=2)
    g.add_edge(edge[0], edge[1])

sample_plot()

x = data[-1].sizes
y = data[-1].avg_deg
plt.subplots_adjust(left=0.25, bottom=0.25)
fig, ax = plt.subplots()
plt.xlim(0, nnodes)
plt.ylim(0, max_deg)
p = plt.scatter(x, y, color=(0.2, 0.6, 0.1, 0.5))
ax.margins(x=0)
axcolor = 'lightgoldenrodyellow'
axis = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
slide = Slider(axis, 'Step', 0, len(data)-1, valinit=0, valstep=1)


def update(val):
    val = int(val)
    p.set_offsets(np.c_[data[val].sizes, data[val].avg_deg])
    fig.canvas.draw_idle()


slide.on_changed(update)
plt.show()
