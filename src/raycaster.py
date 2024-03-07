import pygame, sys
from pygame.locals import *

import objects, game, math

def Vector_Length(start_pos: tuple, end_pos: tuple) -> float:
    return math.sqrt((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)

def Sort_Walls():
    objects.Wall.Sorted_Walls = []

    for wall in objects.Wall.Walls:
        wall_distance_1 = int(Vector_Length((objects.Player.x, objects.Player.y), (wall.start_pos)))
        wall_distance_2 = int(Vector_Length((objects.Player.x, objects.Player.y), (wall.end_pos)))

        if wall_distance_1 > wall_distance_2: wall_distance = wall_distance_1
        else: wall_distance = wall_distance_2
        
        while wall_distance in objects.Wall.Sorted_Walls: wall_distance += 1

        objects.Wall.Sorted_Walls.append((wall_distance, wall))

    def sortkey(wall):
        return wall[0]

    objects.Wall.Sorted_Walls = sorted(objects.Wall.Sorted_Walls, key=sortkey)

def Cast(angle: int, start_x: int, start_y: int):
    # Set the positions
    x_3 = start_x
    y_3 = start_y
    x_4 = -math.sin(game.Angles_To_Radians(angle)) * 100000
    y_4 = -math.cos(game.Angles_To_Radians(angle)) * 100000

    end_x = x_3 + x_4
    end_y = y_3 + y_4

    c_ray_end_x = end_x
    c_ray_end_y = end_y
    c_ray_color = (255, 255, 255)
    c_ray_height = 1
    tracker = 0

    c_ray_len = 1000000

    for wall in objects.Wall.Sorted_Walls:
        wall = wall[1]
        x_1, y_1 = wall.start_pos
        x_2, y_2 = wall.end_pos

        # Calculate the position where the ray and the wall collides
        denominator = ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))

        t_numerator = ((x_1-x_3)*(y_3-y_4)-(y_1-y_3)*(x_3-x_4))

        t = t_numerator / denominator

        u_numerator = ((x_1-x_3)*(y_1-y_2)-(y_1-y_3)*(x_1-x_2))

        u = u_numerator / denominator

        # Checks if the lines touch or no
        if t > 0 and t < 1 and u > 0:
            end_x = (x_3 + u * (x_4 - x_3))
            end_y = (y_3 + u * (y_4 - y_3))
            color = wall.color
            height = wall.height

            if Vector_Length((x_3, y_3), (end_x, end_y)) < c_ray_len:
                c_ray_len = Vector_Length((x_3, y_3), (end_x, end_y))
                c_ray_end_x = end_x
                c_ray_end_y = end_y
                c_ray_color = color
                c_ray_height = height

            tracker += 1
            if tracker > 5:
                break

    if c_ray_len != 1000000:
        objects.Ray((x_3, y_3), (c_ray_end_x, c_ray_end_y), angle, c_ray_color, c_ray_height)
    else:
        objects.Ray.Rays.append(None) # If it doesn't collide with a wall, add None

def Draw_Pseudo_3D():
    rays = objects.Ray.Rays

    width = game.Game.width / (objects.Player.FOV * objects.Player.INTENSITY)

    for idx, ray in enumerate(rays):
        if ray is None:
            continue

        if ray.len > 2000:
            continue

        w = width+1
        h = 100*game.Game.height / ray.len

        a = ray.dir - objects.Player.rotation
        h /= math.cos(game.Angles_To_Radians(a))

        if h > game.Game.height: h = game.Game.height

        x = ((objects.Player.FOV * objects.Player.INTENSITY)-1-idx) * width
        if game.Game.draw_2d:
            x += game.Game.width
        
        y = 300 - h / 2

        color = ray.color

        color_r = int(color[0] / game.Game.width * abs(h))
        color_g = int(color[1] / game.Game.width * abs(h))
        color_b = int(color[2] / game.Game.width * abs(h))

        if color_r > 255: color_r = 255
        if color_g > 255: color_g = 255
        if color_b > 255: color_b = 255
        
        # Draws the 3D part
        pygame.draw.rect(
            game.screen,
            (color_r, color_g, color_b),
            (x, y, w, h)
        )