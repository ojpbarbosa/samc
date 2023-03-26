import tkinter as tk
import numpy as np
import pygame
from time import sleep

from theme import colors


class CellularAutomata:
    def __init__(self, screen, columns=85, rows=65):
        self.screen = screen

        self.world = []

        root = tk.Tk()

        self.columns = columns
        self.rows = rows
        self.cell_size = root.winfo_screenwidth() // self.columns - 6

        self.world = np.ndarray(shape=(self.columns, self.rows), dtype=int)

        for y in range(self.rows):
            for x in range(self.columns):
                self.world[x, y] = 0

        self.generation = 0
        self.generation_timeout = 0.1

        self.paused = False

    def compute_next_generation(self):
        self.screen.fill(colors['primary'])

        for y in range(self.rows):
            for x in range(self.columns):
                if self.world[x, y] == 1:
                    pygame.draw.rect(self.screen, colors['secondary'],
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

                else:
                    pygame.draw.rect(self.screen, colors['shade'],
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)

        if not self.paused:
            next_generation_world = np.ndarray(
                shape=(self.columns, self.rows), dtype=int)

            for x in range(self.columns):
                for y in range(self.rows):
                    cell = self.world[x, y]
                    neighbors = self.get_cell_neighbors(x, y)

                    if cell == 0 and (neighbors > 1 and neighbors < 5):
                        next_generation_world[x, y] = 1
                        continue

                    if cell == 1:
                        if neighbors > 3 and neighbors < 6:
                            next_generation_world[x, y] = 1

                        else:
                            next_generation_world[x, y] = 0

            self.world = next_generation_world
            self.generation += 1

        sleep(self.generation_timeout)

    def get_cell_neighbors(self, x, y):
        neighbors = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                x_edge = (x + i + self.columns) % self.columns
                y_edge = (y + j + self.rows) % self.rows

                neighbors += self.world[x_edge, y_edge]

        neighbors -= self.world[x, y]

        return neighbors

    def handle_click(self, x, y):
        scaled_x = x // self.cell_size
        scaled_y = y // self.cell_size

        if scaled_x >= self.columns or scaled_y >= self.rows:
            pass

        elif self.world[scaled_x, scaled_y] == 0:
            self.world[scaled_x, scaled_y] = 1

        else:
            self.world[scaled_x, scaled_y] = 0

    def restart(self):
        self.world = np.ndarray(shape=(self.columns, self.rows), dtype=int)

        for y in range(self.rows):
            for x in range(self.columns):
                self.world[x, y] = 0

        self.generation = 0

        self.paused = True
