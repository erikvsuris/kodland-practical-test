import random
import math


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        

class Sprite():
    def __init__(self, image):
        self.image = image
        self.next = None


class Player(Actor):
    def __init__(self, start_position):
        super().__init__('player')
        self.pos = start_position
        self.hitbox = Rect(start_position, (self.width - 16, self.height))
        self.speed = Vector(x=0, y=0)
        self.max_speed = Vector(x=500, y=1000)
        self.movement_direction = 0
        self.last_direction = 1
        self.jump_force = 22
        self.on_ground = False
        
        self.life = 3
        self.damage_cooldown = 1
        self.damage_timer = self.damage_cooldown
        
        right_idle_0 = Sprite('player_right')
        right_idle_1 = Sprite('player_right_idle_1')
        right_idle_2 = Sprite('player_right_idle_2')
        right_idle_3 = Sprite('player_right_idle_3')
        right_idle_0.next = right_idle_1
        right_idle_1.next = right_idle_2
        right_idle_2.next = right_idle_3
        right_idle_3.next = right_idle_0
        self.sprites_idle_right = right_idle_0
        
        left_idle_0 = Sprite('player_left')
        left_idle_1 = Sprite('player_left_idle_1')
        left_idle_2 = Sprite('player_left_idle_2')
        left_idle_3 = Sprite('player_left_idle_3')
        left_idle_0.next = left_idle_1
        left_idle_1.next = left_idle_2
        left_idle_2.next = left_idle_3
        left_idle_3.next = left_idle_0
        self.sprites_idle_left = left_idle_0
        
        
        self.sprites_jump_right = 'player_right_jump'
        self.sprites_jump_left = 'player_left_jump'
        
        
        right_sprint_0 = Sprite('player_right')
        right_sprint_1 = Sprite('player_right_sprint_1')
        right_sprint_0.next = right_sprint_1
        right_sprint_1.next = right_sprint_0
        self.sprites_sprint_right = right_sprint_0
        
        left_sprint_0 = Sprite('player_left')
        left_sprint_1 = Sprite('player_left_sprint_1')
        left_sprint_0.next = left_sprint_1
        left_sprint_1.next = left_sprint_0

        self.sprites_sprint_left = left_sprint_0
        
        self.animation_timer = 0.0
        self.animation_interval = 0.1

    def update(self, delta_time):
        self.move(delta_time)
        self.animate(delta_time)
        
        self.damage_timer += delta_time

        self.hitbox.center = self.center

    def move(self, delta_time):
        self.movement_direction = keyboard.d - keyboard.a
        if self.movement_direction != 0:
            self.last_direction = self.movement_direction
        self.speed.x = self.max_speed.x * self.movement_direction * delta_time
        self.hitbox.x += self.speed.x

        self.collide_x()

        self.x = self.hitbox.centerx

        self.jump()

        self.speed.y += GRAVITY * delta_time
        self.hitbox.y += self.speed.y
        
        self.on_ground = False
        self.collide_y()

        self.y = self.hitbox.centery


    def collide_x(self):
        for collider in COLLIDERS:
            if self.hitbox.colliderect(collider):
                if self.movement_direction > 0:
                    self.hitbox.right = collider.left
                elif self.movement_direction < 0:
                    self.hitbox.left = collider.right


    def collide_y(self):
        for collider in COLLIDERS:
            if self.hitbox.colliderect(collider):
                if self.speed.y > 0:
                    self.hitbox.bottom = collider.top
                    self.speed.y = 0
                    self.on_ground = True
                elif self.speed.y < 0:
                    self.hitbox.top = collider.bottom
                    self.speed.y = 0


    def jump(self):
        if keyboard.space and self.on_ground:
            self.speed.y = -self.jump_force
            self.on_ground = False


    def animate(self, delta_time):
        if not self.on_ground:
            self.animation_timer = 0.0
            if self.last_direction == 1:
                self.image = self.sprites_jump_right
            elif self.last_direction == -1:
                self.image = self.sprites_jump_left
        else: 
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_interval:
                self.animation_timer = 0.0
                if self.speed.x == 0:
                    if self.last_direction == 1:
                        self.image = self.sprites_idle_right.image
                        self.sprites_idle_right = self.sprites_idle_right.next
                    elif self.last_direction == -1:
                        self.image = self.sprites_idle_left.image
                        self.sprites_idle_left = self.sprites_idle_left.next
                else:
                    if self.speed.x > 0:
                        self.image = self.sprites_sprint_right.image
                        self.sprites_sprint_right = self.sprites_sprint_right.next
                    elif self.speed.x < 0:
                        self.image = self.sprites_sprint_left.image
                        self.sprites_sprint_left = self.sprites_sprint_left.next


