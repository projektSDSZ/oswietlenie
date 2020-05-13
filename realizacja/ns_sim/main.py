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
MID_NODE_COUNT = 20

# initialize nodes
# main source
node1 = Node(**{"type": 1, "config": s.config})
s.nodes.append(node1)

# middle nodes
for i in range(MID_NODE_COUNT):
    new_node = Node(**{"type": 0, "config": s.config})
    s.nodes.append(new_node)

# main sink
node2 = Node(**{"type": -1, "config": s.config})
s.nodes.append(node2)

# initialize roads
for i in range(len(s.nodes) - 1):
    new_road = Road(**{"len": 50, "start": s.nodes[i], "end": s.nodes[i+1], "config": s.config})
    s.roads.append(new_road)

# run simulation
s.run()

total_added = list()
total_removed = list()
total_overwritten = list()

for n in s.nodes:
    if n.type >= 0:
        total_added += n.added
    if n.type <= 0:
        total_removed += n.removed

for r in s.roads:
    total_overwritten += r.overwritten

print(f"{len(total_added)} joined the traffic: {total_added}")
print(f"{len(total_removed)} left the traffic alive: {total_removed}")
print(f"{len(total_overwritten)} killed on the road: {total_overwritten}")
