"""Class for managing Pages (e.g. main menu, options, game, etc.)"""
from utility import *
import globals
from map import *
import pygame
import random
import sys
import _pickle
from rule import Rule


class Page:

    def __init__(self, win, name, clock, bg_color):
        if not isinstance(win, pygame.Surface): raise TypeError("window has to be a pygame.Surface object")
        if not is_string(name): raise TypeError("name has to be a string")
        if not isinstance(clock, type(pygame.time.Clock())): raise TypeError("clock has to be a pygame.time.Clock object")
        if not is_rgb_color_value(bg_color) and bg_color is not None: raise TypeError("bg_color has to be a RGB tuple")
        self.win = win
        self.name = name
        self.clock = clock
        self.bg_color = bg_color

    def mainloop(self):
        pass


class MainPage(Page):

    def __init__(self, win, name, clock, bg_color=None):
        super().__init__(win, name, clock, bg_color)

        self.drawable_entities = []

        self.map = Map(nrows=100)
        self.p = 0.2
        self.map.randomize(p=self.p)
        self.drawable_entities.append(self.map)

        self.rule = Rule(randomize=True)
        print(self.rule.configurations)

    def mainloop(self):
        while True:

            globals.dt = self.clock.tick(globals.FPS)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.p = 0.01
                        self.map.randomize(p=self.p)
                        self.rule = Rule(randomize=True)
                        print(self.rule.configurations)
                    elif event.key == pygame.K_t:
                        self.rule = Rule(randomize=True)
                        print(self.rule.configurations)
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    pos = Point(pos[0], pos[1])
                    map_grid_index = self.map.point_to_grid_index(pos)
                    self.map.grid[map_grid_index[0]][map_grid_index[1]] = 1

            self.map.run_rule(self.rule)
            globals.win.fill(globals.BLACK)
            for drawable_entity in self.drawable_entities:
                drawable_entity.draw()
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Cellular Automata")
    page = MainPage(win=globals.win, name="Main Page", clock=globals.clock)
    page.mainloop()
