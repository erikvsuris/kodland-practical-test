import pgzrun

# REMOVER
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

TILE_SIZE = 32
ROWS = 25
COLUMNS = 50

WIDTH = TILE_SIZE * COLUMNS
HEIGHT = TILE_SIZE * ROWS

TITLE = "Rambo Rabbit"

PLATFORM_1 = Rect((0,HEIGHT/2), (WIDTH, TILE_SIZE))
PLATFORM_2 = Rect((WIDTH/5, HEIGHT-TILE_SIZE*3), (300, TILE_SIZE))
PLATFORM_3 = Rect((WIDTH/2, HEIGHT-TILE_SIZE), (300, TILE_SIZE))
PLATFORMS = [
    PLATFORM_1, 
    PLATFORM_2,
    PLATFORM_3
]

PLAYER = Actor('player')
START_POSITION = (WIDTH/4, HEIGHT/2-TILE_SIZE/2)
PLAYER.pos = START_POSITION
PLAYER.x_speed = 0
PLAYER.y_speed = 0
PLAYER.x_max_speed = 6
PLAYER.y_max_speed = 18
PLAYER.jump_force = 15

GRAVITY = 0.9

game_over = False


def update(dt):
    if not game_over:
        move_player()
        animate_player()
        if PLAYER.y >= HEIGHT:
            reset()

    if keyboard.r:
        reset()

    if keyboard.escape:
        exit()
        
    print(PLAYER.y, PLATFORM_1.y)


def on_mouse_down(button):
    if button == 1:
        print("SHOT", button, "clicked")


def move_player():
    movement_direction = keyboard.d - keyboard.a
    PLAYER.x_speed = PLAYER.x_max_speed*movement_direction
    
    if PLAYER.y_speed < PLAYER.y_max_speed:
        PLAYER.y_speed += GRAVITY

    if collide_x():
        PLAYER.xspeed = 0        

    if collide_y():
        PLAYER.y_speed = 0
        if keyboard.space:
            PLAYER.y_speed = -PLAYER.jump_force

    if PLAYER.x > 0 and PLAYER.x + PLAYER.width < WIDTH:
        PLAYER.x += PLAYER.x_speed

    if PLAYER.y - PLAYER.height > 0 and PLAYER.y < HEIGHT:
            PLAYER.y += PLAYER.y_speed


def collide_y():
    """ Verifica se o jogador colidiu com uma plataforma no eixo Y """
    for platform in PLATFORMS:
        if (PLAYER.colliderect(platform)
            and PLAYER.x + PLAYER.width > platform.x
            and PLAYER.x < platform.x + platform.width):
            if PLAYER.y + PLAYER.height >= platform.y and PLAYER.y + PLAYER.height <= platform.y + TILE_SIZE/2:
                return True
    return False


def collide_x():
    """ Verifica se o jogador colidiu lateralmente com uma plataforma """
    for platform in PLATFORMS:
        if (PLAYER.y + PLAYER.height > platform.y
            and PLAYER.y < platform.y + platform.height):
            if PLAYER.x + PLAYER.width >= platform.x and PLAYER.x <= platform.x:
                return True
            elif PLAYER.x <= platform.x + platform.width and PLAYER.x + PLAYER.width >= platform.x + platform.width:
                return True
    return False


def animate_player():
    if PLAYER.x_speed > 0:
        PLAYER.image = 'player_right'
    elif PLAYER.x_speed < 0:
        PLAYER.image = 'player_left'


def draw():
    if game_over:
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), "black")
        screen.draw.text("Game Over", center=(WIDTH/2, HEIGHT/2), color="white", fontsize=40)
    else:
        screen.clear()
        screen.fill((25, 25, 25))
        PLAYER.draw()
        
        for platform in PLATFORMS:
            screen.draw.filled_rect(platform, (250, 80, 80))


def reset():
    PLAYER.pos = START_POSITION
    PLAYER.x_speed = 0
    PLAYER.y_speed = 0


pgzrun.go()
