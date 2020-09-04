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


# colour of points in the graph, in RGBA. Making points transparent allows to see stacked points, and the density of
# points in a region
point_colour = (0.2, 0.6, 0.1, 0.5)
# number of nodes in the graph
number_nodes = 1000

data = []   # to store data after adding each edge
g = nx.Graph()
g.add_nodes_from(list(range(number_nodes)))
max_deg = 0 # the maximum average degree of a component, used to properly set y axis limits while making plot


def sample_plot():
    """
    Function to sample the data of the graph, and add it to the data list
    :returns maximum average degree of any component at this step
    """
    components = nx.connected_components(g)     # get the connected components
    data.append(PlotData())     # add a plot data to the list
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
    max_deg = max(max_deg, sample_plot())   # sample the graph and update maximum average degree
    edge = random.choices(list(g.nodes()), k=2)     # choose a random edge
    g.add_edge(edge[0], edge[1])    # add the random edge

sample_plot()   # sample graph after it is connected

# plotting
x = data[0].sizes
y = data[0].avg_deg
plt.subplots_adjust(left=0.25, bottom=0.25)
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.125, bottom=0.157, right=0.9, top=0.95, wspace=0.2, hspace=0.2)

plt.xlim(0, number_nodes)
plt.ylim(0, max_deg)
plt.xlabel("Size of component")
plt.ylabel("Average degree of nodes")

p = plt.scatter(x, y, color=point_colour)
ax.margins(x=0)
axis = plt.axes([0.15, 0.02, 0.7, 0.03])
slide = Slider(axis, '# Edges', 0, len(data)-1, valinit=0, valstep=1)


def update(val):
    val = int(val)
    p.set_offsets(np.c_[data[val].sizes, data[val].avg_deg])
    fig.canvas.draw_idle()


slide.on_changed(update)
plt.show()