class Projectile(Actor):
    def __init__(self, player, target_position):
        dx = target_position[0] - player.x
        dy = target_position[1] - player.y
        angle = math.atan2(dy, dx)
        super().__init__('bullet')
        
        self.x = player.x
        self.y = player.y
        self.angle = angle
        self.speed = 2000
        
        self.vel_x = self.speed * math.cos(angle)
        self.vel_y = self.speed * math.sin(angle)
    
    def update(self, delta_time):
        self.x += self.vel_x * delta_time
        self.y += self.vel_y * delta_time


class Enemy(Actor):
    def __init__(self, start_position, player):
        super().__init__('enemy')
        self.pos = start_position
        self.speed = Vector(x=0, y=0)
        self.max_speed = Vector(x=250, y=250)
        self.movement_direction = Vector(x=random.choice([-1,1]), y=random.choice([-1,1]))
        self.change_direction = False
        self.last_direction = 1
        
        self.player = player
        
        self.life = 5
        
        right_0 = Sprite('enemy_right_0')
        right_1 = Sprite('enemy_right_1')
        right_0.next = right_1
        right_1.next = right_0
        self.sprites_right = right_0
        
        left_0 = Sprite('enemy_left_0')
        left_1 = Sprite('enemy_left_1')
        left_0.next = left_1
        left_1.next = left_0
        self.sprites_left = left_0
        
        self.animation_timer = 0.0
        self.animation_interval = 0.1

    def update(self, delta_time):
        self.move(delta_time)
        self.animate(delta_time)


    def move(self, delta_time):
        self.collide()            
        
        if self.movement_direction.x != 0:
            self.last_direction = self.movement_direction.x

        self.speed.x = self.max_speed.x * self.movement_direction.x * delta_time
        self.x += self.speed.x
        
        self.speed.y = self.max_speed.y * self.movement_direction.y * delta_time
        self.y += self.speed.y
        


    def collide(self):
        if self.left < 0 or self.right > WIDTH:
            self.movement_direction.x = -self.movement_direction.x
        elif self.top < 0 or self.bottom > HEIGHT:
            self.movement_direction.y = -self.movement_direction.y
            
        for collider in COLLIDERS:
            if self.colliderect(collider):
                self.movement_direction.x = -self.movement_direction.x
                self.movement_direction.y = -self.movement_direction.y


    def animate(self, delta_time):
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0.0
            if self.last_direction == 1:
                self.image = self.sprites_right.image
                self.sprites_right = self.sprites_right.next
            elif self.last_direction == -1:
                self.image = self.sprites_left.image
                self.sprites_left = self.sprites_left.next
            
        self.animation_timer += delta_time


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


TILE_SIZE = 32
ROWS = 25
COLUMNS = 50

WIDTH = TILE_SIZE * COLUMNS
HEIGHT = TILE_SIZE * ROWS

TITLE = "Rambo Rabbit"

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50
BUTTON_COLOR = (70, 130, 180)
START_BUTTON = Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 - 60), (BUTTON_WIDTH, BUTTON_HEIGHT))
SOUND_BUTTON = Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2), (BUTTON_WIDTH, BUTTON_HEIGHT))
EXIT_BUTTON = Rect((WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 + 60), (BUTTON_WIDTH, BUTTON_HEIGHT))

COLLIDERS = [
    Rect((0,HEIGHT-TILE_SIZE*11), (TILE_SIZE*18, TILE_SIZE*12)),
    Rect((TILE_SIZE*24,HEIGHT-TILE_SIZE*11), (TILE_SIZE*12, TILE_SIZE*12)),
    Rect((TILE_SIZE*40,HEIGHT-TILE_SIZE*11), (TILE_SIZE*10, TILE_SIZE*12)),
    Rect((0,0), (60, TILE_SIZE*14)),
    Rect((WIDTH-60,0), (60, TILE_SIZE*14)),
    Rect((TILE_SIZE*6,TILE_SIZE*10), (TILE_SIZE*6, TILE_SIZE*2)),
    Rect((TILE_SIZE*28,TILE_SIZE*10), (TILE_SIZE*4, TILE_SIZE*2)),
]

START_POSITION = (100, HEIGHT/2-TILE_SIZE*2)
PLAYER = Player(START_POSITION)
PROJECTILES = []

ENEMY_POSITION_1 = (400, 200)
ENEMY_POSITION_2 = (800, 200)
ENEMY_POSITION_3 = (1200, 200)
ENEMIES = [
    Enemy(ENEMY_POSITION_1, PLAYER),
    Enemy(ENEMY_POSITION_2, PLAYER),
    Enemy(ENEMY_POSITION_3, PLAYER),
]


GRAVITY = 70

game_state = "menu"
sounds_on = True


