import pygame, sys, math
from pygame.locals import *

pygame.init()

import scene_game, scene_menu, scene_settings
import gui, objects

class Game:
    draw_2d = False
    width = 800
    height = 600
    title = "Raycaster demo"
    fps = 0

    scene = "game"
    bg_color = (0, 0, 0)

def Init() -> None:
    if Game.draw_2d:
        Game.width = 1600

    global screen, clock
    screen = pygame.display.set_mode((Game.width, Game.height), 0, 32)
    pygame.display.set_caption(Game.title)
    clock = pygame.time.Clock()

    global get_ticks_last_frame
    get_ticks_last_frame = 0

def Start() -> None:
    scene_menu.Init()
    scene_settings.Init()
    scene_game.Init()
    objects.Player.Init()

    while 1: Update()

def Stop() -> None:
    pygame.quit()
    sys.exit()

def Count_Delta_Time() -> None:
    global delta_time, get_ticks_last_frame, ticks
    ticks = pygame.time.get_ticks()
    delta_time = (ticks - get_ticks_last_frame) / 1000
    get_ticks_last_frame = ticks

def Angles_To_Radians(angles: float):
    return angles * (math.pi / 180)

def Radians_To_Angles(radians: float):
    return radians * (180 / math.pi)

def Input() -> None:
    global mouse_pos, key_input, mouse_rel
    mouse_pos = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    key_input = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT: Stop()

        if event.type == KEYDOWN:
            if event.key == K_1:
                Game.scene = "menu"
                scene_menu.Start()
            elif event.key == K_2:
                Game.scene = "settings"
                scene_settings.Start()
            elif event.key == K_3:
                Game.scene = "game"
                scene_game.Start()

        if Game.scene == "game":
            scene_game.Input(event)
        elif Game.scene == "settings":
            scene_settings.Input(event)
        elif Game.scene == "menu":
            scene_menu.Input(event)

def Update() -> None:
    clock.tick(Game.fps)
    Count_Delta_Time()
    Input()

    if Game.scene == "game":
        scene_game.Update()
    elif Game.scene == "settings":
        scene_settings.Update()
    elif Game.scene == "menu":
        scene_menu.Update()

    gui.Button.Draw()
    gui.Text.Draw()

    pygame.display.update()
    pygame.display.set_caption(f"{Game.title} | {clock.get_fps():.1f} FPS")