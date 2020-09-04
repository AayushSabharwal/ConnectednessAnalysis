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


number_nodes = 1000
data = []
g = nx.Graph()
g.add_nodes_from(list(range(number_nodes)))
max_deg = 0


def sample_plot():
    components = nx.connected_components(g)
    data.append(PlotData())
    curr_max_deg = 0
    for component in components:
        data[-1].n_comp += 1
        data[-1].sizes.append(len(component))
        avg = 0
        for node in component:
            # noinspection PyUnresolvedReferences
            avg += g.degree[node]
        avg /= data[-1].sizes[-1]
        curr_max_deg = max(curr_max_deg, avg)
        data[-1].avg_deg.append(avg)
    return curr_max_deg


while not nx.is_connected(g):
    max_deg = max(max_deg, sample_plot())
    edge = random.choices(list(g.nodes()), k=2)
    g.add_edge(edge[0], edge[1])

sample_plot()

x = data[-1].sizes
y = data[-1].avg_deg
plt.subplots_adjust(left=0.25, bottom=0.25)
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.125, bottom=0.157, right=0.9, top=0.95, wspace=0.2, hspace=0.2)

plt.xlim(0, number_nodes)
plt.ylim(0, max_deg)
plt.xlabel("Size of component")
plt.ylabel("Average degree of nodes")

p = plt.scatter(x, y, color=(0.2, 0.6, 0.1, 0.5))
ax.margins(x=0)
axis = plt.axes([0.15, 0.02, 0.7, 0.03])
slide = Slider(axis, '# Edges', 0, len(data)-1, valinit=0, valstep=1)


def update(val):
    val = int(val)
    p.set_offsets(np.c_[data[val].sizes, data[val].avg_deg])
    fig.canvas.draw_idle()


slide.on_changed(update)
plt.show()
