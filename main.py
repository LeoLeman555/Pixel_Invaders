import pyxel as px
from source.laser import *

SCREEN_SIZE = 128
SHIP_SIZE = (11, 16)

class Main:
    def __init__(self):
        """Initialize the game and load resources."""
        px.init(SCREEN_SIZE, SCREEN_SIZE, "Pixel Invaders")

        # Load the ship image
        px.image(0).load(0, 0, "assets/images/player_ship.png")
        self.x = SCREEN_SIZE // 2
        self.y = SCREEN_SIZE // 2

        self.laser_manager = LaserManager()

        self.run()

    def update(self):
        """Update game logic."""
        if px.btnp(px.KEY_SPACE):
            self.laser_manager.create_laser(1, 3, 10, self.x, self.y, SHIP_SIZE[0])
        self.laser_manager.move_lasers()

        self.move()

    def move(self):
        """Handle player movement."""
        if px.btn(px.KEY_W) or px.btn(px.KEY_UP):
            if self.y > 0:
                self.y -= 1
        if px.btn(px.KEY_A) or px.btn(px.KEY_LEFT):
            if self.x > 0:
                self.x -= 1
        if px.btn(px.KEY_S) or px.btn(px.KEY_DOWN):
            if self.y < SCREEN_SIZE - SHIP_SIZE[1]:
                self.y += 1
        if px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT):
            if self.x < SCREEN_SIZE - SHIP_SIZE[0]:
                self.x += 1

    def draw(self):
        """Render game elements on the screen."""
        px.cls(0)
        self.laser_manager.draw_lasers()
        px.blt(self.x, self.y, 0, 0, 0, SHIP_SIZE[0], SHIP_SIZE[1] + 2)
        px.text(0, 0, f"{self.x, self.y}", 7) # Draw the x and the y for debugging

    def run(self):
        """Start the game loop."""
        px.run(self.update, self.draw)

if __name__ == "__main__":
    Main()
