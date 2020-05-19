from settings import *
from agents import *
from roads import *


class Simulation:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config") if "config" in kwargs else Config()

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
        seconds = 0
        curr_seconds = 0
        mins = 0
        curr_mins = 0
        hours = 0
        curr_hours = 0
        days = 0
        curr_days = 0
        years = 0
        for t in range(self.config.simulation_duration):
            self.step()
            seconds = t+1
            curr_seconds = seconds % 60
            if curr_seconds == 0:
                mins = seconds // 60
                curr_mins = mins % 60
                if curr_mins == 0:
                    hours = mins // 60
                    curr_hours = hours % 24
                    if curr_hours == 0:
                        days = hours // 24
                        curr_days = days % 365
                        if curr_days == 0:
                            years = days // 365

                print(f"{curr_mins} minutes, {curr_hours} hours, {curr_days} days, {years} years have passed")


c = Config(**{"simulation_duration": 84000})
s = Simulation(**{"config": c})
MID_NODE_COUNT = 20

# initialize nodes
# main source
node1 = Node(**{"type": 1, "config": s.config})
s.nodes.append(node1)

# middle nodes
for i in range(MID_NODE_COUNT):
    new_node = Node(**{"type": randrange(-4, 2), "config": s.config})
    s.nodes.append(new_node)

# main sink
node2 = Node(**{"type": -1, "config": s.config})
s.nodes.append(node2)

# initialize roads
for i in range(len(s.nodes) - 1):
    new_road = Road(**{"len": 25, "start": s.nodes[i], "end": s.nodes[i+1], "name": str(i), "config": s.config})
    s.roads.append(new_road)
roadCircle = Road(**{"len": 5, "start": node2, "end": node1, "name": "Full circle", "config": s.config})
s.roads.append(roadCircle)

# run simulation
s.run()

total_added = list()
total_removed = list()
total_overwritten = list()

full_road_cells = list()
left_on_the_road = list()

for n in s.nodes:
    if n.type >= 0:
        total_added += n.added
    if n.type <= 0:
        total_removed += n.removed

for r in s.roads:
    full_road_cells += r.cells
    total_overwritten += r.overwritten

for cell in full_road_cells:
    if cell is not None:
        left_on_the_road.append(cell)

print(f"{len(total_added)} joined the traffic: {total_added}")
print(f"{len(total_removed)} left the traffic alive: {total_removed}")
print(f"{len(total_overwritten)} killed on the road: {total_overwritten}")
print(f"{len(left_on_the_road)} left on the road: {left_on_the_road}")
print(f"The road looks like this: {full_road_cells}")
