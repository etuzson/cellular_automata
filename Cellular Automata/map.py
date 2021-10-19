import globals
import pygame
import sys
import random
from rule import Rule


class Map:

    def __init__(self, nrows):
        self.nrows = nrows
        self.ncols = nrows * 2
        self.grid = [[0 for i in range(self.ncols)] for i in range(self.nrows)]
        self.grid_colors = [[(255, 255, 255) for i in range(self.ncols)] for i in range(self.nrows)]
        self.grid_width = globals.WIN_WIDTH // self.ncols

        self.show_grid = False
        self.show_colors = True
        self.previous_frame_cache = {}

    def draw(self):
        current_y = 0
        for i, row in enumerate(self.grid):
            current_x = 0
            if self.show_grid:
                pygame.draw.line(globals.win, globals.WHITE, (current_x, current_y), (globals.WIN_WIDTH, current_y), width=1)
            for j, col in enumerate(row):
                if self.show_grid:
                    pygame.draw.line(globals.win, globals.WHITE, (current_x, current_y), (current_x, globals.WIN_HEIGHT), width=1)
                if col == 1:
                    color = globals.WHITE
                    if self.show_colors:
                        color = self.grid_colors[i][j]
                    pygame.draw.rect(globals.win, color, (current_x, current_y, self.grid_width, self.grid_width))
                current_x += self.grid_width
            current_y += self.grid_width

    def randomize(self, typeof="uniform", p=0.5):
        if typeof == "uniform":
            for i, row in enumerate(self.grid):
                for j, col in enumerate(row):
                    if random.random() <= p:
                        self.grid[i][j] = 1
                    else:
                        self.grid[i][j] = 0
                    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    self.grid_colors[i][j] = random_color

    def point_to_grid_index(self, point):
        row = point.y // self.grid_width
        col = point.x // self.grid_width
        return row, col

    def rule1(self):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if i == 0:
                    if j == 0:
                        continue
                    elif self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1:
                        self.grid[i][j] = 1
                elif i == self.nrows - 1:
                    if j == self.ncols - 1:
                        continue
                    elif self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 1
                elif j == 0:
                    if self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 1
                elif j == self.ncols - 1:
                    if self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1:
                        self.grid[i][j] = 1
                else:
                    if self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1 and self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 0
                    elif self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1:
                        self.grid[i][j] = 1
                    elif self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 0

    def rule2(self):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if i == 0:
                    if j == 0:
                        continue
                    elif self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1:
                        self.grid[i][j] = 1
                elif i == self.nrows - 1:
                    if j == self.ncols - 1:
                        continue
                    elif self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 1
                elif j == 0:
                    if self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 1
                elif j == self.ncols - 1:
                    if self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1:
                        self.grid[i][j] = 1
                else:
                    if self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1 and self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 0
                    elif self.grid[i + 1][j] == 1 and self.grid[i][j - 1] == 1:
                        self.grid[i][j] = 1
                    elif self.grid[i - 1][j] == 1 and self.grid[i][j + 1] == 1:
                        self.grid[i][j] = 1

    def run_rule(self, rule):
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                for configuration in rule.configurations:
                    if self.grid[i][j] == configuration[0]:
                        if configuration[-1] == 0:
                            if i == 0:
                                if j == 0:
                                    if self.grid[i][j + 1] == configuration[5] and self.grid[i + 1][j] == configuration[7] and self.grid[i + 1][j + 1] == configuration[8]:
                                        self.grid[i][j] = configuration[9]
                                        avg_R = (self.grid_colors[i][j + 1][0] + self.grid_colors[i + 1][j][0] + self.grid_colors[i + 1][j + 1][0]) // 3
                                        avg_G = (self.grid_colors[i][j + 1][1] + self.grid_colors[i + 1][j][1] + self.grid_colors[i + 1][j + 1][1]) // 3
                                        avg_B = (self.grid_colors[i][j + 1][2] + self.grid_colors[i + 1][j][2] + self.grid_colors[i + 1][j + 1][2]) // 3
                                        self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                                elif j == self.ncols - 1:
                                    if self.grid[i][j - 1] == configuration[4] and self.grid[i + 1][j] == configuration[7] and self.grid[i + 1][j - 1] == configuration[6]:
                                        self.grid[i][j] = configuration[9]
                                        avg_R = (self.grid_colors[i][j - 1][0] + self.grid_colors[i + 1][j][0] +
                                                 self.grid_colors[i + 1][j - 1][0]) // 3
                                        avg_G = (self.grid_colors[i][j - 1][1] + self.grid_colors[i + 1][j][1] +
                                                 self.grid_colors[i + 1][j - 1][1]) // 3
                                        avg_B = (self.grid_colors[i][j - 1][2] + self.grid_colors[i + 1][j][2] +
                                                 self.grid_colors[i + 1][j - 1][2]) // 3
                                        self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                                elif self.grid[i][j - 1] == configuration[4] and self.grid[i][j + 1] == configuration[5] and self.grid[i + 1][j - 1] == configuration[6] and self.grid[i + 1][j] == configuration[7] and self.grid[i + 1][j + 1] == configuration[8]:
                                    self.grid[i][j] = configuration[9]
                                    avg_R = (self.grid_colors[i][j - 1][0] + self.grid_colors[i][j + 1][0] + self.grid_colors[i + 1][j - 1][0] + self.grid_colors[i + 1][j][0] +
                                             self.grid_colors[i + 1][j + 1][0]) // 5
                                    avg_G = (self.grid_colors[i][j - 1][1] + self.grid_colors[i][j + 1][1] + self.grid_colors[i + 1][j - 1][1] + self.grid_colors[i + 1][j][1] +
                                             self.grid_colors[i + 1][j + 1][1]) // 5
                                    avg_B = (self.grid_colors[i][j - 1][2] + self.grid_colors[i][j + 1][2] + self.grid_colors[i + 1][j - 1][2] + self.grid_colors[i + 1][j][2] +
                                             self.grid_colors[i + 1][j + 1][2]) // 5
                                    self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                            elif i == self.nrows - 1:
                                if j == 0:
                                    if self.grid[i][j + 1] == configuration[5] and self.grid[i - 1][j] == configuration[2] and self.grid[i - 1][j + 1] == configuration[3]:
                                        self.grid[i][j] = configuration[9]
                                        avg_R = (self.grid_colors[i][j + 1][0] + self.grid_colors[i - 1][j][0] +
                                                 self.grid_colors[i - 1][j + 1][0]) // 3
                                        avg_G = (self.grid_colors[i][j + 1][1] + self.grid_colors[i - 1][j][1] +
                                                 self.grid_colors[i - 1][j + 1][1]) // 3
                                        avg_B = (self.grid_colors[i][j + 1][2] + self.grid_colors[i - 1][j][2] +
                                                 self.grid_colors[i - 1][j + 1][2]) // 3
                                        self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                                elif j == self.ncols - 1:
                                    if self.grid[i][j - 1] == configuration[4] and self.grid[i - 1][j] == configuration[2] and self.grid[i - 1][j - 1] == configuration[1]:
                                        self.grid[i][j] = configuration[9]
                                        avg_R = (self.grid_colors[i][j - 1][0] + self.grid_colors[i - 1][j][0] +
                                                 self.grid_colors[i - 1][j - 1][0]) // 3
                                        avg_G = (self.grid_colors[i][j - 1][1] + self.grid_colors[i - 1][j][1] +
                                                 self.grid_colors[i - 1][j - 1][1]) // 3
                                        avg_B = (self.grid_colors[i][j - 1][2] + self.grid_colors[i - 1][j][2] +
                                                 self.grid_colors[i - 1][j - 1][2]) // 3
                                        self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                                elif self.grid[i][j - 1] == configuration[4] and self.grid[i][j + 1] == configuration[5] and self.grid[i - 1][j - 1] == configuration[1] and self.grid[i - 1][j] == configuration[2] and self.grid[i - 1][j + 1] == configuration[3]:
                                    self.grid[i][j] = configuration[9]
                                    avg_R = (self.grid_colors[i][j - 1][0] + self.grid_colors[i][j + 1][0] +
                                             self.grid_colors[i - 1][j - 1][0] + self.grid_colors[i - 1][j][0] +
                                             self.grid_colors[i - 1][j + 1][0]) // 5
                                    avg_G = (self.grid_colors[i][j - 1][1] + self.grid_colors[i][j + 1][1] +
                                             self.grid_colors[i - 1][j - 1][1] + self.grid_colors[i - 1][j][1] +
                                             self.grid_colors[i - 1][j + 1][1]) // 5
                                    avg_B = (self.grid_colors[i][j - 1][2] + self.grid_colors[i][j + 1][2] +
                                             self.grid_colors[i - 1][j - 1][2] + self.grid_colors[i - 1][j][2] +
                                             self.grid_colors[i - 1][j + 1][2]) // 5
                                    self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                            elif j == 0:
                                if self.grid[i - 1][j] == configuration[2] and self.grid[i - 1][j + 1] == configuration[3] and self.grid[i][j + 1] == configuration[5] and self.grid[i + 1][j] == configuration[7] and self.grid[i + 1][j + 1] == configuration[8]:
                                    self.grid[i][j] = configuration[9]
                                    avg_R = (self.grid_colors[i - 1][j][0] + self.grid_colors[i - 1][j + 1][0] +
                                             self.grid_colors[i][j + 1][0] + self.grid_colors[i + 1][j][0] +
                                             self.grid_colors[i + 1][j + 1][0]) // 5
                                    avg_G = (self.grid_colors[i - 1][j][1] + self.grid_colors[i - 1][j + 1][1] +
                                             self.grid_colors[i][j + 1][1] + self.grid_colors[i + 1][j][1] +
                                             self.grid_colors[i + 1][j + 1][1]) // 5
                                    avg_B = (self.grid_colors[i - 1][j][2] + self.grid_colors[i - 1][j + 1][2] +
                                             self.grid_colors[i][j + 1][2] + self.grid_colors[i + 1][j][2] +
                                             self.grid_colors[i + 1][j + 1][2]) // 5
                                    self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                            elif j == self.ncols - 1:
                                if self.grid[i - 1][j] == configuration[2] and self.grid[i - 1][j - 1] == configuration[1] and self.grid[i][j - 1] == configuration[4] and self.grid[i + 1][j - 1] == configuration[6] and self.grid[i + 1][j] == configuration[7]:
                                    self.grid[i][j] = configuration[9]
                                    avg_R = (self.grid_colors[i - 1][j][0] + self.grid_colors[i - 1][j - 1][0] +
                                             self.grid_colors[i][j - 1][0] + self.grid_colors[i + 1][j - 1][0] +
                                             self.grid_colors[i + 1][j][0]) // 5
                                    avg_G = (self.grid_colors[i - 1][j][1] + self.grid_colors[i - 1][j - 1][1] +
                                             self.grid_colors[i][j - 1][1] + self.grid_colors[i + 1][j - 1][1] +
                                             self.grid_colors[i + 1][j][1]) // 5
                                    avg_B = (self.grid_colors[i - 1][j][2] + self.grid_colors[i - 1][j - 1][2] +
                                             self.grid_colors[i][j - 1][2] + self.grid_colors[i + 1][j - 1][2] +
                                             self.grid_colors[i + 1][j][2]) // 5
                                    self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                            else:
                                if self.grid[i - 1][j - 1] == configuration[1] and self.grid[i - 1][j] == configuration[2] and self.grid[i - 1][j + 1] == configuration[3] and self.grid[i][j - 1] == configuration[4] and self.grid[i][j + 1] == configuration[5] and self.grid[i + 1][j - 1] == configuration[6] and self.grid[i + 1][j] == configuration[7] and self.grid[i + 1][j + 1] == configuration[8]:
                                    self.grid[i][j] = configuration[9]
                                    avg_R = (self.grid_colors[i - 1][j - 1][0] + self.grid_colors[i - 1][j][0] + self.grid_colors[i - 1][j + 1][0] +
                                             self.grid_colors[i][j - 1][0] + self.grid_colors[i][j + 1][0] +
                                             self.grid_colors[i + 1][j - 1][0] + self.grid_colors[i + 1][j][0] + self.grid_colors[i + 1][j + 1][0]) // 8
                                    avg_G = (self.grid_colors[i - 1][j - 1][1] + self.grid_colors[i - 1][j][1] + self.grid_colors[i - 1][j + 1][1] +
                                             self.grid_colors[i][j - 1][1] + self.grid_colors[i][j + 1][1] +
                                             self.grid_colors[i + 1][j - 1][1] + self.grid_colors[i + 1][j][1] + self.grid_colors[i + 1][j + 1][1]) // 8
                                    avg_B = (self.grid_colors[i - 1][j - 1][2] + self.grid_colors[i - 1][j][2] + self.grid_colors[i - 1][j + 1][2] +
                                             self.grid_colors[i][j - 1][2] + self.grid_colors[i][j + 1][2] +
                                             self.grid_colors[i + 1][j - 1][2] + self.grid_colors[i + 1][j][2] + self.grid_colors[i + 1][j + 1][2]) // 8
                                    self.grid_colors[i][j] = (avg_R, avg_G, avg_B)
                        elif configuration[-1] == 1:
                            count = int(str(configuration[1]) + str(configuration[2]) + str(configuration[3]), 2)
                            if i == 0:
                                if j == 0:
                                    if sum([self.grid[i][j + 1], self.grid[i + 1][j], self.grid[i + 1][j + 1]]) >= count:
                                        self.grid[i][j] = configuration[9]
                                elif j == self.ncols - 1:
                                    if sum([self.grid[i][j - 1], self.grid[i + 1][j], self.grid[i + 1][j - 1]]) >= count:
                                        self.grid[i][j] = configuration[9]
                                elif sum([self.grid[i][j - 1], self.grid[i][j + 1], self.grid[i + 1][j - 1], self.grid[i + 1][j], self.grid[i + 1][j + 1]]) >= count:
                                    self.grid[i][j] = configuration[9]
                            elif i == self.nrows - 1:
                                if j == 0:
                                    if sum([self.grid[i][j + 1], self.grid[i - 1][j], self.grid[i - 1][j + 1]]) >= count:
                                        self.grid[i][j] = configuration[9]
                                elif j == self.ncols - 1:
                                    if sum([self.grid[i][j - 1], self.grid[i - 1][j], self.grid[i - 1][j - 1]]) >= count:
                                        self.grid[i][j] = configuration[9]
                                elif sum([self.grid[i][j - 1], self.grid[i][j + 1], self.grid[i - 1][j - 1], self.grid[i - 1][j], self.grid[i - 1][j + 1]]) >= count:
                                    self.grid[i][j] = configuration[9]
                            elif j == 0:
                                if sum([self.grid[i - 1][j], self.grid[i - 1][j + 1], self.grid[i][j + 1],
                                        self.grid[i + 1][j], self.grid[i + 1][j + 1]]) >= count:
                                    self.grid[i][j] = configuration[9]
                            elif j == self.ncols - 1:
                                if sum([self.grid[i - 1][j], self.grid[i - 1][j - 1], self.grid[i][j - 1],
                                        self.grid[i + 1][j], self.grid[i + 1][j - 1]]) >= count:
                                    self.grid[i][j] = configuration[9]
                            else:
                                if sum([self.grid[i - 1][j - 1], self.grid[i - 1][j], self.grid[i - 1][j + 1],
                                        self.grid[i][j - 1], self.grid[i][j + 1],
                                        self.grid[i + 1][j - 1], self.grid[i + 1][j], self.grid[i + 1][j + 1]]) >= count:
                                    self.grid[i][j] = configuration[9]

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Cellular Automata")
    map = Map(nrows=50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        map.draw()
        pygame.display.update()
