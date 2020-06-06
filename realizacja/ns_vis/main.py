import sys
import pygame as pg
from PIL import Image, ImageDraw

from ns_sim.main import Simulation
from ns_sim.roads import Road, Node
from ns_sim.agents import Vehicle
from ns_sim.settings import Config

from ns_vis.settings import *
from ns_vis.sprites import *

from random import randrange
from copy import deepcopy


class SimulationVisualization:
    def __init__(self, sim_object, sim_states=None):
        if sim_states is None:
            sim_states = []
        pg.init()
        self.playing = True
        self.running = True
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.font_name = pg.font.match_font(FONT)

        # simulation objects
        self.sim_object = sim_object  # initial Simulation() state
        self.sim_states = list([sim_object] + sim_states)  # list of Simulation() objects, pre-calculated and saved here
        self.current_state = 0

    def game_loop(self):
        #  always start playing when game loop starts:
        self.playing = True
        while self.playing:
            #  time passes
            self.clock.tick(FPS)

            #  user input
            self.events()

            #  update sprites
            self.update()

            #  draw to the screen
            self.draw()

    def new_game(self):

        #  set up the level
        self.setup()

        #  play the game loop
        self.game_loop()

        #  gameover screen
        self.show_go_screen()

    def setup(self):
        self.all_sprites = pg.sprite.Group()
        self.all_roads = pg.sprite.Group()
        self.all_vehicles = pg.sprite.Group()
        for index, r_data in enumerate(self.sim_object.roads):
            r_sprite = RoadSprite(self, r_data, x=V_SIZE + index * 5 * V_SIZE, angle=0)

    def show_go_screen(self):
        pass

    def events(self):
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                self.playing = False
                self.running = False

        self.sim_object.step()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.screen.blit(text_surface, text_rect)


c = Config(**{"simulation_duration": 6000})
s = Simulation(**{"config": c})
MID_NODE_COUNT = 20

# initialize nodes
# main source
node1 = Node(**{"type": 1, "config": s.config, "dest_range": (19, 20)})
s.nodes.append(node1)

# middle nodes
for i in range(MID_NODE_COUNT):
    new_node = Node(**{"type": randrange(0, 1), "chance_to_spawn": 0.1, "spawned_vehicles_limit": 50, "config": s.config, "dest_range": (19, 20)})
    s.nodes.append(new_node)

# main sink
node2 = Node(**{"type": -1, "config": s.config})
s.nodes.append(node2)

# initialize roads
for i in range(len(s.nodes) - 1):
    new_road = Road(**{"len": 25, "start": s.nodes[i], "end": s.nodes[i+1], "name": str(i), "config": s.config})
    s.roads.append(new_road)
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

    # prepare this step statistics
    full_road_cells = list()
    for r in s.roads:
        full_road_cells += r.cells
        total_overwritten += r.overwritten

    # prepare pixel coordinates
    pixels = list()
    for index, cell in enumerate(full_road_cells):
        if type(full_road_cells[index]) is Vehicle or index % 25 == 0:
            pixels.append((index, i))
    all_pixels.append(pixels)
    all_road_cells.append(full_road_cells)


# sum up the statistics
for n in s.nodes:
    if n.type >= 0:
        total_added += n.added
    if n.type <= 0:
        total_removed += n.removed


# for n in sv.sim_object.nodes:
#     if n.type >= 0:
#         total_added += n.added
#     if n.type <= 0:
#         total_removed += n.removed
#
# for r in sv.sim_object.roads:
#     full_road_cells += r.cells
#     total_overwritten += r.overwritten


for cell in full_road_cells:
    if cell is not None:
        left_on_the_road.append(cell)

print(f"{len(total_added)} joined the traffic: {total_added}")
print(f"{len(total_removed)} left the traffic alive: {total_removed}")
print(f"{len(total_overwritten)} killed on the road: {total_overwritten}")
print(f"{len(left_on_the_road)} left on the road: {left_on_the_road}")
print(f"The road looks like this: {full_road_cells}")
print(all_road_cells)
print(f"Blockers: {blockers}")

with Image.new("RGB", (len(full_road_cells), len(all_pixels))) as im:

    draw = ImageDraw.Draw(im)
    image = im.load()
    for pixel_row in all_pixels:
        for pixel_coord in pixel_row:
            print(pixel_coord)
            if pixel_coord[0] % 25 == 0:
                im.putpixel(pixel_coord, (255, 255, 0))
            else:
                im.putpixel(pixel_coord, (255, 255, 255))
    im.save("wykres.png", "PNG")
