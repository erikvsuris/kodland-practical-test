# TODO REMOVER
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        

class Player(Actor):
    def __init__(self, start_position):
        super().__init__('player')
        self.pos = start_position
        self.previous_pos = start_position
        self.speed = Vector(x=0, y=0)
        self.max_speed = Vector(x=300, y=800)
        self.delta_pos = Vector(x=0,y=0)
        self.delta_x = 0
        self.delta_y = 0
        self.jump_force = 1000
        # PLAYER.hitbox_rect = PLAYER.rect.inflate(-16, -8)


TILE_SIZE = 32
ROWS = 25
COLUMNS = 50

WIDTH = TILE_SIZE * COLUMNS
HEIGHT = TILE_SIZE * ROWS

TITLE = "Rambo Rabbit"

START_POSITION = (WIDTH/4, HEIGHT/2-TILE_SIZE*5)
PLAYER = Player(START_POSITION)

COLLIDER_1 = Rect((0,HEIGHT/2), (WIDTH, TILE_SIZE))
COLLIDERS_2 = Rect((WIDTH/5, HEIGHT-TILE_SIZE*3), (300, TILE_SIZE))
COLLIDERS_3 = Rect((WIDTH/2, HEIGHT-TILE_SIZE), (300, TILE_SIZE))
COLLIDERS = [
    COLLIDER_1, 
    COLLIDERS_2,
    COLLIDERS_3
]

GRAVITY = 80

game_over = False


def update(dt):    
    if not game_over:
        move_player(dt)
        animate_player()
        # if PLAYER.y >= HEIGHT:
        #     reset()

    if keyboard.r:
        reset()

    if keyboard.escape:
        exit()


def on_mouse_down(button):
    if button == 1:
        print("SHOT", button, "clicked")


def move_player(delta_time):
    PLAYER.delta_x = 0
    PLAYER.delta_y = 0
    
    movement_direction = keyboard.d - keyboard.a
    PLAYER.speed.x = PLAYER.max_speed.x*movement_direction
    
    if PLAYER.speed.y < PLAYER.max_speed.y:
        PLAYER.speed.y += GRAVITY
        
    if PLAYER.left > 0 and PLAYER.right < WIDTH:
        PLAYER.delta_x += PLAYER.speed.x * delta_time

    if PLAYER.top > 0 and PLAYER.bottom < HEIGHT:
        PLAYER.delta_y += PLAYER.speed.y * delta_time

    # if collide("x"):
    #     PLAYER.speed.x = 0
        
    # if collide("y"):
    #     PLAYER.speed.y = 0
        
    # if collide("bottom") and keyboard.space:
    #     print("AAAAAAAAAAAA")
    #     PLAYER.speed.y = -PLAYER.jump_force
    
    collide()
    
    PLAYER.x += PLAYER.delta_x
    PLAYER.y += PLAYER.delta_y


def collide():
    for collider in COLLIDERS:
        if collider.colliderect(PLAYER.x + PLAYER.delta_pos.x, PLAYER.y, PLAYER.width, PLAYER.height):
            PLAYER.delta_pos.x = 0
        if collider.colliderect(PLAYER.x, PLAYER.y + PLAYER.delta_pos.y, PLAYER.width, PLAYER.height):
            if PLAYER.speed.y < 0:
                PLAYER.delta_pos.y = collider.bottom - PLAYER.top
                PLAYER.speed.y = 0
            elif PLAYER.speed.y >= 0:
                PLAYER.delta_y = collider.top - PLAYER.bottom
                PLAYER.speed.y = 0
    
    #     if PLAYER.colliderect(collider):
    #         if pos == "x":
    #             if PLAYER.right + PLAYER.speed.x > collider.left:
    #                 # PLAYER.right = collider.left
    #                 return True
    #             elif PLAYER.left - PLAYER.speed.x < collider.right:
    #                 # PLAYER.left = collider.right
    #                 return True
    #         elif pos == "y":
    #             if PLAYER.bottom + PLAYER.speed.y > collider.top:
    #                 PLAYER.bottom = collider.top
    #                 return True
    #             elif PLAYER.top  + PLAYER.speed.y < collider.bottom:
    #                 PLAYER.top = collider.bottom
    #                 return True
    #         elif pos == "bottom":
    #             if PLAYER.bottom > collider.top:
    #                 return True
    # return False


def animate_player():
    if PLAYER.speed.x > 0:
        PLAYER.image = 'player_right'
    elif PLAYER.speed.x < 0:
        PLAYER.image = 'player_left'


def draw():
    if game_over:
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), "black")
        screen.draw.text("Game Over", center=(WIDTH/2, HEIGHT/2), color="white", fontsize=40)
    else:
        screen.clear()
        screen.fill((252, 223, 205))
        
        PLAYER.draw()
        
        for collider in COLLIDERS:
            screen.draw.filled_rect(collider, (182, 213, 60))


def reset():
    PLAYER.pos = START_POSITION
    PLAYER.previous_pos = pos
    PLAYER.speed.x = 0
    PLAYER.speed.y = 0

