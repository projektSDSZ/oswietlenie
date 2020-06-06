import pygame as pg
import math

from ns_vis.settings import *


class RoadSprite(pg.sprite.Sprite):
    def __init__(self, vis, road, x=0, y=0, angle=0):
        self.groups = vis.all_sprites, vis.all_roads
        pg.sprite.Sprite.__init__(self, self.groups)

        # setup hooks to parent Simulation() information
        self.vis = vis
        self.road = road

        # setup sprite image
        self.image = pg.Surface((2 * V_SIZE, self.road.len * V_SIZE), pg.SRCALPHA)
        # self.image.fill(WHITE)

        # setup sprite position inside Pygame screen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = angle  # initial angle of the road on screen

        # adjust image to angle
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # height offset h = n * (p / (len * root(1 + tan^2(angle))), where n - current list index, p - diagonal of the
        # Sprite, len - is len(road.cells)
        p = math.sqrt(self.rect.w ** 2 + self.rect.h ** 2)
        tan = self.rect.w / self.rect.h
        # h_const = (p / (len * root(1 + tan^2(angle)))
        h_const = p / (self.road.len * math.sqrt(1 + tan**2))
        for offset, v_data in enumerate(self.road.cells):
            # h_v = int(self.rect.h / self.road.len) * offset
            # w_v = int(self.rect.w / self.road.len) * offset
            h_v = int(offset * h_const) + V_SIZE // 2
            w_v = int(tan * h_v) + V_SIZE // 2
            if v_data is None:
                pg.draw.circle(self.image, WHITE, (w_v, h_v), V_SIZE // 2)
            else:
                pg.draw.circle(self.image, RED, (w_v, h_v), V_SIZE // 2)
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))


class VehicleSprite(pg.sprite.Sprite):
    def __init__(self, vehicle, vis, road_sprite, x=0, y=0, angle=0):
        self.groups = vis.all_sprites, vis.all_roads
        pg.sprite.Sprite.__init__(self, self.groups)

        # setup hooks to parent Simulation() information
        self.vis = vis
        self.road_sprite = road_sprite
        self.vehicle = vehicle

        # setup sprite image
        self.image = pg.Surface((V_SIZE, V_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.image, RED, (V_SIZE//2, V_SIZE//2), V_SIZE//2)

        # setup sprite position inside Pygame screen
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = angle  # initial angle of the road on screen

    def update(self, *args):
        pass
