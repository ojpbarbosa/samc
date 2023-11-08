import pygame
import darkdetect
import tkinter as tk
import os
from time import sleep

from utilities.pygame import theme
from utilities.pygame import button
import pathfinder
import celullar_automata


def view():
    # TODO: add select file button as initial screen
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # matrix_path = os.path.join(dir_path, 'data', 'input', 'matrix-i.txt')
    matrix_path = './data/input/matrix-v.txt'

    ca = celullar_automata.CellularAutomata(matrix_path)

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.set_caption('Stone Automata Maze Challenge')

    icon_path = os.path.join(
        dir_path, 'assets', 'images', f'samc-icon-{str(darkdetect.theme()).lower()}.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    generation_interval = 0.5

    origin = destination = None

    for x in range(ca.column_count):
        for y in range(ca.row_count):
            if ca.matrix[x, y] == 3:
                origin = (x, y)

            elif ca.matrix[x, y] == 4:
                destination = (x, y)

    pf = pathfinder.Pathfinder(origin, destination)

    # root = tk.Tk()

    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()

    screen_width, screen_height = pygame.display.get_window_size()

    cell_size = screen_height // ca.row_count

    running = True
    paused = False

    font_path = os.path.join(dir_path, 'assets', 'fonts', 'emulogic.ttf')
    font = pygame.font.Font(font_path, 24)

    restart_button_x = screen_width - \
        (screen_width - cell_size * ca.column_count) // 2 - 120
    restart_button_y = 60

    restart_button = button.Button(
        screen, font, theme.colors['green'], theme.colors['background'], restart_button_x, restart_button_y, 240, 60, '')

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

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()

            if restart_button.is_hovering(x, y):
                ca.restart()
                paused = True

        # if not paused:
        #     if len(pf.path) > 0:
        #         print(pf.path)
        #         print(pf.path_to_string())
        #         print(len(pf.path_to_string().split(' ')))
        #         paused = True
        #     else:
        ca.attribute_next_generation()
        #         pf.move(ca.matrix.copy())
        sleep(generation_interval)

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

        for explorer in pf.explorers:
            # pygame.draw.circle(screen, theme.colors['red'], (explorer[-1][0] * cell_size + cell_size // 2,
            #                                                  explorer[-1][1] * cell_size + cell_size // 2), cell_size // 2.25)

            for i in range(len(explorer)-1):
                # Get the starting and ending coordinates for the line
                origin_x, origin_y = explorer[i]
                destination_x, destination_y = explorer[i + 1]

                # Calculate the pixel coordinates for the starting and ending points
                origin_x_pixel = origin_x * cell_size + cell_size // 2 - 1
                origin_y_pixel = origin_y * cell_size + cell_size // 2 - 1
                destination_x_pixel = destination_x * cell_size + cell_size // 2 - 1
                destination_y_pixel = destination_y * cell_size + cell_size // 2 - 1

                # Draw the line between the two points
                # pygame.draw.line(screen, theme.colors['red'], (origin_x_pixel, origin_y_pixel),
                #                  (destination_x_pixel, destination_y_pixel), 2)

        x, y = pygame.mouse.get_pos()

        restart_button.text = str(ca.generation) + ' gen'
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
