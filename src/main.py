import pyxel
from enum import Enum
import pygame

class App:
    WIDTH = 320
    HEIGHT = 240
    
    def __init__(self):
        pyxel.init(self.WIDTH, self.HEIGHT, title="Pyxel Display PNG")
        pyxel.images[0].load(0, 0, "assets/pipo-xmaschara03.png")
        pyxel.images[1].load(0, 0, "assets/map.png")
        self.player = Player(0, 0, 0, 64, 64, 32, 32, 11, Direction.RIGHT)
        self.music_player = MusicPlayer('assets/music.mp3')
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.music_player.loop(time=0.0)
        pass

    def draw(self):
        pyxel.cls(0)
        self.draw_field()
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
    def __init__(self, x, y, img, u, v, w, h, colkey, direction):
        self.x = x
        self.y = y
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.direction = direction
        self.direction_count = 0

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

    def move(self, direction):
        if self.direction != direction:
            self.direction = direction
            self.direction_count = 0
        if direction == Direction.UP:
            self.y -= 1
        elif direction == Direction.LEFT:
            self.x -= 1
        elif direction == Direction.DOWN:
            self.y += 1
        elif direction == Direction.RIGHT:
            self.x += 1

        self.direction_count += 1
        self.u, self.v = 32 * (self.direction_count % 3), direction.value * 32

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

class MusicPlayer:
    def __init__(self,filename):
        pygame.mixer.init()
        pygame.mixer.music.load(filename)

    def loop(self,time=0.0):
        pos = pygame.mixer.music.get_pos()
        if int(pos) == -1:
            pygame.mixer.music.play(-1,time)

    def start(self, count=1):
        pygame.mixer.music.play(count)

    def stop(self):
        pygame.mixer.music.stop()

App()
