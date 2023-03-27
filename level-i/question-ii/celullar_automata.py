import numpy as np
from time import sleep


class CellularAutomata:
    def __init__(self, filepath):
        self.filepath = filepath

        self.matrix = []
        self.column_count = 0
        self.row_count = 0

        self.generation = 0
        self.generation_interval = 0.1

        self.load_matrix()

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

        self.matrix = next_generation_matrix
        self.generation += 1

        sleep(self.generation_interval)

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
