import pyxel

class App:
    WIDTH = 320
    HEIGHT = 240
    
    def __init__(self):
        pyxel.init(self.WIDTH, self.HEIGHT, title="Pyxel Display PNG")
        pyxel.images[0].load(0, 0, "assets/pipo-xmaschara03.png")
        pyxel.images[1].load(0, 0, "assets/map.png")
        self.player = Player(0, 0, 0, 64, 64, 32, 32, 11)
        pyxel.run(self.update, self.draw)

    def update(self):
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

class Player:
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
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, self.colkey)

    def draw_field(self):
        pyxel.rect(0, 0, self.WIDTH, self.HEIGHT-16, 12)
        for x in range(0, self.WIDTH, 16):
            pyxel.blt(x, self.HEIGHT-16, 1, 0, 0, 16, 16)
        for i in range(int((self.WIDTH)/32)+2):
            pyxel.blt(i*32 - int(pyxel.frame_count/10)%64, int(self.WIDTH/8)*(i%2)+int(self.WIDTH/8), 1, 16, 0, 16, 16, 11)

App()
