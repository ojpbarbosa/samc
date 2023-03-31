import numpy as np
from time import time


class CellularAutomata:
    def __init__(self, filepath):
        self.filepath = filepath

        self.matrix = []
        self.column_count = 0
        self.row_count = 0

        self.generation = 0

        self.load_matrix()

    def attribute_next_generation(self):
        self.matrix = self.compute_next_generation()
        self.generation += 1

    def compute_next_generation(self):
        next_generation_matrix = np.ndarray(
            shape=(self.column_count, self.row_count), dtype=int)

        for x in range(self.column_count):
            for y in range(self.row_count):
                cell = self.matrix[x, y]

                neighbors = self.get_cell_neighbors(x, y)

                if cell == 0 and (neighbors > 1 and neighbors < 5):
                    next_generation_matrix[x, y] = 1

                elif cell == 1:
                    if neighbors > 3 and neighbors < 6:
                        next_generation_matrix[x, y] = 1

                    else:
                        next_generation_matrix[x, y] = 0

                else:
                    next_generation_matrix[x, y] = cell

        return next_generation_matrix

    def get_cell_neighbors(self, x, y):
        neighbors = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                x_edge = (x + i + self.column_count) % self.column_count
                y_edge = (y + j + self.row_count) % self.row_count

                edge_cell = self.matrix[x_edge, y_edge]

                if edge_cell == 1:
                    neighbors += 1

        return neighbors - self.matrix[x, y]

    def load_matrix(self):
        with open(self.filepath, 'r') as file:
            rows = [line.replace('\n', '').split(' ')
                    for line in file.readlines()]

            self.column_count = len(rows[0])
            self.row_count = len(rows)

            self.matrix = np.ndarray(
                shape=(self.column_count, self.row_count), dtype=int)

            for x in range(self.column_count):
                for y in range(self.row_count):
                    self.matrix[x, y] = int(rows[y][x])

    def clear_matrix(self):
        self.matrix = np.ndarray(
            shape=(self.column_count, self.row_count), dtype=int)

        for x in range(self.column_count):
            for y in range(self.row_count):
                self.matrix[x, y] = 0

        self.generation = 0

    def restart(self):
        self.clear_matrix()
        self.load_matrix()


class Pathfinder:
    def __init__(self, origin: tuple, destination: tuple):
        self.path = []                  # initialize an empty path
        self.explorers = []             # initialize an empty list of explorers

        self.origin = origin            # set the origin point
        self.destination = destination  # set the destination point

        # add the starting point as an initial explorer
        self.explorers.append([origin])

        self.MAXIMUM_EXPLORERS = 50       # set the maximum number of explorers

    def explore(self, matrix):
        new_explorers = []              # initialize a new list of explorers

        def valid_explorer(explorer):
            # check if the new explorer is not the same as any previous ones
            for new_explorer in new_explorers:
                if explorer == None or new_explorer == None:
                    return False

                if explorer[-1] == new_explorer[-1]:
                    return False

            return True

        for explorer in self.explorers[:]:
            # get the coordinates of the last point of the explorer
            explorer_x, explorer_y = explorer[-1]

            available_movements = self.available_movements(
                explorer_x, explorer_y, matrix)   # get the available movements for the current point

            # if there are no available movements, skip this explorer
            if len(available_movements) == 0:
                continue

            # if there is only one available movement, add it to the explorer
            elif len(available_movements) == 1:
                new_explorer = explorer + [available_movements[0]]
                new_explorers.append(new_explorer)

            # if there are multiple available movements, clone the explorer for each one
            elif len(available_movements) > 1:
                for movement in available_movements:
                    clone_explorer = explorer.copy()
                    clone_explorer.append(movement)
                    new_explorer = clone_explorer.copy()

                    if valid_explorer(new_explorer):
                        new_explorers.append(new_explorer)

        # remove any None values from the list of explorers
        new_explorers = list(filter(None, new_explorers))
        # clear the previous list of explorers
        self.explorers.clear()
        # set the new list of explorers
        self.explorers = new_explorers.copy()

        # check if there are any explorers that moved
        if len(self.explorers) == 0:
            return

        # limit to N closest explorers to destination
        # sort the explorers based on their distance to the destination
        self.explorers.sort(key=lambda x: self.distance(x[-1]))
        # keep only the closest self.MAXIMUM_EXPLORERS explorers
        self.explorers = self.explorers[:self.MAXIMUM_EXPLORERS]

    def available_movements(self, x, y, matrix):
        available_movements = []  # initialize a list of available movements
        # get the number of columns in the matrix
        column_count = matrix.shape[0]
        row_count = matrix.shape[1]  # get the number of rows in the matrix

        # check if the right movement is available
        if x + 1 < column_count and (matrix[x + 1, y] == 0 or matrix[x + 1, y] == 4):
            if matrix[x + 1, y] == 4:
                return [(x + 1, y)]

            available_movements.append((x + 1, y))

        # check if the left movement is available
        if x - 1 >= 0 and (matrix[x - 1, y] == 0 or matrix[x - 1, y] == 4):
            if matrix[x - 1, y] == 4:
                return [(x - 1, y)]

            available_movements.append((x - 1, y))

        # check if the down movement is available
        if y + 1 < row_count and (matrix[x, y + 1] == 0 or matrix[x, y + 1] == 4):
            if matrix[x, y + 1] == 4:
                return [(x, y + 1)]

            available_movements.append((x, y + 1))

        # check if the up movement is available
        if y - 1 >= 0 and (matrix[x, y - 1] == 0 or matrix[x, y - 1] == 4):
            if matrix[x, y - 1] == 4:
                return [(x, y - 1)]

            available_movements.append((x, y - 1))

        return available_movements

    def distance(self, movement):
        # manhattan distance calculation
        return abs(self.destination[0] - movement[0]) + abs(self.destination[1] - movement[1])

    def move(self, matrix):
        self.explore(matrix)

        for explorer in self.explorers:
            if explorer[-1] == self.destination:
                self.path = explorer
                self.explorers.clear()
                self.explorers = [explorer]
                return

    def path_to_string(self):
        directions = []
        for i in range(len(self.path) - 1):
            x0, y0 = self.path[i]
            x1, y1 = self.path[i + 1]
            dx, dy = x1 - x0, y1 - y0
            if dx > 0:
                directions.append('r ')
            elif dx < 0:
                directions.append('l ')
            elif dy > 0:
                directions.append('d ')
            elif dy < 0:
                directions.append('u ')

        return ''.join(directions)


if __name__ == '__main__':
    ca = CellularAutomata('data/input/matrix-i.txt')

    origin = destination = None
    for x in range(ca.column_count):
        for y in range(ca.row_count):
            if ca.matrix[x, y] == 3:
                origin = (x, y)
            elif ca.matrix[x, y] == 4:
                destination = (x, y)

    pf = Pathfinder(origin, destination)

    while pf.path == []:
        ca.attribute_next_generation()
        pf.move(ca.matrix)

    print(pf.path)
    print(pf.path_to_string().upper())

    with open(f'data/output/matrix-i-{time()}.txt', 'w') as file:
        file.write(pf.path_to_string().upper())
