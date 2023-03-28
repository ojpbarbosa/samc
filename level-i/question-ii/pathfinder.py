from celullar_automata import CellularAutomata


class Pathfinder:
    def __init__(self, ca: CellularAutomata, origin_x: int, origin_y: int, destination_x: int, destination_y: int):
        self.ca = ca

        self.path = []
        self.visited = []

        self.origin_x = origin_x
        self.origin_y = origin_y
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.current_x = origin_x
        self.current_y = origin_y

    def find_next_movement(self):
        available_movements = self.available_movements(
            self.current_x, self.current_y)

        if len(available_movements) == 0:
            return self.path.pop()

        elif len(available_movements) == 1:
            return available_movements[0]

        else:
            return self.find_best_movement(available_movements)

    def available_movements(self, x, y):
        self.matrix = self.ca.compute_next_generation()

        available_movements = []

        if self.matrix[x + 1, y] == 0 and x + 1 < self.ca.column_count and (x + 1, y) not in self.visited:
            available_movements.append((x + 1, y))

        if self.matrix[x - 1, y] == 0 and x - 1 >= 0 and (x - 1, y) not in self.visited:
            available_movements.append((x - 1, y))

        if self.matrix[x, y + 1] == 0 and y + 1 < self.ca.row_count and (x, y + 1) not in self.visited:
            available_movements.append((x, y + 1))

        if self.matrix[x, y - 1] == 0 and y - 1 >= 0 and (x, y - 1) not in self.visited:
            available_movements.append((x, y - 1))

        return available_movements

    def find_best_movement(self, available_movements):
        best_movement = available_movements[0]

        for movement in available_movements:
            if self.distance(movement) < self.distance(best_movement):
                best_movement = movement

        return best_movement


    def distance(self, movement):
        return abs(self.destination_x - movement[0]) + abs(self.destination_y - movement[1])


    def move(self):
        next_movement = self.find_next_movement()

        self.current_x = next_movement[0]
        self.current_y = next_movement[1]

        self.path.append(next_movement)
        self.visited.append(next_movement)

        return next_movement

    def is_finished(self):
        return self.current_x == self.destination_x and self.current_y == self.destination_y
