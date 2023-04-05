from time import time
import numpy as np
from numba import njit
from multiprocessing import Pool


class CellularAutomata:
    def __init__(self, filepath):
        self.filepath = filepath
        self.matrix = np.array([])
        self.row_count = 0
        self.column_count = 0
        self.generation = 0
        self.load_matrix()

    def attribute_next_generation(self):
        self.matrix = self.compute_next_generation()
        self.generation += 1

    def compute_next_generation(self):
        with Pool(processes=4) as pool:
            chunked_matrices = np.array_split(self.matrix, 4)
            next_generation_matrices = pool.map(self.compute_next_generation_chunk, chunked_matrices)
            return np.concatenate(next_generation_matrices)

    @staticmethod
    @njit(fastmath=True)
    def compute_next_generation_chunk(matrix):
        next_generation_matrix = np.zeros(shape=matrix.shape, dtype=np.int32)

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                cell = matrix[i, j]
                neighbors = CellularAutomata.get_cell_neighbors(matrix, i, j)

                if cell == 0 and (neighbors > 1 and neighbors < 5):
                    next_generation_matrix[i, j] = 1
                elif cell == 1:
                    if neighbors > 3 and neighbors < 6:
                        next_generation_matrix[i, j] = 1

        return next_generation_matrix

    @staticmethod
    @njit(fastmath=True)
    def get_cell_neighbors(matrix, i, j):
        neighbors = 0

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                i_edge = i + x
                j_edge = j + y

                if i_edge < 0 or i_edge >= matrix.shape[0] or j_edge < 0 or j_edge >= matrix.shape[1]:
                    continue

                edge_cell = matrix[i_edge, j_edge]

                if edge_cell == 1:
                    neighbors += 1

        return neighbors

    def load_matrix(self):
        with open(self.filepath, 'r') as file:
            rows = [line.strip().split() for line in file]

            self.row_count = len(rows)
            self.column_count = len(rows[0])

            self.matrix = np.zeros(shape=(self.row_count, self.column_count), dtype=np.int32)
            for i in range(self.row_count):
                for j in range(self.column_count):
                    self.matrix[i, j] = int(rows[i][j])

if __name__ == '__main__':
    automata = CellularAutomata('input.txt')

    for i in range(100):
        start = time()
        automata.attribute_next_generation()
        end = time()
        print(f'Generation {i + 1} took {end - start}s')
