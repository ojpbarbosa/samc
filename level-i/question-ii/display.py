import pygame
import tkinter as tk

from theme import colors
from celullar_automata import CellularAutomata
from button import Button


def display():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.set_caption('Stone Automata Maze Challenge phase 1')

    cellular_automata = CellularAutomata("matrix.txt")

    root = tk.Tk()

    screen_height = root.winfo_screenheight()

    cell_size = screen_height // cellular_automata.row_count

    button_x = root.winfo_screenwidth() // 2 - 120
    button_y = screen_height - 82.5

    restart_button = Button(
        screen, colors['green'], colors['background'], 1520, 60, 240, 60, 'restart')

    paused = running = True
    font = pygame.font.Font('./fonts/emulogic.ttf', 24)

    while running:
        screen.fill(colors['background'])
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
                cellular_automata.restart()

        if not paused:
            cellular_automata.compute_next_generation()

        screen.fill(colors['background'])

        for x in range(cellular_automata.column_count):
            for y in range(cellular_automata.row_count):
                cell = cellular_automata.matrix[x, y]

                if cell == 1:
                    pygame.draw.rect(screen, colors['green'],
                                     (x * cell_size, y * cell_size, cell_size, cell_size))

                elif cell == 3 or cell == 4:
                    pygame.draw.rect(screen, colors['yellow'],
                                     (x * cell_size, y * cell_size, cell_size, cell_size))

                else:
                    pygame.draw.rect(screen, colors['shade'],
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
    display()
