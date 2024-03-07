import pygame, sys
from pygame.locals import *

import game

pygame.init()

class Text:
    Texts = {}
    Fonts = {}

    font_path = "fonts"
    font = "arial.ttf"

    def __init__(self, name: str, scene: str, x: float, y: float, size: int, text: str, color: tuple, alignment: str):
        self.name = name
        self.scene = scene

        self.size = size
        self.text = str(text)
        self.alignment = alignment
        self.color = color

        self.create_object()
        self.update_pos(x, y)

        self.active = True

        Text.Texts[self.name] = self

    def create_object(self):
        if not self.size in Text.Fonts:
            Text.Fonts[self.size] = pygame.font.Font(f"{Text.font_path}/{Text.font}", self.size)

        self.object = Text.Fonts[self.size].render(self.text, True, self.color)

    def count_alignment(self):
        self.width, self.height = Text.Fonts[self.size].size(self.text)

        if self.alignment == "left":
            self.draw_x = self.x
            self.draw_y = self.y - self.height / 2
        elif self.alignment == "center":
            self.draw_x = self.x - self.width / 2
            self.draw_y = self.y - self.height / 2
        elif self.alignment == "right":
            self.draw_x = self.x - self.width
            self.draw_y = self.y - self.height / 2

    def update_pos(self, x: float, y: float):
        self.x = x
        self.y = y
        self.count_alignment()

    def update_text(self, text: str):
        self.text = text
        self.create_object()
        self.count_alignment()

    def update_color(self, color: tuple):
        self.color = color
        self.create_object()

    def update_size(self, size: int):
        self.size = size
        self.create_object()
        self.count_alignment()

    def set_active(self, state: bool):
        self.active = state

    def draw(self):
        if game.Game.scene == self.scene and self.active:
            game.screen.blit(self.object, (self.draw_x, self.draw_y))

    def Draw():
        for text_object in Text.Texts.values():
            text_object.draw()

class Button:
    Buttons = {}

    def __init__(self, name: str, scene: str, x: float, y: float, width: float, height: float, text: str, font: int, color: tuple, alignment: str):
        self.name = name
        self.scene = scene

        self.width = width
        self.height = height
        self.alignment = alignment

        self.text = text
        self.text_size = font
        self.text_color = color

        self.text_object = Text(f"{self.name}_text", self.scene, 0, 0, self.text_size, self.text, self.text_color, "center")
        self.create_object()
        self.update_pos(x, y)

        self.active = True

        Button.Buttons[self.name] = self

    def create_object(self):
        self.object = pygame.Surface((self.width, self.height))
        self.object.fill((0, 0, 0))
        pygame.draw.rect(self.object, (255, 255, 255), (0, 0, self.width, self.height), width = 2)

        self.highlighted = pygame.Surface((self.width, self.height))
        self.highlighted.fill((0, 0, 0))
        pygame.draw.rect(self.highlighted, (255, 255, 255), (0, 0, self.width, self.height), width = 5)

        self.button_object = game.screen.blit(self.highlighted, (-100, -100))

    def update_pos(self, x: float, y: float):
        self.x = x
        self.y = y

        self.update_alignment()

    def update_alignment(self):
        if self.alignment == "left":
            self.draw_x = self.x
            self.draw_y = self.y - self.height / 2
        elif self.alignment == "center":
            self.draw_x = self.x - self.width / 2
            self.draw_y = self.y - self.height / 2
        elif self.alignment == "right":
            self.draw_x = self.x - self.width
            self.draw_y = self.y - self.height / 2

        self.text_object.update_pos(self.draw_x + self.width / 2, self.draw_y + self.height / 2)

    def set_active(self, state: bool):
        self.active = state

    def draw(self):
        if game.Game.scene == self.scene and self.active:
            if self.button_object.collidepoint((game.mouse_pos[0], game.mouse_pos[1])):
                self.button_object = game.screen.blit(self.highlighted, (self.draw_x, self.draw_y))
            else:
                self.button_object = game.screen.blit(self.object, (self.draw_x, self.draw_y))

    def Draw():
        for button_object in Button.Buttons.values():
            button_object.draw()