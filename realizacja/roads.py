from typing import Optional

from agents import Vehicle


class Node:
    def __init__(self, **kwargs):
        """
        Node's type could be one of three:
            -> positive integer indicates a Source
            -> negative integer indicates a Sink
            -> 0 indicates Source and Sink together

        :param kwargs:
        """
        self.type = kwargs.get("type") if "type" in kwargs else 0

        self.input_road = kwargs.get("input_road") if "input_road" in kwargs else None
        self.output_road = kwargs.get("output_road") if "output_road" in kwargs else None

    def input_not_empty(self) -> bool:
        return self.input_road.cells[-1] is not None

    def step(self) -> None:
        """
        Two types of step operation, one for sink, one for source
        :return:
        """
        if self.input_not_empty():
            """If last cell in input_road is a vehicle"""
            # pass vehicle along if destination not reached
            if self.output_road.cells[0] is None and self.input_road.cells[-1].dest > 0:
                # if there is empty space on the beginning of output road
                if self.type <= 0:
                    """Case Sink"""
                    # decrement destination counter
                    self.input_road.cells[-1].dest -= 1

                if self.type >= 0:
                    """Case Source"""
                    pass

                # move the vehicle there
                self.output_road.cells[0] = self.input_road.cells[-1]
                self.input_road.cells[-1] = None
            else:
                # if space occupied
                # do not pass the vehicle
                pass




class Road:
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

        # vehicles jest listą obiektów klasy Vehicle, komórka listy jest naszą komórką drogową
        self.cells = list(kwargs.get("cells")) if "cells" in kwargs else list()

        # start i end są węzłami, obiektami klasy Node
        self.start = kwargs.get("start") if "start" in kwargs else None
        self.end = kwargs.get("end") if "end" in kwargs else None

    def step(self):
        for i in range(len(self.cells), -1, -1):
            """Resolve from last, so furthest on the road, to first"""
            self.cells[i].step()
