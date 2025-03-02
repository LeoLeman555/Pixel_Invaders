import pyxel as px


class EnemyLaser:
    """Represent a laser shot by an enemy in the game."""

    def __init__(self, main, x, y):
        self.main = main
        self.x = x
        self.y = y
        self.width = 1
        self.height = 3
        self.active = True
        self.laser_speed = 4

    def is_collision_player(self, player):
        """Check if the boost collides with the player."""
        return (
            self.x < player.x + player.width
            and self.x + self.width > player.x
            and self.y < player.y + player.height
            and self.y + self.height > player.y
        )

    def update(self):
        """Move the laser down."""
        self.y += self.laser_speed
        if self.is_collision_player(self.main.player):
            self.active = False
            self.main.player.lose_life()
        if self.y > px.height:
            self.active = False

    def draw(self):
        """Draw the laser."""
        px.rect(self.x, self.y, self.width, self.height, 8)