def update(delta_time):
    global game_state, sounds_on

    if sounds_on and not music.is_playing("background"):
        music.play("background")
    elif not sounds_on and music.is_playing("background"):
        music.stop()
    
    if game_state == "playing":
        for enemy in ENEMIES:
            if enemy.colliderect(PLAYER):
                if PLAYER.damage_timer > PLAYER.damage_cooldown:
                    PLAYER.damage_timer = 0
                    PLAYER.life -= 1
                    if sounds_on:
                        sounds.ouch.play()
                
        if PLAYER.life == 0:
            game_state = "over"
        
        check_projectiles()
                
        PLAYER.update(delta_time)
        for projectile in PROJECTILES:
            projectile.update(delta_time)
        for enemy in ENEMIES:
            enemy.update(delta_time)

        if keyboard.escape:
            game_state = "menu"
        if len(ENEMIES) == 0:
            game_state = "win"
        if PLAYER.y > HEIGHT:
            game_state = "over"
    elif game_state == "win" or game_state == "over":
        if keyboard.escape:
            reset()
            game_state = "menu"


def check_projectiles():
    for projectile in PROJECTILES:
        if projectile.right > WIDTH or projectile.left < 0:
            PROJECTILES.remove(projectile)
            del projectile
            continue

        collided = False
        for collider in COLLIDERS:
            if projectile.colliderect(collider):
                PROJECTILES.remove(projectile)
                del projectile
                collided = True
                break
        if collided:
            continue

        for enemy in ENEMIES:
            if projectile.colliderect(enemy):
                if sounds_on:
                    sounds.hit.play() 
                PROJECTILES.remove(projectile)
                del projectile
                enemy.life -= 1
                if enemy.life <= 0:
                    ENEMIES.remove(enemy)
                    del enemy
                break


def on_mouse_down(pos, button):
    if button == 1:
        global game_state, sounds_on
        match game_state:
            case "menu":
                if START_BUTTON.collidepoint(pos):
                    game_state = "playing"
                    reset()
                elif SOUND_BUTTON.collidepoint(pos):
                    sounds_on = not sounds_on
                elif EXIT_BUTTON.collidepoint(pos):
                    exit()
            case "playing":
                PROJECTILES.append(Projectile(PLAYER, pos))
                if sounds_on:
                    sounds.shot.play() 


def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "win":
        draw_win()
    elif game_state == "over":
        draw_over()

def draw_menu():
    screen.fill((30, 30, 30))
    
    screen.draw.text("RAMBO RABBIT", center=(WIDTH/2, HEIGHT/4), fontsize=60, color="white")
    
    screen.draw.filled_rect(START_BUTTON, BUTTON_COLOR)
    screen.draw.text("Play", center=START_BUTTON.center, fontsize=30, color="white")
    
    music_text = f"Music and Sound: {"On" if sounds_on else "Off"}"
    screen.draw.filled_rect(SOUND_BUTTON, BUTTON_COLOR)
    screen.draw.text(music_text, center=SOUND_BUTTON.center, fontsize=30, color="white")
    
    screen.draw.filled_rect(EXIT_BUTTON, BUTTON_COLOR)
    screen.draw.text("Exit", center=EXIT_BUTTON.center, fontsize=30, color="white")

def draw_game():
    screen.fill((25, 25, 25))
    screen.blit('background', (0,0))
    
    for enemy in ENEMIES:
        enemy.draw()
        
    for projectile in PROJECTILES:
        projectile.draw()
        
    PLAYER.draw()
    for i in range(PLAYER.life):
        screen.blit('heart', ((i * TILE_SIZE) + TILE_SIZE * 3, TILE_SIZE))


def draw_win():
    screen.fill("black")
    screen.draw.text("You Won!", center=(WIDTH/2, HEIGHT/2 - 20), color="white", fontsize=40)
    screen.draw.text("Press ESCAPE to return menu", center=(WIDTH/2, HEIGHT/2 + 20), color="white", fontsize=30)

def draw_over():
    screen.fill("black")
    screen.draw.text("Game Over", center=(WIDTH/2, HEIGHT/2 - 20), color="white", fontsize=40)
    screen.draw.text("Press ESCAPE to return menu", center=(WIDTH/2, HEIGHT/2 + 20), color="white", fontsize=30)


def reset():
    PLAYER.pos = START_POSITION
    PLAYER.hitbox.x = PLAYER.x - PLAYER.hitbox.width / 2
    PLAYER.hitbox.y = PLAYER.y - PLAYER.hitbox.height / 2
    PLAYER.speed.x = 0
    PLAYER.speed.y = 0
    PLAYER.life = 3
    
    PROJECTILES.clear()
    
    ENEMIES.clear()
    ENEMIES.extend([
        Enemy(ENEMY_POSITION_1, PLAYER),
        Enemy(ENEMY_POSITION_2, PLAYER),
        Enemy(ENEMY_POSITION_3, PLAYER)
    ])
