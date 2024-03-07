import pygame, game
from pygame.locals import *

import gui, objects
import scene_settings, scene_game

def Init():
    Start()

    # Create the UI elements
    gui.Text("menu_title_text", "menu", 400, 150, 72, "PUZZLE THINGY", (255, 255, 255), "center")

    gui.Text("menu_version_text", "menu", 5, 583, 24, "Version 0.5", (255, 255, 255), "left")
    gui.Text("menu_credit_text", "menu", 795, 583, 24, "Made By Veeti Tuomola", (255, 255, 255), "right")

    gui.Button("menu_play_button", "menu", 400, 270, 300, 80, "PLAY", 42, (255, 255, 255), "center")
    gui.Button("menu_settings_button", "menu", 400, 360, 300, 80, "SETTINGS", 42, (255, 255, 255), "center")
    gui.Button("menu_exit_button", "menu", 400, 450, 300, 80, "EXIT", 42, (255, 255, 255), "center")

    objects.Player.Load_Settings()

def Start():
    pygame.mouse.set_visible(True)

def Input(event):
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:

            # Buttons
            if gui.Button.Buttons["menu_play_button"].button_object.collidepoint(game.mouse_pos):
                game.Game.scene = "game"
                scene_game.Start()
            elif gui.Button.Buttons["menu_settings_button"].button_object.collidepoint(game.mouse_pos):
                game.Game.scene = "settings"
                scene_settings.Start()
            elif gui.Button.Buttons["menu_exit_button"].button_object.collidepoint(game.mouse_pos):
                game.Stop()


def Update():
    game.screen.fill(game.Game.bg_color)