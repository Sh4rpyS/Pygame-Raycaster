import pygame, game, gui
from pygame.locals import *

import objects, scene_menu

def Init():
    gui.Text("settings_text", "settings", 400, 100, 62, "SETTINGS", (255, 255, 255), "center")
    gui.Text("mouse_title_text", "settings", 350, 200, 42, "Mouse: ", (255, 255, 255), "right")
    gui.Text("sens_title_text", "settings", 350, 275, 42, "Sensitivity: ", (255, 255, 255), "right")
    gui.Text("fov_title_text", "settings", 350, 350, 42, "Field Of View: ", (255, 255, 255), "right")
    gui.Text("res_title_text", "settings", 350, 425, 42, "Resolution: ", (255, 255, 255), "right")

    gui.Button("settings_back_button", "settings", 5, 30, 100, 50, "Back", 32, (255, 255, 255), "left")

    gui.Button("settings_mouse_disable_button", "settings", 350, 200, 35, 35, "<", 24, (255, 255, 255), "left")
    gui.Button("settings_mouse_enable_button", "settings", 650, 200, 35, 35, ">", 24, (255, 255, 255), "right")
    gui.Text("mouse_status_text", "settings", 500, 200, 32, "ENABLED", (255, 255, 255), "center")

    gui.Button("settings_sens_dec_button", "settings", 350, 275, 35, 35, "<", 24, (255, 255, 255), "left")
    gui.Button("settings_sens_inc_button", "settings", 650, 275, 35, 35, ">", 24, (255, 255, 255), "right")
    gui.Text("sens_status_text", "settings", 500, 275, 32, "0.14", (255, 255, 255), "center")

    gui.Button("settings_fov_dec_button", "settings", 350, 350, 35, 35, "<", 24, (255, 255, 255), "left")
    gui.Button("settings_fov_inc_button", "settings", 650, 350, 35, 35, ">", 24, (255, 255, 255), "right")
    gui.Text("fov_status_text", "settings", 500, 350, 32, "60", (255, 255, 255), "center")

    gui.Button("settings_res_dec_button", "settings", 350, 425, 35, 35, "<", 24, (255, 255, 255), "left")
    gui.Button("settings_res_inc_button", "settings", 650, 425, 35, 35, ">", 24, (255, 255, 255), "right")
    gui.Text("res_status_text", "settings", 500, 425, 32, "1", (255, 255, 255), "center")

    Start()
    objects.Player.Load_Settings()

def Start():
    pygame.mouse.set_visible(True)

    Update_Settings_Text()

def Update_Settings_Text():
    if objects.Player.MOUSE_LOOK: gui.Text.Texts["mouse_status_text"].update_text("ENABLED")
    else: gui.Text.Texts["mouse_status_text"].update_text("DISABLED")

    gui.Text.Texts["sens_status_text"].update_text(f"{objects.Player.SENSITIVITY}")
    gui.Text.Texts["fov_status_text"].update_text(f"{objects.Player.FOV}")
    gui.Text.Texts["res_status_text"].update_text(f"{objects.Player.INTENSITY}")

def Input(event):
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            # Settings buttons
            if gui.Button.Buttons["settings_res_dec_button"].button_object.collidepoint(game.mouse_pos) and objects.Player.INTENSITY > 1:
                objects.Player.INTENSITY -= 1
            elif gui.Button.Buttons["settings_res_inc_button"].button_object.collidepoint(game.mouse_pos) and objects.Player.INTENSITY < 10:
                objects.Player.INTENSITY += 1
            elif gui.Button.Buttons["settings_fov_dec_button"].button_object.collidepoint(game.mouse_pos) and objects.Player.FOV > 30:
                objects.Player.FOV -= 5
            elif gui.Button.Buttons["settings_fov_inc_button"].button_object.collidepoint(game.mouse_pos) and objects.Player.FOV < 360:
                objects.Player.FOV += 5
            elif gui.Button.Buttons["settings_sens_dec_button"].button_object.collidepoint(game.mouse_pos) and objects.Player.SENSITIVITY > 0.01:
                objects.Player.SENSITIVITY -= 0.01
                objects.Player.SENSITIVITY = float(f"{objects.Player.SENSITIVITY:.2f}")
            elif gui.Button.Buttons["settings_sens_inc_button"].button_object.collidepoint(game.mouse_pos) and objects.Player.SENSITIVITY < 1:
                objects.Player.SENSITIVITY += 0.01
                objects.Player.SENSITIVITY = float(f"{objects.Player.SENSITIVITY:.2f}")
            elif gui.Button.Buttons["settings_mouse_disable_button"].button_object.collidepoint(game.mouse_pos):
                objects.Player.MOUSE_LOOK = False
            elif gui.Button.Buttons["settings_mouse_enable_button"].button_object.collidepoint(game.mouse_pos):
                objects.Player.MOUSE_LOOK = True

            # Back button
            elif gui.Button.Buttons["settings_back_button"].button_object.collidepoint(game.mouse_pos):
                game.Game.scene = "menu"
                scene_menu.Start()

            # Update the settings status
            Update_Settings_Text()
            objects.Player.Save_Settings()

def Update():
    game.screen.fill(game.Game.bg_color)