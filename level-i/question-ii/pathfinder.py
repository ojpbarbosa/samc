from celullar_automata import CellularAutomata


class Pathfinder:
    def __init__(self, ca: CellularAutomata, origin: tuple, destination: tuple):
        self.path = []
        self.explorers = []

        self.origin = origin
        self.destination = destination

        self.explorers.append([origin])

        self.dead_end = False

    def explore(self, matrix):
        new_explorers = []

        def valid_explorer(explorer):
            for new_explorer in new_explorers:
                if explorer == None or new_explorer == None:
                    return False

                if explorer[-1] == new_explorer[-1]:
                    return False

            return True

        # new_matrix = self.ca.compute_next_generation()

        for explorer in self.explorers.copy():
            explorer_x, explorer_y = explorer[-1]

            available_movements = self.available_movements(
                explorer_x, explorer_y, matrix)

            if len(available_movements) == 0:
                continue

            elif len(available_movements) == 1:
                new_explorer = explorer.append(available_movements[0])

                if new_explorer not in new_explorers and valid_explorer(new_explorer):
                    new_explorers.append(new_explorer)

            elif len(available_movements) > 1:
                # derivates explorers
                available_movements = list(filter(None, available_movements))
                available_movements.sort(key=lambda x: self.distance(x))
                for movement in available_movements:
                    clone_explorer = explorer.copy()
                    clone_explorer.append(movement)
                    new_explorer = clone_explorer.copy()

                    if new_explorer not in new_explorers and valid_explorer(new_explorer):
                        new_explorers.append(new_explorer)

            print(explorer[-1], len(available_movements), len(new_explorers))

        new_explorers = list(filter(None, new_explorers))

        if len(new_explorers) == 0:
            self.dead_end = True
            return

        self.explorers.clear()
        self.explorers = new_explorers.copy()

        if len(self.explorers) == 0:
            return

        self.explorers.sort(key=lambda x: self.distance(x[-1]))
        # self.explorers = self.explorers[:30]

    def available_movements(self, x, y, matrix):
        available_movements = []
        column_count = matrix.shape[0]
        row_count = matrix.shape[1]

        if x + 1 < column_count and (matrix[x + 1, y] == 0 or matrix[x + 1, y] == 4):
            if matrix[x + 1, y] == 4:
                return [(x + 1, y)]

            available_movements.append((x + 1, y))

        if x - 1 >= 0 and (matrix[x - 1, y] == 0 or matrix[x - 1, y] == 4):
            if matrix[x - 1, y] == 4:
                return [(x - 1, y)]

            available_movements.append((x - 1, y))

        if y + 1 < row_count and (matrix[x, y + 1] == 0 or matrix[x, y + 1] == 4):
            if matrix[x, y + 1] == 4:
                return [(x, y + 1)]

            available_movements.append((x, y + 1))

        if y - 1 >= 0 and (matrix[x, y - 1] == 0 or matrix[x, y - 1] == 4):
            if matrix[x, y - 1] == 4:
                return [(x, y - 1)]

            available_movements.append((x, y - 1))

        return available_movements

    def find_best_movement(self, available_movements):
        best_movement = available_movements[0]

        for movement in available_movements:
            if self.distance(movement) < self.distance(best_movement):
                best_movement = movement

        return best_movement

    def distance(self, movement):
        return abs(self.destination[0] - movement[0]) + abs(self.destination[1] - movement[1])

    def move(self, matrix):
        self.explore(matrix)

        for explorer in self.explorers:
            if self.is_finished(explorer):
                self.path = explorer
                self.explorers.clear()
                self.explorers = [explorer]
                return

    def is_finished(self, explorer):
        return explorer[-1] == self.destination

    def path_to_string(self):
        directions = []
        for i in range(len(self.path) - 1):
            x0, y0 = self.path[i]
            x1, y1 = self.path[i + 1]
            dx, dy = x1 - x0, y1 - y0
            if dx > 0:
                directions.append("r ")
            elif dx < 0:
                directions.append("l ")
            elif dy > 0:
                directions.append("d ")
            elif dy < 0:
                directions.append("u ")

        return "".join(directions).upper()
