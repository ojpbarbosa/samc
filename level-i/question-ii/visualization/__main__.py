
import pygame
import tkinter as tk
import sys
import os
import darkdetect

parent_path = os.path.abspath('.')
sys.path.insert(1, parent_path)


import celullar_automata
import theme
import button


def view():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.set_caption('Stone Automata Maze Challenge')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(dir_path, 'images', f'samc-icon-{str(darkdetect.theme()).lower()}.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # TODO: add select file button as initial screen
    parent_path = os.path.abspath('../question-ii')
    matrix_path = os.path.join(parent_path, 'data', 'matrix.txt')
    ca = celullar_automata.CellularAutomata(matrix_path)

    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    cell_size = screen_height // ca.row_count

    paused = running = True

    font_path = os.path.join(dir_path, 'fonts', 'emulogic.ttf')
    font = pygame.font.Font(font_path, 24)

    restart_button_x = screen_width - (screen_width - cell_size * ca.column_count) // 2 - 120
    restart_button_y = 60

    restart_button = button.Button(
        screen, font, theme.colors['green'], theme.colors['background'], restart_button_x, restart_button_y, 240, 60, 'restart')

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

        if not paused:
            ca.compute_next_generation()

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
