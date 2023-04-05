from time import time


class CellularAutomata:
    def __init__(self, filepath):
        self.filepath = filepath
        self.matrix = []
        self.row_count = 0
        self.column_count = 0
        self.generation = 0
        self.load_matrix()

    def attribute_next_generation(self):
        self.matrix = self.compute_next_generation()
        self.generation += 1

    def compute_next_generation(self):
        next_generation_matrix = []

        for i in range(self.row_count):
            row = []
            for j in range(self.column_count):
                cell = self.matrix[i][j]
                neighbors = self.get_cell_neighbors(i, j)
                if cell == 0 and (neighbors > 1 and neighbors < 5):
                    row.append(1)
                elif cell == 1:
                    if neighbors > 3 and neighbors < 6:
                        row.append(1)
                    else:
                        row.append(0)
                else:
                    row.append(cell)
            next_generation_matrix.append(row)

        return next_generation_matrix

    def get_cell_neighbors(self, i, j):
        neighbors = 0

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                i_edge = i + x
                j_edge = j + y

                if i_edge < 0 or i_edge >= self.row_count or j_edge < 0 or j_edge >= self.column_count:
                    continue

                edge_cell = self.matrix[i_edge][j_edge]

                if edge_cell == 1:
                    neighbors += 1

        return neighbors

    def load_matrix(self):
        with open(self.filepath, 'r') as file:
            rows = [line.replace('\n', '').split()
                    for line in file.readlines()]

            self.row_count = len(rows)
            self.column_count = len(rows[0])

            self.matrix = []
            for i in range(self.row_count):
                row = []
                for j in range(self.column_count):
                    row.append(int(rows[i][j]))
                self.matrix.append(row)


class Pathfinder:
    def __init__(self, origin: tuple, destination: tuple):
        self.path = []
        self.explorers = []

        self.origin = origin
        self.destination = destination

        self.explorers.append([origin])

        self.MAXIMUM_EXPLORERS = 100

    def explore(self, matrix):
        new_explorers = []

        def valid_explorer(explorer):

            for new_explorer in new_explorers:
                if explorer == None or new_explorer == None:
                    return False

                if explorer[-1] == new_explorer[-1]:
                    return False

            return True

        for explorer in self.explorers[:]:
            explorer_x, explorer_y = explorer[-1]

            available_movements = self.available_movements(
                explorer_x, explorer_y, matrix)

            if len(available_movements) == 0:
                continue

            elif len(available_movements) == 1:
                new_explorer = explorer + [available_movements[0]]
                new_explorers.append(new_explorer)

            elif len(available_movements) > 1:
                for movement in available_movements:
                    clone_explorer = explorer.copy()
                    clone_explorer.append(movement)
                    new_explorer = clone_explorer.copy()

                    if valid_explorer(new_explorer):
                        new_explorers.append(new_explorer)

        new_explorers = list(filter(None, new_explorers))

        self.explorers.clear()
        self.explorers = new_explorers.copy()

        if len(self.explorers) == 0:
            return

        self.explorers.sort(key=lambda column: self.distance(column[-1]))
        self.explorers = self.explorers[:self.MAXIMUM_EXPLORERS]

    def available_movements(self, column, row, matrix):
        available_movements = []

        row_count = len(matrix)
        column_count = len(matrix[0])

        if column + 1 < column_count and (matrix[column + 1, row] == 0 or matrix[column + 1, row] == 4):
            if matrix[column + 1, row] == 4:
                return [(column + 1, row)]

            available_movements.append((column + 1, row))

        if column - 1 >= 0 and (matrix[column - 1, row] == 0 or matrix[column - 1, row] == 4):
            if matrix[column - 1, row] == 4:
                return [(column - 1, row)]

            available_movements.append((column - 1, row))

        if row + 1 < row_count and (matrix[column, row + 1] == 0 or matrix[column, row + 1] == 4):
            if matrix[column, row + 1] == 4:
                return [(column, row + 1)]

            available_movements.append((column, row + 1))

        if row - 1 >= 0 and (matrix[column, row - 1] == 0 or matrix[column, row - 1] == 4):
            if matrix[column, row - 1] == 4:
                return [(column, row - 1)]

            available_movements.append((column, row - 1))

        return available_movements

    def distance(self, movement):
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
                directions.append('R ')
            elif dx < 0:
                directions.append('L ')
            elif dy > 0:
                directions.append('D ')
            elif dy < 0:
                directions.append('U ')

        return ''.join(directions)


if __name__ == '__main__':
    matrix = input('Matrix file name: ')
    ca = CellularAutomata(f'{matrix}.txt')

    origin = destination = None
    for column in range(ca.column_count):
        for row in range(ca.row_count):
            if ca.matrix[column, row] == 3:
                origin = (column, row)
            elif ca.matrix[column, row] == 4:
                destination = (column, row)

    pf = Pathfinder(origin, destination)

    start_time = time()

    while pf.path == []:
        ca.attribute_next_generation()
        pf.move(ca.matrix)

    end_time = time()

    print(pf.path_to_string())

    print(f'Found in {end_time - start_time}s')
    print(f'Path length: {len(pf.path) - 1}')

    with open(f'{matrix}-{time()}.txt', 'w') as file:
        file.write(pf.path_to_string())
