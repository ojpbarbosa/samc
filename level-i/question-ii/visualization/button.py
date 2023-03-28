# inspired by https://www.youtube.com/watch?v=4_9twnEduFA
import pygame


class Button:
    def __init__(self, screen, font, background_color, text_color, x, y, width, height, text):
        self.screen = screen
        self.font = font

        self.background_color = background_color
        self.text_color = text_color

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.text = text


        self.hovering = False

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color,
                         (self.x, self.y, self.width, self.height))

        text = self.font.render(self.text, 1, self.text_color)

        self.screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                         self.y + (self.height / 2 - text.get_height() / 2)))

    def draw_hovering(self):
        pygame.draw.rect(self.screen, self.text_color,
                         (self.x, self.y, self.width, self.height))

        text = self.font.render(self.text, 1, self.background_color)

        self.screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                         self.y + (self.height / 2 - text.get_height() / 2)))

        pygame.draw.rect(self.screen, self.background_color,
                         (self.x, self.y, self.width, self.height), 2)

    def is_hovering(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                self.hovering = True
                return True

        self.hovering = False
        return False
