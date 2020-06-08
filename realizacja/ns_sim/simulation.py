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

        # phase of day traffic modifiers
        self.curr_time = self.config.sim_start_time  # current day time in seconds
        self.curr_phase = self.config.sim_daytime_phases[-1]  # current phase of the day with its traffic modifier
        self.total_time_elapsed = 0  # time passed since beginning of simulation

    def step_time(self):
        self.total_time_elapsed += 1
        self.curr_time = (self.curr_time + 1) % (24 * 3600)

    def adjust_daytime_phase(self):
        """Should be called at every step of the simulation"""
        # remember previous phase
        prev_phase = self.curr_phase
        phases = self.config.sim_daytime_phases

        for i in range(len(phases) - 1, -1, -1):
            if self.curr_time >= phases[i][0]:
                # change phase
                self.curr_phase = phases[i]

                # adjust nodes' spawn modifier
                for node in self.nodes:
                    node.chance_to_spawn /= prev_phase[1]
                    node.chance_to_spawn *= self.curr_phase[1]
                break

    def step(self):
        """
        Perform a single time step for all simulation elements
        Bigger, environmental elements contain others,
            e.g. Roads contain Vehicles, so simulation only calls
            step() for Roads, they internally will call step()
            for their child elements
        :return:
        """
        # check for new daytime phase
        self.adjust_daytime_phase()

        # this is basically equivalent to calling step() on every vehicle
        for r in self.roads:
            r.step()

        # then you should resolve all nodes, removing or adding vehicles
        for n in self.nodes:
            n.step()

        # move time forward by 1 time step
        self.step_time()

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

