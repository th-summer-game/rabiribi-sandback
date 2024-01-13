import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Display PNG")
        pyxel.images[0].load(0, 0, "assets/pipo-xmaschara03.jpg")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 64, 64, 32, 32, 13)

App()
