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
                directions.append("r ")
            elif dx < 0:
                directions.append("l ")
            elif dy > 0:
                directions.append("d ")
            elif dy < 0:
                directions.append("u ")

        return "".join(directions)
