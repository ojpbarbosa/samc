
import pygame
import darkdetect
import tkinter as tk
import sys
import os
from time import sleep

parent_path = os.path.abspath('.')
sys.path.insert(1, parent_path)

import celullar_automata
import pathfinder
import button
import theme


def view():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.set_caption('Stone Automata Maze Challenge')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(
        dir_path, 'images', f'samc-icon-{str(darkdetect.theme()).lower()}.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # TODO: add select file button as initial screen
    parent_path = os.path.abspath('../question-ii')
    matrix_path = os.path.join(parent_path, 'data', 'input', 'matrix-i.txt')

    ca = celullar_automata.CellularAutomata(matrix_path)

    generation_interval = 0

    origin = destination = None

    for x in range(ca.column_count):
        for y in range(ca.row_count):
            if ca.matrix[x, y] == 3:
                origin = (x, y)

            elif ca.matrix[x, y] == 4:
                destination = (x, y)

    """
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    """

    screen_width = 1920
    screen_height = 1080

    cell_size = screen_height // ca.row_count

    paused = running = True

    font_path = os.path.join(dir_path, 'fonts', 'emulogic.ttf')
    font = pygame.font.Font(font_path, 24)

    restart_button_x = screen_width - \
        (screen_width - cell_size * ca.column_count) // 2 - 120
    restart_button_y = 60

    restart_button = button.Button(
        screen, font, theme.colors['green'], theme.colors['background'], restart_button_x, restart_button_y, 240, 60, 'restart')

    explorer_path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (17, 11), (18, 11), (18, 12), (18, 13), (19, 13), (18, 13), (19, 13), (19, 14), (20, 14), (20, 15), (20, 16), (20, 17), (19, 17), (20, 17), (20, 18), (21, 18), (21, 17), (22, 17), (21, 17), (21, 16), (22, 16), (21, 16), (21, 17), (21, 18), (21, 19), (21, 20), (22, 20), (22, 21), (22, 20), (23, 20), (22, 20), (23, 20), (24, 20), (23, 20), (24, 20), (24, 21), (25, 21), (26, 21), (27, 21), (28, 21), (28, 22), (27, 22), (28, 22), (29, 22), (30, 22), (30, 23), (30, 24), (31, 24), (31, 23), (32, 23), (32, 22), (33, 22), (34, 22), (35, 22), (35, 23), (36, 23), (37, 23), (37, 24), (38, 24), (38, 25), (37, 25), (36, 25), (36, 26), (37, 26), (38, 26), (38, 27), (38, 26), (38, 25), (39, 25), (38, 25), (39, 25), (39, 26), (40, 26), (41, 26), (42, 26), (43, 26), (43, 25), (43, 26), (44, 26), (44, 27), (44, 28), (43, 28), (44, 28), (45, 28), (46, 28), (47, 28), (46, 28), (46, 29), (46, 28), (47, 28), (48, 28), (49, 28), (49, 29), (49, 30), (49, 31), (49, 30), (50, 30), (50, 31), (51, 31), (51, 32), (52, 32), (52, 31), (51, 31), (50, 31), (51, 31), (51, 32), (50, 32), (51, 32), (52, 32), (53, 32), (53, 31), (53, 32), (52, 32), (52, 33), (52, 34), (52, 35), (53, 35), (52, 35), (52, 36), (51, 36), (52, 36), (53, 36), (54, 36), (54, 37), (54, 38), (55, 38), (55, 39), (56, 39), (57, 39), (58, 39), (57, 39), (56, 39), (56, 40), (56, 41), (57, 41), (58, 41), (59, 41), (59, 42), (60, 42), (60, 43), (60, 44), (59, 44), (60, 44), (61, 44), (61, 45), (61, 46), (61, 47), (62, 47), (62, 48), (63, 48), (64, 48), (65, 48), (66, 48), (67, 48), (67, 49), (66, 49), (67, 49), (67, 50), (68, 50), (68, 51), (69, 51), (68, 51), (67, 51), (66, 51), (66, 52), (66, 53), (67, 53), (67, 54), (67, 55), (67, 54), (68, 54), (69, 54), (70, 54), (71, 54), (71, 55), (71, 54), (71, 55), (70, 55), (71, 55), (72, 55), (71, 55), (72, 55), (73, 55), (74, 55), (74, 54), (74, 55), (75, 55), (75, 54), (76, 54), (76, 55), (77, 55), (77, 56), (77, 55), (76, 55), (77, 55), (77, 56), (77, 57), (77, 56), (78, 56), (78, 57), (78, 58), (77, 58), (78, 58), (78, 59), (79, 59), (79, 60), (80, 60), (79, 60), (79, 59), (79, 60), (80, 60), (81, 60), (82, 60), (82, 61), (83, 61), (83, 62), (84, 62), (84, 63), (84, 64)]
    movement_i = 0
    while running:
        screen.fill(theme.colors['background'])
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    paused = not paused

        if movement_i > 0:
            key_input = pygame.key.get_pressed()
            pygame.event.wait()
        ca.attribute_next_generation()
        explorer = explorer_path[movement_i + 1]
        movement_i += 1

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()

            if restart_button.is_hovering(x, y):
                ca.restart()

        screen.fill(theme.colors['background'])

        for x in range(ca.column_count):
            for y in range(ca.row_count):
                cell = ca.matrix[x, y]

                if cell == 1:
                    pygame.draw.rect(screen, theme.colors['green'],
                                     (x * cell_size, y * cell_size, cell_size, cell_size))

                elif cell == 3 or cell == 4:
                    pygame.draw.rect(screen, theme.colors['yellow'],
                                     (x * cell_size, y * cell_size, cell_size, cell_size))

                else:
                    pygame.draw.rect(screen, theme.colors['shade'],
                                     (x * cell_size, y * cell_size, cell_size, cell_size), 1)

        pygame.draw.circle(screen, theme.colors['red'], (explorer[0] * cell_size + cell_size // 2,
                                                            explorer[1] * cell_size + cell_size // 2), cell_size // 2.25)

        x, y = pygame.mouse.get_pos()

        if restart_button.is_hovering(x, y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            restart_button.draw_hovering()

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            restart_button.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    view()
