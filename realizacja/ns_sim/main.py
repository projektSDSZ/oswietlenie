from ns_sim.settings import *
from ns_sim.agents import *
from ns_sim.roads import *

from copy import deepcopy


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

        return self

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

