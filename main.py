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
player.x_speed = 6
player.y_speed = 6
player.jump_force = 6

gravity = 0.6
terminal_speed = 12

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
        
    if collide_x():
        player.x_speed = 0
        
    if collide_y():
        player.y_speed = 0
        if collide_down and keyboard.space:
            player.y_speed -= player.jump_force

    player.y += player.y_speed

    return False


def collide_y():
    return (player.x + player.width >= ground.x
        and player.x < ground.x + ground.width
        and collide_up()
        and collide_down()
    )


def collide_x():
    return (player.y - player.height <= ground.y
        and player.y > ground.y + ground.height
        and collide_right()
        and collide_left()
    )


def collide_up():
    return player.y <= ground.y


def collide_right():
    return player.x >= ground.x


def collide_down():
    return player.y >= ground.y - ground.height


def collide_left():
    return player.x <= ground.x + ground.width


def on_collide_x(): 
    return False


def on_mouse_down(button):
    if button == 1:
        print("SHOT", button, "clicked")

def draw():
    screen.clear()
    screen.fill((25, 25, 25))
    player.draw()
    ground.draw()
    
    
