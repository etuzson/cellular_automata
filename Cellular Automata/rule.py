import globals
import utility
import random


class Rule:

    def __init__(self, configurations=None, randomize=False):
        # 1'st bit is whether current cell should be 1 or 0
        # next 8 bits indicate state of cells around current cell going from top left clockwise
        # second last bit is what to set current bit to given that surrounding cells match configuration
        # last int is the type of rule: 0 = basic configuration rule, 1 = count of neighbors
        if configurations is None:
            self.configurations = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        else:
            self.configurations = configurations
        if randomize:
            self.randomize()

    def randomize(self):
        n_configurations = random.randint(1, 5)
        self.configurations = [[0 for i in range(len(self.configurations[0]))] for i in range(n_configurations)]
        for configuration in self.configurations:
            for i in range(len(self.configurations[0])):
                if random.random() <= random.random():
                    configuration[i] = 1
            if configuration[0] == 1 and configuration[9] == 1:
                configuration[9] = 0
            elif configuration[0] == 0 and configuration[9] == 0:
                configuration[9] = 1

