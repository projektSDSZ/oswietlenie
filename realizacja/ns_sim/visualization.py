from ns_sim.agents import Vehicle
from ns_sim.roads import Node, Road
from ns_sim.settings import Config
from ns_sim.main import Simulation

from PIL import Image, ImageDraw
from random import randrange, uniform

c = Config(**{"simulation_duration": 6000})
s = Simulation(**{"config": c})

# data describing Cracow's First Bypass
kr_node_types = [0, 1, -1, 1, 0, 0, 0, -1, 0, 1, 0, 1, 0, 1, 0, -1, 0, -1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # starting from Pawia St., counter-clockwise direction

kr_road_lengths_meter = [152, 56, 150, 50, 225, 300, 100, 77, 77, 77, 125, 70, 120, 85, 190, 135, 160, 80, 207, 140, 225, 100, 175, 56, 185, 65, 135, 100, 70]  # meters, require conversion
kr_road_lengths_cell = [val // c.cell_size for val in kr_road_lengths_meter]

for n_type in kr_node_types:
    new_node = Node(**{"type": n_type, "chance_to_spawn": 0.08, "spawned_vehicles_limit": -1, "dest_range": (0, len(kr_node_types) // 2), "config": s.config})
    s.nodes.append(new_node)

for index, r_len in enumerate(kr_road_lengths_cell):
    if index == len(kr_road_lengths_cell) - 1:
        new_road = Road(**{"len": r_len, "start": s.nodes[index], "end": s.nodes[0], "name": "ul.Zamenhofa",
                           "config": s.config})
        s.roads.append(new_road)
        break
    new_road = Road(**{"len": r_len, "start": s.nodes[index], "end": s.nodes[index + 1], "name": str(index), "config": s.config})
    s.roads.append(new_road)

# # initialize nodes
# MID_NODE_COUNT = 20
# # main source
# node1 = Node(**{"type": 1, "chance_to_spawn": 0.1, "spawned_vehicles_limit": -1, "config": s.config, "dest_range": (0, 10)})
# s.nodes.append(node1)
#
# # middle nodes
# for i in range(MID_NODE_COUNT):
#     new_node = Node(**{"type": randrange(-2, 5), "chance_to_spawn": 0.1, "spawned_vehicles_limit": -1, "config": s.config, "dest_range": (0, 10)})
#     s.nodes.append(new_node)
#
# # main sink
# node2 = Node(**{"type": -1, "config": s.config})
# s.nodes.append(node2)
#
# # initialize roads
# for i in range(len(s.nodes) - 1):
#     new_road = Road(**{"len": 25, "start": s.nodes[i], "end": s.nodes[i+1], "name": str(i), "config": s.config})
#     s.roads.append(new_road)
# roadCircle = Road(**{"len": 25, "start": node2, "end": node1, "name": "Full circle", "config": s.config})
# s.roads.append(roadCircle)

# sv = SimulationVisualization(s)
# sv.new_game()

total_added = list()
total_removed = list()
total_overwritten = list()

full_road_cells = list()
left_on_the_road = list()

# list of full_road_cells lists
all_road_cells = list()

# vehicles that permanently froze in place
blockers = list()

# run simulation
all_pixels = list()
for i in range(s.config.simulation_duration):

    # calculate current state
    s.step()

    '''GATHERING DATA FOR DRAWING'''
    # prepare this step statistics
    full_road_cells = list()
    for r in s.roads:
        full_road_cells += r.cells
        total_overwritten += r.overwritten  # checking for an old bug, may be replaced in the future
    '''\\GATHERING DATA FOR DRAWING'''

    '''DRAWING MAGIC'''
    # prepare pixel coordinates
    pixels = list()
    for index, cell in enumerate(full_road_cells):
        if type(full_road_cells[index]) is Vehicle:
            pixels.append((index, i))
    all_pixels.append(pixels)
    '''\\DRAWING MAGIC'''
    all_road_cells.append(full_road_cells)

source_node_x_coords = list()
sink_node_x_coords = list()
universal_node_x_coords = list()

curr_cell_count = 0

# sum up the statistics
for index, n in enumerate(s.nodes):
    if n.input_road is not None and index > 0:
        curr_cell_count += len(n.input_road.cells)
    if n.type >= 0:
        if n.type > 0:
            source_node_x_coords.append(curr_cell_count)  # node pixel data
        total_added += n.added
    if n.type <= 0:
        if n.type < 0:
            sink_node_x_coords.append(curr_cell_count)  # node pixel data
        total_removed += n.removed
    if n.type == 0:
        universal_node_x_coords.append(curr_cell_count)  # node pixel data


for cell in full_road_cells:
    if cell is not None:
        left_on_the_road.append(cell)

print(f"{len(total_added)} joined the traffic: {total_added}")
print(f"{len(total_removed)} left the traffic alive: {total_removed}")
print(f"{len(total_overwritten)} killed on the road: {total_overwritten}")
print(f"{len(left_on_the_road)} left on the road: {left_on_the_road}")
print(f"The road looks like this: {full_road_cells}")
print(all_road_cells)

with Image.new("RGB", (len(full_road_cells), len(all_pixels))) as im:

    image = im.load()

    # draw vehicles
    for pixel_row in all_pixels:
        for pixel_coord in pixel_row:
            print(pixel_coord)
            im.putpixel(pixel_coord, (255, 255, 255))

    # draw nodes
    draw = ImageDraw.Draw(im)
    for x in source_node_x_coords:
        draw.line((x, 0, x, im.size[1]), fill=(0, 255, 0))
    for x in sink_node_x_coords:
        draw.line((x, 0, x, im.size[1]), fill=(255, 0, 0))
    for x in universal_node_x_coords:
        draw.line((x, 0, x, im.size[1]), fill=(255, 255, 0))
    im.save("wykres.png", "PNG")

for n in s.nodes:
    if n.input_available():
        blockers.append(n.input_road.cells[-1])
print(f"Blockers: {blockers}")
