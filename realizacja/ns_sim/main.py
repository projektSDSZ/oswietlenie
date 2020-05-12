from settings import *
from agents import *
from roads import *


class Simulation:
    def __init__(self, **kwargs):
        self.config = Config()

        # define nodes first because roads contain references
        #   to start and end nodes
        self.nodes = kwargs.get("nodes") if "nodes" in kwargs else list()
        self.roads = kwargs.get("roads") if "roads" in kwargs else list()

    def step(self):
        """
        Perform a single time step for all simulation elements
        Bigger, environmental elements contain others,
            e.g. Roads contain Vehicles, so simulation only calls
            step() for Roads, they internally will call step()
            for their child elements
        :return:
        """
        # this is basically equivalent to calling step() on every vehicle
        for r in self.roads:
            r.step()

        # then you should resolve all nodes, removing or adding vehicles
        for n in self.nodes:
            n.step()

    def run(self):
        for t in range(self.config.simulation_duration):
            self.step()


s = Simulation()

# initialize nodes
node1 = Node(**{"type": 0, "config": s.config})
node2 = Node(**{"type": 0, "config": s.config})

# initialize roads
road1 = Road(**{"len": 100, "start": node1, "end": node2, "config": s.config})

# pass nodes and roads to the simulation
s.nodes.append(node1)
s.nodes.append(node2)

s.roads.append(road1)

# run simulation
s.run()

for n in s.nodes:
    print(n.added)
    print(n.removed)

for r in s.roads:
    print(r.cells)
