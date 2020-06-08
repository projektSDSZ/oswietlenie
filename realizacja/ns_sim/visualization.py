from ns_sim.agents import Vehicle
from ns_sim.roads import Node, Road
from ns_sim.settings import Config
from ns_sim.simulation import Simulation

from PIL import Image, ImageDraw, ImageOps, ImageFont
from random import randrange, uniform


def draw_text(text, image_object, topleft_coords=(0, 0), angle=0, font_size=12, font_color=(255, 255, 255)):
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', font_size)
    txt_image = Image.new('L', (font_size * len(text), font_size))
    d = ImageDraw.Draw(txt_image)
    d.text((0, 0), text, font=font, fill=255)
    w = txt_image.rotate(angle, expand=1)
    image_object.paste(ImageOps.colorize(w, (0, 0, 0), font_color), topleft_coords, w)


c = Config(**{"sim_start_time": 18 * 3600, "simulation_duration": 3 * 3600, "visibility": 10,
              "sim_daytime_phases": [(7 * 3600, 0.03), (10 * 3600, 0.015), (15 * 3600, 0.03), (19 * 3600, 0.015)]})
s = Simulation(**{"config": c})

# data describing Cracow's First Bypass
kr_node_types = [0, 1, -1, 1, 0, 0, 0, -1, 0, 1, 0, 1, 0, 1, 0, -1, 0, -1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                 0]  # starting from Pawia St., counter-clockwise direction

kr_road_lengths_meter = [152, 56, 150, 50, 225, 300, 100, 77, 77, 77, 125, 70, 120, 85, 190, 135, 160, 80, 207, 140,
                         225, 100, 175, 56, 185, 65, 135, 100, 70]  # meters, require conversion
kr_road_lengths_cell = [val // c.cell_size for val in kr_road_lengths_meter]

kr_node_chance_to_spawn = [10, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 1, 10, 1, 1, 1, 10, 1, 5, 1,
                           1]  # values describing how often cars enter the bypass from the i-th node, in proportion to other nodes
kr_node_names = ["Pawia+Lubicz", "Zacisze", "pl. Matejki", "pl. Matejki", "Długa+Sławkowska", "Krowoderska",
                 "Garbarska", "pl. Szczepański", "Karmelicka", "Studencka", "Kapucyńska", "Jabłonowskich",
                 "Piłsudskiego", "Smoleńsk", "Zwierzyniecka+Franciszkańska", "Poselska", "pl. Na Groblach", "Podzamcze",
                 "Kanonicza", "Grodzka+Droga do Zamku", "Stradomska+Bernardyńska", "Św. Sebastiana", "Józefa Sarego",
                 "Dominikańska", "Starowiślna+Wielopole", "Zyblikiewicza", "Kopernika", "Marii Skłodowskiej-Curie",
                 "Zamenhofa"]

for n_type, n_chance_to_spawn, n_name in zip(kr_node_types, kr_node_chance_to_spawn, kr_node_names):
    new_node = Node(
        **{"type": n_type, "chance_to_spawn": s.curr_phase[1] * n_chance_to_spawn, "spawned_vehicles_limit": -1,
           "dest_range": (0, len(kr_node_types) // 2), "config": s.config, "name": n_name})
    s.nodes.append(new_node)

for index, r_len in enumerate(kr_road_lengths_cell):
    if index == len(kr_road_lengths_cell) - 1:
        new_road = Road(**{"len": r_len, "start": s.nodes[index], "end": s.nodes[0],
                           "config": s.config})
        s.roads.append(new_road)
        break
    new_road = Road(
        **{"len": r_len, "start": s.nodes[index], "end": s.nodes[index + 1], "name": str(index), "config": s.config})
    s.roads.append(new_road)

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

all_node_x_coords = list()

curr_cell_count = 0

# sum up the statistics
for index, n in enumerate(s.nodes):
    all_node_x_coords.append(curr_cell_count)
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

with open("stats.txt", "w") as statfile:
    print(f"{len(total_added)} joined the traffic", file=statfile)
    print(f"{len(total_removed)} left the traffic", file=statfile)
    print(f"{len(left_on_the_road)} are left on the road\n\n", file=statfile)
    print(f"Configuration:\n{s.config}\n\n\n", file=statfile)
    print(f"Nodes:\n")
    for n in s.nodes:
        print(str(n) + "\n", file=statfile)
    print(f"\n\nRoads:\n")
    for r in s.roads:
        print(str(r) + "\n", file=statfile)
    statfile.close()

with Image.new("RGB", (len(full_road_cells), len(all_pixels))) as im:
    image = im.load()
    draw = ImageDraw.Draw(im)

    # time grid, one line is quarter of an hour
    for i in range(s.config.simulation_duration):
        if i % 900 == 0:
            draw.line((0, i, im.size[0], i), fill=(0, 0, 255))

    # draw nodes
    for x in source_node_x_coords:
        draw.line((x, 0, x, im.size[1]), fill=(0, 255, 0))
    for x in sink_node_x_coords:
        draw.line((x, 0, x, im.size[1]), fill=(255, 0, 0))
    for x in universal_node_x_coords:
        draw.line((x, 0, x, im.size[1]), fill=(255, 255, 0))

    # draw vehicles
    for pixel_row in all_pixels:
        for pixel_coord in pixel_row:
            print(pixel_coord)
            im.putpixel(pixel_coord, (255, 255, 255))

    # draw phase beginning thresholds
    for phase in s.config.sim_daytime_phases:
        draw.line((0, phase[0], im.size[0], phase[0]), fill=(int(10000 * phase[1]), 200, 0))



    # write descriptions
    # for node, x in zip(s.nodes, all_node_x_coords):
    #     draw_text(node.name, im, (x, 0), 90, font_color=(255, 255, 0))

    im.save("wykres.png", "PNG")

for n in s.nodes:
    if n.input_available():
        blockers.append(n.input_road.cells[-1])
print(f"Blockers: {blockers}")
