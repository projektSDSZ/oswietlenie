from agents import Vehicle
from settings import Config

from typing import Optional
from random import uniform


class Node:
    """
    Default parameters
    """
    D_SPAWNED_VEHICLES_LIMIT = 10  # maximum number of vehicles a Source can spawn
    D_CHANCE_TO_SPAWN = 0.8  # chance to spawn a vehicle on each time step

    def __init__(self, **kwargs):
        """
        Node's type could be one of three:
            -> positive integer indicates a Source
            -> negative integer indicates a Sink
            -> 0 indicates Source and Sink together

        :param kwargs:
        """
        self.config = kwargs.get("config") if "config" in kwargs else Config()

        self.type = kwargs.get("type") if "type" in kwargs else 0

        self.spawned_vehicles = kwargs.get("spawned_vehicles") if "spawned_vehicles" in kwargs else 0
        self.spawned_vehicles_limit = kwargs.get(
            "spawned_vehicles_limit") if "spawned_vehicles_limit" in kwargs else Node.D_SPAWNED_VEHICLES_LIMIT
        self.chance_to_spawn = kwargs.get("chance_to_spawn") if "chance_to_spawn" in kwargs else Node.D_CHANCE_TO_SPAWN

        self.input_road = kwargs.get("input_road") if "input_road" in kwargs else None
        self.output_road = kwargs.get("output_road") if "output_road" in kwargs else None

        self.added = list()  # archive-list of Vehicles added by this Node
        self.removed = list()  # archive-list of Vehicles removed by this Node

    def try_to_spawn_vehicle(self) -> None:
        # if its a Source, and it haven't spawned all of its possible vehicles, and the stars align
        if self.type >= 0 and self.spawned_vehicles < self.spawned_vehicles_limit:
            spawn_roll = uniform(0, 1)
            if spawn_roll < self.chance_to_spawn and self.output_available():
                # create a new vehicle and pass it to output Road
                kwargs = {"road": self.output_road, "config": self.config, "behaviour": 0.5, "dest": 0}
                vehicle = Vehicle(**kwargs)
                self.output_road.cells[0] = vehicle
                self.spawned_vehicles += 1
                self.added.append(vehicle)

    def try_to_remove_vehicle(self) -> None:
        # remove Vehicle that reached its destination at this Node
        if self.type <= 0 and self.input_available() and self.input_road.cells[-1].dest <= 0:
            self.removed.append(self.input_road.cells[-1])
            self.input_road.cells[-1] = None

    def input_available(self) -> bool:
        return self.input_road is not None and self.input_road.cells[-1] is not None

    def output_available(self) -> bool:
        return self.output_road is not None and self.output_road.cells[0] is None

    def step(self) -> None:
        """
        Two types of step operation, one for sink, one for source
        :return:
        """
        if self.type <= 0:
            """Case Sink"""
            self.try_to_remove_vehicle()

        if self.type >= 0:
            """Case Source"""
            self.try_to_spawn_vehicle()


class Road:
    """
    Define default parameters here
    """
    D_SPEED_LIMIT = 2  # in [CELL_SIZE / TIME_STEP] -> 13.89m/s == 50km/h

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """

        '''
        WYJAŚNIENIA
        --> Słowniki argumentów ułatwią zmianę ilości parametrów jakie 
            przyjmuje konstruktor. Jeżeli na którymś etapie 
            zechcemy wyrzucić lub dodać jakieś pole to wystarczy
            dopisać/usunąć linijkę typu self.xyz = kwargs.get("xyz")...
        
        '''
        self.config = kwargs.get("config") if "config" in kwargs else Config()

        # road length in [CELL_SIZE]
        self.len = kwargs.get("len") if "len" in kwargs else 0

        # speed limit in [CELL_SIZE / TIME_STEP]
        self.speed_limit = kwargs.get("speed_limit") if "speed_limit" in kwargs else Road.D_SPEED_LIMIT

        # lista ma długość drogi w [CELL_SIZE], komórka może zawierać nic (typ None) lub Vehicle
        self.cells = kwargs.get("cells") if "cells" in kwargs else [None for _ in range(self.len)]

        # start i end są węzłami, obiektami klasy Node
        self.start = kwargs.get("start") if "start" in kwargs else None
        self.end = kwargs.get("end") if "end" in kwargs else None

        # pass reference to this Road to its start and end Nodes
        if self.start is not None:
            self.start.output_road = self
        if self.end is not None:
            self.end.input_road = self

    def step(self):
        for i in range(len(self.cells) - 1, -1, -1):
            """Resolve from last on the list, so furthest on the road, to first on the list"""
            if self.cells[i] is not None:
                self.cells[i].step()
