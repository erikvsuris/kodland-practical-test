import math
import random
import pgzero

# REMOVER
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

TITLE = "Rambo Rabbit"
WIDTH = 1280
HEIGHT = 720

ground = Actor('ground', (WIDTH/5, HEIGHT/2 + 5))

initial_pos = (WIDTH/5, HEIGHT/2 - 10)
player = Actor('player', )
player.pos = initial_pos
player.x_speed = 5
player.y_speed = 5
player.jump_force = 6

gravity = 1
terminal_speed = 10

def reset():
    player.pos = initial_pos

def update(dt):
    if keyboard.r:
        reset()
        
    move_player()

def move_player():
    movement_direction = keyboard.d - keyboard.a
    player.x += movement_direction * player.x_speed
 
    if player.y_speed < terminal_speed:
        player.y_speed += gravity
        
    if player.colliderect(ground):
        player.x_speed = 0
        player.y_speed = 0

    if player.colliderect(ground) and keyboard.space:
            player.y_speed -= player.jump_force

    player.y += player.y_speed

    return False

def on_mouse_down(button):
    if button == 1:
        print("SHOT", button, "clicked")

def draw():
    screen.clear()
    screen.fill((25, 25, 25))
    player.draw()
    ground.draw()
    
    
