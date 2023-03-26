import pygame
import tkinter as tk

from theme import colors
from celullar_automata import CellularAutomata
from button import Button
from utilities import human_format


def maze():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.set_caption('Stone Automata Maze Challenge phase 1')

    cellular_automata = CellularAutomata(screen)

    root = tk.Tk()

    button_x = root.winfo_screenwidth() // 2 - 120
    button_y = root.winfo_screenheight() - 82.5

    restart_button = Button(
        screen, colors['secondary'], colors['primary'], button_x, button_y, 240, 60, 'restart')

    running = True

    font = pygame.font.Font('./fonts/emulogic.ttf', 24)

    while running:
        screen.fill(colors['primary'])
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    cellular_automata.paused = not cellular_automata.paused

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()

            cellular_automata.handle_click(x, y)

            if restart_button.is_hovering(x, y):
                cellular_automata.restart()

        cellular_automata.compute_next_generation()

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
    maze()
