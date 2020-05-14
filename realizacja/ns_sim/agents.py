from settings import Config

from collections import deque
from random import uniform
import names


class Vehicle:
    """
    Default parameters here
    """
    D_POS = 0
    D_VELOCITY = 0

    D_DIST_TO_NEXT = -1
    D_DEST = 0

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
        # give vehicle all information about the simulation's Config
        self.config = kwargs.get("config") if "config" in kwargs else Config()

        # give the vehicle all information about the Road its on
        self.road = kwargs.get("road") if "road" in kwargs else None

        # positional values derived from the Nagel-Schreckenberg model
        self.pos = kwargs.get("x") if "x" in kwargs else Vehicle.D_POS  # current position x(t)
        self.vel = kwargs.get("v") if "v" in kwargs else Vehicle.D_VELOCITY  # current velocity v(t)

        # keep distance to next car in this variable, usually calculated by its parent Road; in [CELL_SIZE]
        self.dist_to_next = kwargs.get("dist_to_next") if "dist_to_next" in kwargs else Vehicle.D_DIST_TO_NEXT

        # name the driver
        self.name = names.get_full_name()
        self.behav = kwargs.get("behav") if "behav" in kwargs else uniform(0.05, 0.95)  # probability of taking a sudden random,
        # the human element, e.g. braking out of fear

        self.dest = kwargs.get("dest") if "dest" in kwargs else Vehicle.D_DEST  # destination, number of possible sinks that agent
        # will ignore before choosing the one through
        # which he leaves

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name) + " who fears for his life " + str(self.behav * 100) + "% of the time"

    def speed_up(self, max_vel: int) -> int:
        """
        :param max_vel: describes maximum velocity, either determined by Road's speed limit or other factors
        :return:
        """
        if max_vel < 0:
            return self.vel
        self.vel = min(self.vel + 1, max_vel)
        return self.vel

    def slow_down(self, dist_to_next: int) -> int:
        """
        dist_to_next: free space between this Vehicle and the next one on the Road
        :return:
        """
        if dist_to_next < 0:
            return self.vel
        self.vel = min(self.vel, dist_to_next)
        return self.vel

    def calc_dist_to_next(self) -> int:
        """
        Calculate distance to next vehicle. Uses .visibility from the self.config variable
        -1 means no Vehicle is visible ahead of this one
        :return: distance in .cell_size units from the next vehicle within .visibility range
        """
        visible_cells_checked_q = 0
        next_road = self.road

        # 1.initialise the queue, first make a list, slice it to the right size
        cell_list = list(next_road.cells[self.pos+1:])
        while len(cell_list) < self.config.visibility:
            if next_road.end is not None:
                next_road = next_road.end.output_road
            else:
                break
            if next_road is None:
                break
            # 2.add self.config.visibility-many elements to the queue
            cell_list += list(next_road.cells)

        # 1.5. then pass it to the queue, sliced to the right size
        cell_queue = deque(list(cell_list[:self.config.visibility]))
        while len(cell_queue) > 0:
            # 3.check first element until Vehicle is found or queue empty
            elem = cell_queue.popleft()
            if elem is not None:
                # 4.return however many Nones have been found
                return visible_cells_checked_q
            visible_cells_checked_q += 1
        return -1

        # [OLD]: distance calculation
        # visible_cells_checked = 1  # increase this for every cell you check in search for a Vehicle, 1 because we
        # # # start from the next cell
        # while next_road is not None and visible_cells_checked < self.config.visibility:
        #     # special case for the Road that the vehicle is on, to only check ahead of it
        #     # initialize the queue
        #     if visible_cells_checked == 1:
        #         curr_road_cells = list(next_road.cells[self.pos + 1:])
        #     else:
        #         curr_road_cells = list(next_road.cells)
        #     # if this Vehicle is on a non-empty Road
        #     while len(curr_road_cells) > 0:
        #         if visible_cells_checked > self.config.visibility:
        #             # if ran out of visible cells then no Vehicle was encountered during the search
        #             self.dist_to_next = -1
        #             return -1
        #         # ELSE
        #         # see if this cell contains a Vehicle
        #         if curr_road_cells[0] is not None:
        #             # if element is a Vehicle, return distance to it
        #             self.dist_to_next = visible_cells_checked - 1
        #             return visible_cells_checked - 1
        #
        #         curr_road_cells.pop(0)
        #         visible_cells_checked += 1
        #
        #     # if no valid vehicle was found on this road, try to proceed search to the next one
        #     if next_road.end is not None:
        #         next_road = next_road.end.output_road
        #         visible_cells_checked += 1
        #     else:
        #         self.dist_to_next = -1
        #         return -1
        # return -1

    def get_speed_limit(self) -> int:
        return self.road.speed_limit if self.road is not None else -1

    def step(self) -> None:
        """
        Calculate increase in velocity, then constraint it by distance between this Vehicle and the next one,
            according to the Nagel-Schreckenberg model
        :return:
        """
        # firstly, all Vehicles accelerate by 1 every time step until they reach speed limit
        self.speed_up(self.get_speed_limit())

        # secondly, Vehicle's speed may get reduced to the distance between itself and the next Vehicle
        self.slow_down(self.calc_dist_to_next())

        # additionally, every Vehicle has a chance of randomly reducing their speed by 1 on each time step
        #       this is defined by the behaviour probability value
        if uniform(0, 1) <= self.behav:
            # if a random fraction from 0.0 to 1.0 is smaller than probability of slowing down
            # slow down by 1 CELL/TIME_STEP
            self.vel = max(0, self.vel - 1)

        # move the vehicle:
        # if next Node is a Sink
        if self.road.end.type >= 0 and self.vel + self.pos > self.road.len - 1:
            if self.dest <= 0:
                # Vehicle will slow down if the next intersection is its destination
                #   its the same formula as before but now intersection is the point at which Vehicle stops
                # removing the Vehicle is handled automatically by the self.road.end Node,
                #   which always checks the last cell in its input road
                self.slow_down(self.road.len - 1 - self.pos)
            else:
                self.dest -= 1

        # place Vehicle in its new cell
        if self.vel > 0:
            #   move Vehicle over an intersection if appropriate (so from a Road to Road.end.output_road or further)
            new_pos = self.pos + self.vel
            new_road = self.road
            while new_road is not None and new_pos > new_road.len - 1:
                if new_road.end.output_available():
                    new_pos -= new_road.len
                    new_road = new_road.end.output_road
                else:
                    # kill self by overwriting current cell
                    self.road.cells[self.pos] = None
                    self.road.end.removed.append(self)
                    return

            # check if Vehicles overwrite other Vehicles in their movement function
            if new_road.cells[new_pos] is not None:
                poor_fellow = new_road.cells[new_pos].name
                new_road.overwritten.append(poor_fellow)
                print(f"Collision! {poor_fellow} killed by {self.name}! Road: {new_road.name} Position: {new_pos} " +
                      f"From position: {self.pos} Velocity: {self.vel} Perceived distance: {self.dist_to_next}")

            # move vehicle
            new_road.cells[new_pos] = self

            # remove it from its previous position
            self.road.cells[self.pos] = None

            # update its position value
            self.pos = new_pos
            self.road = new_road
