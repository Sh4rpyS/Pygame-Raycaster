import pygame, math
from pygame.locals import *

import game, raycaster

class Wall:
    Sorted_Walls = []
    Walls = []
    Selected = None

    Start_Point = ()
    End_Point = ()

    def __init__(self, start_pos: tuple, end_pos: tuple, color: tuple, height: float):
        # Positions will be saved in tuples
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.center_pos = ((self.start_pos[0] + self.end_pos[0]) / 2, (self.start_pos[1] + self.end_pos[1]) / 2)
        self.color = color

        self.height = height
        self.len = self.length()

        # Adds itself to the list
        Wall.Walls.append(self)

    # Return the length of the wall
    def length(self) -> float:
        return math.sqrt((self.end_pos[0]-self.start_pos[0])**2 + (self.end_pos[1]-self.start_pos[1])**2)

    def draw(self):
        # Draws the highlight
        if Wall.Selected == self:
            pygame.draw.line(
                game.screen,
                (0, 0, 255),
                self.start_pos,
                self.end_pos,
                width = 3
            )

        # Draws the line from starting point to the end point
        pygame.draw.line(
            game.screen,
            self.color,
            self.start_pos,
            self.end_pos,
            width = 1
        )

    # Draws all the colliders
    def Draw_Colliders():
        for wall in Wall.Walls:
            # Draws the collilder
            wall.drawn = pygame.draw.line(
                game.screen,
                (0, 0, 0),
                wall.start_pos,
                wall.end_pos,
                width = 9
            )

    # Draws all the walls using their own function
    def Draw_All():
        for wall in Wall.Walls:
            wall.draw()

# Pretty much just a wall lol
class Ray:
    Rays = []

    def __init__(self, start_pos: tuple, end_pos: tuple, direction: float, color: tuple, height: float):
        # Positions will be saved in tuples
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.dir = direction
        self.color = color

        self.height = height
        self.len = self.length()

        # Adds itself to the list
        Ray.Rays.append(self)

    # Returns the length of the Ray
    def length(self) -> float:
        return math.sqrt((self.end_pos[0]-self.start_pos[0])**2 + (self.end_pos[1]-self.start_pos[1])**2)

    # Clears the Ray list
    def Clear():
        Ray.Rays.clear()

    def draw(self):

        # Draws the line from starting point to the end point
        pygame.draw.line(
            game.screen,
            self.color,
            self.start_pos,
            self.end_pos,
            width = 1
        )

    # Draws all the rays using their own function
    def Draw_All():
        for ray in Ray.Rays:
            if ray != None:
                ray.draw()

class Player:
    # Camera settings
    FOV = 60
    INTENSITY = 1
    MOUSE_LOOK = None
    SENSITIVITY = 0.14

    # Initialize some variables
    x: int
    y: int
    rotation: int

    collider: pygame.Surface

    # Loads game settings when the game is launched
    def Load_Settings():
        with open("pref/settings.dat", "r") as settings:
            settings_data = settings.readlines()

        settings = [setting.strip() for setting in settings_data]
        Player.MOUSE_LOOK = bool(int(settings[0].split("=")[1]))
        Player.INTENSITY = int(settings[1].split("=")[1])
        Player.FOV = int(settings[2].split("=")[1])
        Player.SENSITIVITY = float(settings[3].split("=")[1])

    # Save the game settings
    def Save_Settings():
        with open("pref/settings.dat", "w") as settings:
            settings.write(f"mouse={int(Player.MOUSE_LOOK)}\n")
            settings.write(f"resolution={Player.INTENSITY}\n")
            settings.write(f"fov={Player.FOV}\n")
            settings.write(f"sensitivity={Player.SENSITIVITY}")

    # Runs once when the game is opened
    def Init():
        Player.Load_Settings()

    # Runs everytime the scene is loaded
    def Start():
        Player.x = 100
        Player.y = 100
        Player.rotation = 270

        Player.collider = pygame.Surface((8, 8))
        Player.collider.set_alpha(0)
        raycaster.Sort_Walls()

    # Draws the player object
    def Draw():
        pygame.draw.circle(
            game.screen,
            (255, 0, 0),
            (Player.x, Player.y),
            4 # Radius
        )

    # Checks if player intersects on the next move
    def Check_For_Collision(mov_x: float, mov_y: float):
        collider = game.screen.blit(Player.collider, (Player.x - 4 + mov_x, Player.y - 4 + mov_y))

        for wall in Wall.Walls:
            if collider.colliderect(wall.drawn):
                return True

        return False

    def Calculate_Dir_Movement(angle) -> tuple:
        mov_x = math.sin(game.Angles_To_Radians(angle)) * 300 * game.delta_time
        mov_y = math.cos(game.Angles_To_Radians(angle)) * 300 * game.delta_time

        return (mov_x, mov_y)

    # Runs every frame while in correct scene
    def Update():

        # Allow the player to move forwards
        if game.key_input[pygame.K_w]:
            mov_x, mov_y = Player.Calculate_Dir_Movement(Player.rotation)

            if not Player.Check_For_Collision(-mov_x, -mov_y):
                Player.x -= mov_x
                Player.y -= mov_y
                raycaster.Sort_Walls()

        # Allow the player to move backwards
        elif game.key_input[pygame.K_s]:
            mov_x, mov_y = Player.Calculate_Dir_Movement(Player.rotation)

            if not Player.Check_For_Collision(mov_x, mov_y):
                Player.x += mov_x
                Player.y += mov_y
                raycaster.Sort_Walls()

        # If mouse looking is enabled, use the mouse to rotate the player camera
        if Player.MOUSE_LOOK:
            Player.rotation -= game.mouse_rel[0] * Player.SENSITIVITY
            # Lock the mouse to the middle, if it goes too far

            if not pygame.mouse.get_visible():
                if game.mouse_pos[0] < 100 or game.mouse_pos[0] > 700 or game.mouse_pos[1] < 100 or game.mouse_pos[1] > 500:
                    pygame.mouse.set_pos((400, 300))

            # Allow side movement
            # Moving right
            if game.key_input[pygame.K_d]:
                mov_x, mov_y = Player.Calculate_Dir_Movement(Player.rotation + 90)
                if not Player.Check_For_Collision(mov_x, mov_y):
                    Player.x += mov_x
                    Player.y += mov_y
                    raycaster.Sort_Walls()

            # Moving left
            elif game.key_input[pygame.K_a]:
                mov_x, mov_y = Player.Calculate_Dir_Movement(Player.rotation - 90)
                if not Player.Check_For_Collision(mov_x, mov_y):
                    Player.x += mov_x
                    Player.y += mov_y
                    raycaster.Sort_Walls()
        else:
            # Else use the set binds
            if game.key_input[pygame.K_d]: Player.rotation -= 150 * game.delta_time
            elif game.key_input[pygame.K_a]: Player.rotation += 150 * game.delta_time