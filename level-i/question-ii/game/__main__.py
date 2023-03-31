import pygame
import darkdetect
import tkinter as tk
import sys
import os
from time import sleep

parent_path = os.path.abspath('.')
sys.path.insert(1, parent_path)

import theme
import button
import celullar_automata


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

    explorer_path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (16, 8), (16, 9), (16, 8), (17, 8), (18, 8), (17, 8), (18, 8), (18, 9), (19, 9), (20, 9), (20, 10), (21, 10), (22, 10), (23, 10), (24, 10), (25, 10), (26, 10), (25, 10), (26, 10), (26, 11), (27, 11), (28, 11), (27, 11), (27, 12), (27, 11), (28, 11), (28, 12), (28, 13), (29, 13), (29, 14), (30, 14), (30, 15), (31, 15), (31, 16), (31, 17), (30, 17), (31, 17), (32, 17), (33, 17), (34, 17), (35, 17), (36, 17), (36, 16), (37, 16), (38, 16), (39, 16), (39, 17), (40, 17), (39, 17), (39, 18), (40, 18), (39, 18), (39, 19), (40, 19), (41, 19), (41, 18), (42, 18), (43, 18), (43, 19), (44, 19), (44, 20), (44, 21), (44, 22), (43, 22), (44, 22), (45, 22), (46, 22), (46, 23), (47, 23), (47, 22), (48, 22), (49, 22), (49, 21), (50, 21), (50, 22), (49, 22), (50, 22), (49, 22), (50, 22), (50, 21), (51, 21), (50, 21), (50, 22), (50, 23), (51, 23), (52, 23), (52, 22), (51, 22), (51, 23), (52, 23), (53, 23), (53, 24), (53, 25), (54, 25), (55, 25), (55, 26), (55, 27), (54, 27), (54, 28), (55, 28), (55, 29), (55, 28), (55, 29), (55, 30), (55, 31), (56, 31), (57, 31), (57, 32), (57, 33), (57, 34), (57, 35), (57, 36), (57, 37), (58, 37), (58, 38), (59, 38), (60, 38), (60, 39), (60, 40), (59, 40), (60, 40), (61, 40), (62, 40), (63, 40), (62, 40), (63, 40), (63, 41), (63, 42), (63, 43), (63, 44), (63, 45), (63, 46), (63, 47), (63, 48), (63, 49), (64, 49), (64, 50), (64, 49), (65, 49), (65, 50), (66, 50), (66, 51), (66, 52), (66, 53), (67, 53), (68, 53), (68, 54), (69, 54), (70, 54), (70, 55), (71, 55), (72, 55), (73, 55), (73, 54), (72, 54), (72, 55), (72, 56), (72, 57), (73, 57), (74, 57), (74, 58), (75, 58), (74, 58), (74, 57), (74, 56), (75, 56), (76, 56), (77, 56), (77, 55), (76, 55), (77, 55), (78, 55), (79, 55), (79, 56), (79, 57), (80, 57), (81, 57), (82, 57), (81, 57), (81, 58), (82, 58), (82, 59), (83, 59), (83, 60), (83, 59), (83, 60), (82, 60), (82, 59), (82, 58), (81, 58), (81, 59), (81, 58), (81, 59), (81, 60), (80, 60), (80, 59), (80, 58), (81, 58), (82, 58), (81, 58), (81, 57), (82, 57), (82, 56), (83, 56), (83, 57), (83, 58), (82, 58), (82, 59), (82, 60), (82, 61), (83, 61), (84, 61), (84, 60), (84, 61), (84, 62), (84, 63), (84, 64)]
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

        if ca.matrix[explorer[0], explorer[1]] == 1:
            screen.fill(theme.colors['red'])
        else:
            screen.fill(theme.colors['background'])

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()

            if restart_button.is_hovering(x, y):
                ca.restart()

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
