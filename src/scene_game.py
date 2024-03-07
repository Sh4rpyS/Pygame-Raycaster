import pygame, game
from pygame.locals import *
import raycaster, objects

def Init():
    Start()

def Start():

    objects.Wall.Walls.clear()

    objects.Wall((1, 1), (799, 1), (0, 255 ,0), 1.5)
    objects.Wall((1, 1), (1, 599), (0, 255 ,0), 1.5)
    objects.Wall((2000, 1), (2000, 599), (255, 0 ,0), 1.5)
    objects.Wall((1, 599), (799, 599), (255, 0 ,0), 1.5)

    objects.Wall((151, 118), (396, 118), (255, 255, 255), 1)
    objects.Wall((151, 118), (151, 354), (255, 255, 255), 1)
    objects.Wall((151, 354), (554, 354), (0, 0, 255), 1)
    objects.Wall((554, 354), (554, 256), (0, 0, 255), 1)
    objects.Wall((554, 256), (269, 256), (0, 0, 255), 1)
    objects.Wall((269, 256), (269, 189), (255, 255, 255), 1)
    objects.Wall((269, 189), (555, 189), (255, 255, 255), 1)

    objects.Player.Start()
    objects.Player.Load_Settings()

    if objects.Player.MOUSE_LOOK:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

def Input(event):
    if event.type == MOUSEBUTTONDOWN and game.Game.draw_2d:

        # Select walls and deselect walls
        if event.button == 1:
            for wall in objects.Wall.Walls:
                if wall.drawn.collidepoint(game.mouse_pos):

                    # If a wall is selected, earlier points are removed
                    objects.Wall.Start_Point = ()
                    objects.Wall.End_Point = ()

                    # Toggle wall selections
                    if objects.Wall.Selected == wall:
                        objects.Wall.Selected = None
                    else:
                        objects.Wall.Selected = wall

        # Place wall points
        elif event.button == 3:
            if objects.Wall.Start_Point == ():
                # Check if a wall is selected, and if it is, snap it to the closer corner

                if objects.Wall.Selected != None:
                    # Get the distances of the points related to the mouse pos
                    start_len = raycaster.Vector_Length(objects.Wall.Selected.start_pos, game.mouse_pos)
                    end_len = raycaster.Vector_Length(objects.Wall.Selected.end_pos, game.mouse_pos)
                    
                    # Check which one is closer
                    if start_len <= end_len:        # Start point is closer
                        objects.Wall.Start_Point = objects.Wall.Selected.start_pos
                    else:                           # End point is closer
                        objects.Wall.Start_Point = objects.Wall.Selected.end_pos
                
                else:
                    # Get the mouse position and set it as the starting position
                    objects.Wall.Start_Point = (game.mouse_pos[0], game.mouse_pos[1])
            else:
                # Get the longer axis difference, and set it as end point
                x_diff = game.mouse_pos[0] - objects.Wall.Start_Point[0]
                y_diff = game.mouse_pos[1] - objects.Wall.Start_Point[1]

                if abs(x_diff) >= abs(y_diff):
                    objects.Wall.End_Point = (game.mouse_pos[0], objects.Wall.Start_Point[1])
                else:
                    objects.Wall.End_Point = (objects.Wall.Start_Point[0], game.mouse_pos[1])
                
                if objects.Wall.Start_Point != objects.Wall.End_Point:
                    objects.Wall(objects.Wall.Start_Point, objects.Wall.End_Point, (255, 255, 255), 1)
                    objects.Wall.Start_Point = ()
                    objects.Wall.End_Point = ()
                    objects.Wall.Selected = objects.Wall.Walls[-1]
                else:
                    objects.Wall.End_Point = ()


    if event.type == KEYDOWN:

        # Removes an already selected wall
        if event.key == K_r:
            if objects.Wall.Selected != None:
                objects.Wall.Walls.remove(objects.Wall.Selected)
                objects.Wall.Selected = None

        # Deselects everything, and removes already selected points
        elif event.key == K_c:
            objects.Wall.Selected = None
            objects.Wall.Start_Point = ()
            objects.Wall.End_Point = ()

        # Allow mouse control
        elif event.key == K_ESCAPE:
            if objects.Player.MOUSE_LOOK:
                objects.Player.MOUSE_LOOK = False
                pygame.mouse.set_visible(True)
            else:
                objects.Player.MOUSE_LOOK = True
                pygame.mouse.set_visible(False)


def Update():
    objects.Player.Update()
    objects.Ray.Clear()

    for i in range(objects.Player.INTENSITY * objects.Player.FOV):

        rotation = (objects.Player.rotation - objects.Player.FOV / 2) + i * (objects.Player.FOV / (objects.Player.FOV * objects.Player.INTENSITY))
        raycaster.Cast(rotation, objects.Player.x, objects.Player.y)
    
    # Draw the wall colliders
    # This is required for the player movement to work
    objects.Wall.Draw_Colliders()

    game.screen.fill(game.Game.bg_color)
    pygame.draw.rect(game.screen, (30, 30, 30), (0, 300, 800, 300))

    # 2D Draw
    if game.Game.draw_2d:
        objects.Wall.Draw_All()
        objects.Ray.Draw_All()
        objects.Player.Draw()

    # Pseudo 3D Draw
    raycaster.Draw_Pseudo_3D()