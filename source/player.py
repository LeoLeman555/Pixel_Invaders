import pyxel as px


class Player:
    def __init__(self, main, x, y):
        """Initialize the player with position, size, and attributes."""
        self.main = main
        self.width = 11
        self.height = 16
        self.x = x - self.width // 2
        self.y = y - self.height
        self.lives = 5
        self.speed = 2

    def lose_life(self):
        """Reduce player lives and check for game over."""
        self.lives -= 1
        if self.lives <= 0:
            self.main.game_state = "game_over"

    def move(self):
        """Handle player movement."""
        if px.btn(px.KEY_A) or px.btn(px.KEY_LEFT):
            if self.x > 0:
                self.x -= self.speed
        if px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT):
            if self.x < px.height - self.width:
                self.x += self.speed

    def update(self):
        """Update the player's state each frame."""
        self.move()

    def draw(self):
        """Render the player on the screen."""
        px.blt(self.x, self.y, 0, 0, 0, self.width, self.height, 0)
