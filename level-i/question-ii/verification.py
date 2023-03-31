import pygame
import darkdetect
import tkinter as tk
import os
from time import sleep

from utilities.pygame import theme
from utilities.pygame import button

import celullar_automata


def verify():
    matrix = input('Enter the matrix file name: ')
    explorer_path = input('Enter explorer path: ').replace(
        '\n', '').lower().split(' ')

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.set_caption('Stone Automata Maze Challenge')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(
        dir_path, 'assets', 'images', f'samc-icon-{str(darkdetect.theme()).lower()}.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # TODO: add select file button as initial screen
    matrix_path = os.path.join(dir_path, 'data', 'input', f'{matrix}.txt')

    ca = celullar_automata.CellularAutomata(matrix_path)

    """
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    """

    screen_width = 1920
    screen_height = 1080

    cell_size = screen_height // ca.row_count

    paused = running = True

    font_path = os.path.join(dir_path, 'assets', 'fonts', 'emulogic.ttf')
    font = pygame.font.Font(font_path, 24)

    restart_button_x = screen_width - \
        (screen_width - cell_size * ca.column_count) // 2 - 120
    restart_button_y = 60

    restart_button = button.Button(
        screen, font, theme.colors['green'], theme.colors['background'], restart_button_x, restart_button_y, 240, 60, 'restart')

    origin = None

    for x in range(ca.column_count):
        for y in range(ca.row_count):
            if ca.matrix[x, y] == 3:
                origin = (x, y)

    path = []
    explorer = origin
    path.append(explorer)
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

        pygame.key.get_pressed()
        pygame.event.wait()
        ca.attribute_next_generation()
        if explorer_path[movement_i] == 'u':
            explorer = (explorer[0], explorer[1] - 1)
        elif explorer_path[movement_i] == 'd':
            explorer = (explorer[0], explorer[1] + 1)
        elif explorer_path[movement_i] == 'l':
            explorer = (explorer[0] - 1, explorer[1])
        elif explorer_path[movement_i] == 'r':
            explorer = (explorer[0] + 1, explorer[1])
        path.append(explorer)
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

        for i in range(len(path) - 1):
            origin_x_pixel = path[i][0] * cell_size + cell_size // 2
            origin_y_pixel = path[i][1] * cell_size + cell_size // 2
            destination_x_pixel = path[i + 1][0] * cell_size + cell_size // 2
            destination_y_pixel = path[i + 1][1] * cell_size + cell_size // 2

            pygame.draw.line(screen, theme.colors['red'], (origin_x_pixel, origin_y_pixel),
                             (destination_x_pixel, destination_y_pixel), 2)

            # Draw the line between the two points
            pygame.draw.line(screen, theme.colors['red'], (origin_x_pixel, origin_y_pixel),
                             (destination_x_pixel, destination_y_pixel), 2)

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
    verify()
