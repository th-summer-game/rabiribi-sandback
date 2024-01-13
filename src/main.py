import pyxel

class App:
    WIDTH = 320
    HEIGHT = 240
    
    def __init__(self):
        pyxel.init(self.WIDTH, self.HEIGHT, title="Pyxel Display PNG")
        pyxel.images[0].load(0, 0, "assets/pipo-xmaschara03.png")
        pyxel.images[1].load(0, 0, "assets/map.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        self.draw_field()
        pyxel.blt(0, 0, 0, 64, 64, 32, 32, 11)

    def draw_field(self):
        pyxel.rect(0, 0, self.WIDTH, self.HEIGHT-16, 12)
        for x in range(0, self.WIDTH, 16):
            pyxel.blt(x, self.HEIGHT-16, 1, 0, 0, 16, 16)
        for i in range(int((self.WIDTH)/32)+2):
            pyxel.blt(i*32 - int(pyxel.frame_count/10)%64, int(self.WIDTH/8)*(i%2)+int(self.WIDTH/8), 1, 16, 0, 16, 16, 11)

App()
