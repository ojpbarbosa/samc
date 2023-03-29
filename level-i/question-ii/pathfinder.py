from celullar_automata import CellularAutomata


class Pathfinder:
    def __init__(self, ca: CellularAutomata, origin: tuple, destination: tuple):
        self.ca = ca

        self.path = []
        self.explorers = []

        self.origin = origin
        self.destination = destination

        self.explorers.append([origin])

    def explore(self):
        for explorer in self.explorers.copy():
            explorer_x, explorer_y = explorer[-1]
            print(explorer_x, explorer_y)

            available_movements = self.available_movements(
                explorer_x, explorer_y)

            if len(available_movements) == 0:
                self.explorers.remove(explorer)

            elif len(available_movements) == 1:
                new_explorer = explorer.append(available_movements[0])

                if new_explorer not in self.explorers:
                    self.explorers.append(new_explorer)

                self.explorers.remove(explorer)

            else:
                # return self.find_best_movement(available_movements)
                clone_explorer = explorer.copy()
                self.explorers.remove(explorer)

                # derivates explorers
                for movement in available_movements:
                    clone_explorer.append(movement)
                    self.explorers.append(clone_explorer.copy())

        self.explorers = list(filter(None, self.explorers))

        if len(self.explorers) == 0:
            return

        self.explorers.sort(key=lambda x: self.distance(x[-1]))
        self.explorers = self.explorers[:1]

    def available_movements(self, x, y):
        matrix = self.ca.compute_next_generation()

        available_movements = []

        if x + 1 < self.ca.column_count and (matrix[x + 1, y] == 0 or matrix[x + 1, y] == 4):
            if matrix[x + 1, y] == 4:
                return [(x + 1, y)]

            available_movements.append((x + 1, y))

        if x - 1 >= 0 and (matrix[x - 1, y] == 0 or matrix[x - 1, y] == 4):
            if matrix[x - 1, y] == 4:
                return [(x - 1, y)]

            available_movements.append((x - 1, y))

        if y + 1 < self.ca.row_count and (matrix[x, y + 1] == 0 or matrix[x, y + 1] == 4):
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

    def move(self):
        if len(self.explorers) == 0:
            # self.ca.restart()
            pass

        self.explore()

        for explorer in self.explorers:
            if self.is_finished(explorer):
                self.path = explorer
                return

    def is_finished(self, explorer):
        return explorer[-1] == self.destination
