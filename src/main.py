import pyxel
from enum import Enum
# import pygame
import random

GROUND_BASE = 190

BULLET_SIZE = [3, 4, 7]
# BULLET_HEIGHT = 2
BULLET_COLOR = [6, 11, 14]
BULLET_SPEED = [2, 3, 4]

PLAYER_SPEED = 3

bullets = []
particles = []

class App:
    WIDTH = 320
    HEIGHT = 240
    
    def __init__(self):
        pyxel.init(self.WIDTH, self.HEIGHT, title="Pyxel Display PNG")
        pyxel.images[0].load(0, 0, "assets/pipo-xmaschara03.png")
        pyxel.images[1].load(0, 0, "assets/map.png")
        pyxel.images[2].load(0, 0, "assets/pipo-charachip_otaku01.png")
        self.player = Player(0, GROUND_BASE, 0, 64, 64, 32, 32, 11, Direction.RIGHT, 0)
        self.otaku = Otaku(100, GROUND_BASE, 2, 64, 64, 32, 32, 11)
        # self.music_player = MusicPlayer('assets/music.mp3')
        random.seed()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.otaku.update()
        # self.music_player.loop(time=0.0)
        pass

    def draw(self):
        pyxel.cls(0)
        self.draw_field()
        
        for bullet in bullets:
            if bullet.is_alive:
                bullet.update()
                bullet.draw()
            else:
                bullets.remove(bullet)

        for particle in particles:
            if particle.is_alive:
                particle.update()
                particle.draw()
            else:
                particles.remove(particle)

        for bullet in bullets:
            # otaku との当たり判定
            if bullet.x > self.otaku.x and bullet.x < self.otaku.x + self.otaku.w and bullet.y > self.otaku.y and bullet.y < self.otaku.y + self.otaku.h:
                bullet.is_alive = False
                break

        pyxel.blt(
            self.otaku.x,
            self.otaku.y,
            self.otaku.img,
            self.otaku.u,
            self.otaku.v,
            self.otaku.w,
            self.otaku.h,
            self.otaku.colkey)

        pyxel.blt(
            self.player.x,
            self.player.y,
            self.player.img,
            self.player.u,
            self.player.v,
            self.player.w,
            self.player.h,
            self.player.colkey)


    def draw_field(self):
        pyxel.rect(0, 0, self.WIDTH, self.HEIGHT-16, 12)
        for x in range(0, self.WIDTH, 16):
            pyxel.blt(x, self.HEIGHT-16, 1, 0, 0, 16, 16)
        for i in range(int((self.WIDTH)/32)+2):
            pyxel.blt(i*32 - int(pyxel.frame_count/10)%64, int(self.WIDTH/8)*(i%2)+int(self.WIDTH/8), 1, 16, 0, 16, 16, 11)

class Direction(Enum):
    DOWN = 0
    LEFT = 1
    RIGHT = 2
    UP = 3

class Player:
    JUMP = 1
    GRAVITY = 1

    def __init__(self, x, y, img, u, v, w, h, colkey, direction, vy):
        self.x = x
        self.y = y
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.direction = direction
        self.vy = vy
        self.direction_count = 0
        self.begin_pressing = -1

    def update(self):
        direction_mapping = {
            pyxel.KEY_W: Direction.UP,
            pyxel.KEY_A: Direction.LEFT,
            pyxel.KEY_S: Direction.DOWN,
            pyxel.KEY_D: Direction.RIGHT
        }

        for key, direction in direction_mapping.items():
            if pyxel.btn(key):
                self.move(direction)
            else:
                self.apply_gravity()

        bullet_level = int((pyxel.frame_count - self.begin_pressing)/10)
        if bullet_level > 2:
            bullet_level = 2
        if pyxel.btn(pyxel.KEY_SPACE):
            print("space")
            if self.begin_pressing < 0:
                self.begin_pressing = pyxel.frame_count

            Particle(self.x + self.w/2, self.y + self.h/2, BULLET_COLOR[bullet_level], 5, 3, 3) 
        else:
            if self.begin_pressing > 0:
                Bullet(self.x + self.w/2, self.y + self.h/2, self.direction, bullet_level)
                self.begin_pressing = -1

            
    def apply_gravity(self):
        self.vy += self.GRAVITY
        self.y += self.vy
        if GROUND_BASE < self.y:
            self.y = GROUND_BASE

    def move(self, direction):
        self.apply_gravity()

        if self.direction != direction:
            self.direction = direction
            self.direction_count = 0
        if direction == Direction.UP:
            if self.y == GROUND_BASE:
                self.vy = -10 * self.JUMP
            # self.y -= 1
        elif direction == Direction.LEFT:
            self.x -= PLAYER_SPEED
        # elif direction == Direction.DOWN:
        #     self.y += 1
        elif direction == Direction.RIGHT:
            self.x += PLAYER_SPEED

        self.direction_count += 1
        self.u, self.v = 32 * (self.direction_count % 3), direction.value * 32

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

# class MusicPlayer:
#     def __init__(self,filename):
#         pygame.mixer.init()
#         pygame.mixer.music.load(filename)

#     def loop(self,time=0.0):
#         pos = pygame.mixer.music.get_pos()
#         if int(pos) == -1:
#             pygame.mixer.music.play(-1,time)

#     def start(self, count=1):
#         pygame.mixer.music.play(count)

#     def stop(self):
#         pygame.mixer.music.stop()

class Bullet:
    def __init__(self, x, y, direction, level):
        self.x = x
        self.y = y
        self.level = level
        self.direction = direction
        self.is_alive = True
        bullets.append(self)

    def update(self):
        if self.direction == Direction.LEFT:
            dx = -BULLET_SPEED[self.level]
        elif self.direction == Direction.RIGHT:
            dx = BULLET_SPEED[self.level]
        else:
            dx = 0

        self.x += dx
        if self.x < 0 or self.x > 320:
            self.is_alive = False
        if pyxel.frame_count % 2 == 0:
            Particle(self.x - 3*dx, self.y, None, 2)
            
            
    def draw(self):
        # pyxel.rect(self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT, BULLET_COLOR)
        pyxel.circ(self.x, self.y, BULLET_SIZE[self.level], BULLET_COLOR[self.level])
        pyxel.circ(self.x, self.y, int(BULLET_SIZE[self.level]/2), 7)

class Particle:
    def __init__(self, x, y, col = None, max_size = 2, diffusion = 1.2, size = 2):
        self.x = x
        self.y = y
        self.dx = diffusion * random.uniform(-1, 1)
        self.dy = diffusion * random.uniform(-1, 1)
        self.size = int(random.uniform(size-1, size+3))
        self.max_size = max_size
        self.dsize = random.uniform(-0.2, 0.2)
        self.col = col
        if self.col == None:
            self.col = int(random.uniform(1, 16))
        self.born = pyxel.frame_count
        self.lifespan = int(random.uniform(5, 12))
        self.is_alive = True
        particles.append(self)
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.size += self.dsize
        if self.born + self.lifespan < pyxel.frame_count:
            self.is_alive = False
        elif int(self.size) < 0:
            self.is_alive = False
        elif int(self.size) > self.max_size:
            self.size = self.max_size
            self.dsize = 0

    def draw(self):
        pyxel.rect(self.x, self.y, self.size, self.size, self.col)

class Otaku:
    def __init__(self, x, y, img, u, v, w, h, colkey):
        self.x = x
        self.y = y
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey

    def update(self):
        pass

    def draw(self):
        pass

App()
