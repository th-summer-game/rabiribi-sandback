import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Display PNG")
        pyxel.images[0].load(0, 0, "assets/pipo-xmaschara03.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.images[0].blt(50, 50, 0, 32, 32, 160, 120)

App()
